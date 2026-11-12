"""Write tests/rehearsal/results.md from the rehearsal runs, and copy the final round's logs next to it.

    py tools/summarize_rehearsal.py "Round 1=tmp/rehearsal/r1" "Round 2=tmp/rehearsal/final" "Round 3=tmp/rehearsal/round3"

Each argument is a label and a folder of runs made with tools/mock_nas.py. Every run is scored again
with tools/check_rehearsal.py, so all rounds are measured by the same checks. The last round is the
one the submitted package was frozen at; its logs are copied to tests/rehearsal/runs/.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_rehearsal as cr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "rehearsal"


def score(run_dir):
    scen, res, log = cr.check(run_dir)
    dele = [e for e in log if e["kind"] == "delegate"]
    asks = [e for e in log if e["kind"] == "ask"]
    waits = [e for e in log if e["kind"] == "wait"]
    return {
        "run": Path(run_dir).name, "title": scen["title"], "covers": scen.get("covers", ""),
        "checks": len(res), "passed": sum(r["pass"] for r in res),
        "failed": [r["check"] for r in res if not r["pass"]],
        "delegations": len(dele), "first": sum(1 for e in dele if e.get("template")),
        "writes": len(waits), "asks": len(asks),
        "longest": max([e["chars"] for e in dele] or [0]),
    }


def main(args):
    rounds = []
    for arg in args:
        label, folder = arg.split("=", 1)
        runs = sorted(p for p in (ROOT / folder).iterdir() if (p / "log.jsonl").exists())
        rounds.append((label, folder, [score(r) for r in runs]))
    final_label, final_folder, final = rounds[-1]

    lines = ["# Rehearsal results", "",
             "A small, fast model played the NAS assistant. It was given the brief in [assistant-brief.md](assistant-brief.md) and the Skill package, "
             "and nothing else, and acted only through [tools/mock_nas.py](../../tools/mock_nas.py): a scripted NAS whose five experts answer from a made-up library "
             "([library.json](library.json)) and whose user answers from a script ([scenarios.json](scenarios.json)). "
             "[tools/check_rehearsal.py](../../tools/check_rehearsal.py) then scored what it sent, what was saved and what it told the user. "
             "The mock accepts an instruction only if it is one of the Skill's templates with every slot filled, so a run also measures how often the model sent the template as written.", "",
             "This is a fixture test. It shows that a small model can follow the instructions as written, that no write happens without approval, and that the checks hold on a made-up library. "
             "It says nothing about recall on a real library or about how the real experts behave: those wait for the NAS.", ""]
    total_c = sum(r["checks"] for r in final)
    total_p = sum(r["passed"] for r in final)
    lines += [f"## {final_label}: the package as submitted", "",
              f"**{total_p} of {total_c} checks passed over {len(final)} runs of {len({r['title'] for r in final})} scenarios.** "
              f"{sum(r['delegations'] for r in final)} delegations and {sum(r['writes'] for r in final)} write approvals in all; "
              f"{sum(r['first'] for r in final)} of {sum(r['delegations'] for r in final)} instructions were accepted as first sent; the rest were rejected by the mock as not matching a template. "
              f"The longest instruction was {max(r['longest'] for r in final):,} characters.", "",
              "| Run | Scenario | Test-plan cases | Checks | Delegations | Accepted as first sent | Failed checks |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in final:
        lines.append(f"| {r['run']} | {r['title']} | {r['covers']} | {r['passed']} of {r['checks']} | {r['delegations']} | {r['first']} | {'; '.join(r['failed']) or 'none'} |")
    lines += ["", "The logs of these runs (every instruction sent, every reply, every question and answer) are in [runs/](runs/), with each run's `checks.json`.", ""]
    lines += ["## Every round", "", "Each round found gaps in the Skill's wording; they were fixed before the next. The same checks score every round.", "",
              "| Round | Runs | Checks passed | Accepted as first sent |", "| --- | --- | --- | --- |"]
    for label, folder, runs in rounds:
        lines.append(f"| {label} | {len(runs)} | {sum(r['passed'] for r in runs)} of {sum(r['checks'] for r in runs)} | {sum(r['first'] for r in runs)} of {sum(r['delegations'] for r in runs)} |")
    lines += [""]
    for label, folder, runs in rounds[:-1]:
        fails = [(r["run"], f) for r in runs for f in r["failed"]]
        if fails:
            lines += [f"Failed in {label}: " + "; ".join(f"{run}: {f}" for run, f in fails) + ".", ""]
    lines += ["## Notes", "",
              "- Round 1 had a sixth run, the break-in. It is left out: the scripted user answered a question about the camera window with its answer about the exhibit copies, a fault in the mock's script that was fixed before round 2.",
              "- The checks were tightened as the Skill was: the ten-line and 4,000-character checks were added when the Skill set those limits, and every round above is scored with today's checks.",
              "- Rounds 6 and 7 ran after the claim search was changed to describe nine photos spread across the capture dates instead of the eight latest (the version note in `references/disclosures.md` says why). "
              "In round 6, one run asked about the items of the voice walk-through instead of listing them; the user's reply did not answer, and under the rule that an unanswered question decides nothing, four lost items were left off the claim. "
              "C2 and C3 now keep what the user names, typed or spoken, on the list unless the user removes it. Round 6 also found three wording gaps, fixed before round 7: a receipt for a row already in the ledger, the exhibit line when the copies are declined, and what continuing a claim search means.",
              "- One check in the altered-save scenario, \"the mock altered one saved value\", confirms the mock did its part rather than testing the assistant.",
              "- After the last round, nothing in the package changed.", ""]
    (OUT / "results.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    (OUT / "results.json").write_text(json.dumps({"rounds": [{"label": l, "runs": r} for l, _, r in rounds]}, indent=1) + "\n", encoding="utf-8")

    dest = OUT / "runs"
    if dest.exists():
        shutil.rmtree(dest)
    for r in final:
        src = ROOT / final_folder / r["run"]
        (dest / r["run"]).mkdir(parents=True)
        for name in ("log.jsonl", "state.json", "checks.json"):
            if (src / name).exists():
                shutil.copyfile(src / name, dest / r["run"] / name)
    print(f"{final_label}: {total_p} of {total_c} checks over {len(final)} runs; written to {OUT / 'results.md'}")


if __name__ == "__main__":
    main(sys.argv[1:])
