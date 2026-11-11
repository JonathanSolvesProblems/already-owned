"""Check the Skill package against the Round 1 limits, with no dependency beyond Python.

Run from the repository root:  python tools/check_package.py
Exit code 0 means every check passed. This does not replace UGREEN's own checker
(uliya-skill-kit/scripts/check-skill.mjs); it lets anyone verify the package without it.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill" / "home-contents-inventory"
EXPERTS = {"photo-agent", "document-agent", "knowledge-agent", "file-agent", "security-monitor-agent"}
SECTIONS = ["# Goal", "# Required input", "# Generation-time capability evidence",
            "# Orchestration", "# Completion and failure"]
STATES = ["completed", "failed", "cancelled", "waiting_user", "waiting_approval"]

failures = []


def check(ok: bool, label: str, detail: str = "") -> None:
    print(("PASS  " if ok else "FAIL  ") + label + (f"  ({detail})" if detail else ""))
    if not ok:
        failures.append(label)


def main() -> int:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    check(front is not None, "SKILL.md starts with frontmatter")
    fields = dict(line.split(": ", 1) for line in front.group(1).splitlines()) if front else {}
    check(set(fields) == {"name", "description"}, "frontmatter holds only name and description")
    name = fields.get("name", "")
    check(bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)) and 2 <= len(name) <= 64,
          "name is lowercase, hyphenated, 2 to 64 characters", name)
    check(name == SKILL.name, "name matches the package folder")
    description = fields.get("description", "")
    check(0 < len(description) <= 1024, "description is at most 1,024 characters", f"{len(description)}")

    for section in SECTIONS:
        check(re.search(rf"^{re.escape(section)}$", text, flags=re.M) is not None, f"section present: {section}")
    for state in STATES:
        check(f"`{state}`" in text, f"delegation state handled: {state}")

    files = sorted(p for p in SKILL.rglob("*") if p.is_file())
    check(len(files) <= 100, "at most 100 files", f"{len(files)}")
    check(all(p.suffix == ".md" for p in files), "Markdown only: no script, binary or manifest")
    check(all(p.stat().st_size <= 1024 * 1024 for p in files), "every file is at most 1 MB")
    total = sum(p.stat().st_size for p in files)
    check(total <= 10 * 1024 * 1024, "package is at most 10 MB", f"{total} bytes")

    references = sorted(p.name for p in (SKILL / "references").glob("*.md"))
    linked = set(re.findall(r"\]\(references/([a-z0-9-]+\.md)\)", text))
    check(set(references) == linked, "every reference is linked from SKILL.md and every link resolves",
          ", ".join(references))

    delegations = re.findall(r"^`delegate --target ([a-z-]+) --instruction '(.*)'`$", text, flags=re.M)
    check(len(delegations) == text.count("`delegate --target"), "every delegation is one line in single quotes")
    targets = {target for target, _ in delegations}
    check(targets <= EXPERTS, "every delegation targets a registered expert", ", ".join(sorted(targets)))
    check(not any(re.search(r"[<>|]| --[a-z]", body) for _, body in delegations),
          "no angle bracket, pipe or command option inside an instruction")
    check("cli.invoke" not in text, "no direct CLI call")
    writes = [body for _, body in delegations
              if re.search(r"\b(Create|Save|Place a duplicate|attach that tag)\b", body)]
    check(all("request user approval first" in body for body in writes),
          "every write delegation asks for approval first", f"{len(writes)} writes")

    steps = re.findall(r"^\*\*([UAC]\d+[ab]?)\. ", text, flags=re.M)
    print(f"\n{len(steps)} steps, {len(delegations)} delegations, {len(targets)} experts, "
          f"{len(references)} references, SKILL.md {len(text.encode('utf-8'))} bytes")
    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nAll checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
