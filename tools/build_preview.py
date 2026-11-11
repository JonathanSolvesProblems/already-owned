"""Build the gallery images for the project page into preview/ (1500 x 1000 PNG, at most eight).

Every figure on a slide is read from a file in this repository, and every product capture is taken
from the deployed page, so a changed result or a changed page redraws the slides.

    py tools/build_preview.py            # all slides
    py tools/build_preview.py 2 8        # only those numbers

Needs: playwright (chromium), pillow.
"""
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"
CAP = ROOT / "tmp" / "preview-captures"
SITE = "https://jonathansolvesproblems.github.io/already-owned/"
ADDRESS = "jonathansolvesproblems.github.io/already-owned"
W, H = 1500, 1000


# ---------- figures, read from files ----------
def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def figures() -> dict:
    census = read("results/pre-loss-photo-census.md")
    ablation = read("results/ablation-filename-date.md")
    runs = read("tests/dry-run/runs-2026-11-11.md")
    index = read("tests/dry-run/README.md")
    skill = read("skill/home-contents-inventory/SKILL.md")
    f = {}
    f["confirmed"], f["items"] = map(int, re.search(r"Confirmed: (\d+) of (\d+)", census).groups())
    f["unclear"] = int(re.search(r"Plausible: (\d+)", census).group(1))
    f["nowhere"] = int(re.search(r"Not found anywhere: (\d+)", census).group(1))
    f["by_name"] = int(re.search(r"Verified result: (\d+) of \d+", ablation).group(1))
    f["pass"] = int(re.search(r"\| Pass \| (\d+) \|", runs).group(1))
    f["partial"] = int(re.search(r"\| Partial \| (\d+) \|", runs).group(1))
    f["fail"] = int(re.search(r"\| Fail \| (\d+) \|", runs).group(1))
    f["cases"] = f["pass"] + f["partial"] + f["fail"]
    f["defects"] = sum(int(n) for n in re.findall(r"(\d+)(?: more)? defects", index))
    f["templates"] = len(re.findall(r"(?m)^`delegate --target ", skill))
    f["experts"] = len(set(re.findall(r"(?m)^`delegate --target ([a-z-]+) ", skill)))
    f["clis"] = len(re.findall(r"(?m)^- `[a-z-]+` → `[a-z-]+`$", skill))
    f["references"] = len(list((ROOT / "skill/home-contents-inventory/references").glob("*.md")))
    assert f["confirmed"] + f["unclear"] + f["nowhere"] == f["items"], f
    return f


F = figures()

# ---------- brand ----------
CSS = """
*{box-sizing:border-box;margin:0}
.sq .cell{aspect-ratio:1}
html,body{width:1500px;height:1000px;overflow:hidden}
body{background:#fbc23a;color:#1d1817;font:400 30px/1.4 "Hanken Grotesk",sans-serif;position:relative}
.wm{position:absolute;left:64px;top:46px;font:800 34px/1 "Besley",serif;letter-spacing:-.02em}
.src{position:absolute;right:64px;top:54px;font:400 19px/1 "Red Hat Mono",monospace}
.at{position:absolute;right:64px;bottom:40px;font:400 19px/1 "Red Hat Mono",monospace}
.dark .wm,.dark .src,.dark .at{color:#f9ead4}
h1{font:800 92px/1.02 "Besley",serif;letter-spacing:-.025em}
.lead{font:500 34px/1.36 "Hanken Grotesk",sans-serif}
.mono{font-family:"Red Hat Mono",monospace}
.hand{font-family:"Shantell Sans",cursive;font-weight:500}
.stage{position:absolute;left:64px;right:64px;top:130px;bottom:96px}
img{display:block}
.frame{position:relative;background:#141010;padding:10px}
.frame img{width:100%;aspect-ratio:3/2;object-fit:cover}
.cell{aspect-ratio:3/2;position:relative}
"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Besley:wght@500;800&family=Hanken+Grotesk:wght@400;500;700&family=Red+Hat+Mono:wght@400;600&family=Shantell+Sans:wght@500&display=swap" rel="stylesheet">')


def page(body: str, source: str, dark: bool = False, extra_css: str = "", address: bool = True) -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{CSS}{extra_css}</style></head>"
            f"<body class='{'dark' if dark else ''}'><div class='wm'>Already Owned</div><div class='src'>{source}</div>"
            f"{body}{f'<div class=at>{ADDRESS}</div>' if address else ''}</body></html>")


def art(name: str) -> str:
    return (ROOT / "docs" / "art" / f"{name}.jpg").as_uri()


def cap(name: str) -> str:
    return (CAP / f"{name}.png").as_uri()


# ---------- slides ----------
def s1_cover():
    body = f"""
    <div class='stage' style='top:112px'>
      <div style='display:flex;align-items:flex-end;gap:34px'>
        <div style='font:800 286px/.78 "Besley",serif;letter-spacing:-.05em'>{F['confirmed']}</div>
        <div style='font:500 60px/1.1 "Besley",serif;letter-spacing:-.02em;padding-bottom:6px;max-width:15em'>of the {F['items']} things I lost in a flood were already in my photos.</div>
      </div>
    </div>
    <img src='{cap('sheet')}' style='position:absolute;left:38px;top:322px;width:1392px'>"""
    return page(body, "my June 2026 claim · counted by hand", address=False)


def s2_baseline():
    def cells(kinds):
        out = []
        for k in kinds:
            if k == "yes":
                out.append("<div class='cell' style='background:#f9ead4;border:5px solid #141010;outline:5px solid #2c6b50'></div>")
            elif k == "maybe":
                out.append("<div class='cell' style='border:4px dashed #2c6b50'></div>")
            else:
                out.append("<div class='cell' style='border:4px dashed #a81f18'></div>")
        return "".join(out)
    top = ["yes"] * F["confirmed"] + ["maybe"] * F["unclear"] + ["no"] * F["nowhere"]
    bottom = ["yes"] * F["by_name"] + ["no"] * (F["items"] - F["by_name"])
    grid = "display:grid;grid-template-columns:repeat(9,1fr);gap:16px 14px"
    body = f"""
    <div class='stage'>
      <h1 style='font-size:76px'>The proof was there. Its file names were not</h1>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:70px;margin-top:40px'>
        <div>
          <div style='display:flex;align-items:baseline;gap:18px;margin-bottom:22px'><span style='font:800 176px/.8 "Besley",serif;letter-spacing:-.04em'>{F['confirmed']}</span><span class='lead' style='font-size:30px'>of {F['items']} items appear in a photo<br>I took before the flood</span></div>
          <div class='sq' style='{grid}'>{cells(top)}</div>
          <p style='font-size:23px;margin-top:20px'>{F['unclear']} more are unclear in photos. {F['nowhere']} are in no photo at all.</p>
        </div>
        <div>
          <div style='display:flex;align-items:baseline;gap:18px;margin-bottom:22px'><span style='font:800 176px/.8 "Besley",serif;letter-spacing:-.04em'>{F['by_name']}</span><span class='lead' style='font-size:30px'>of {F['items']} found by searching<br>file names and dates</span></div>
          <div class='sq' style='{grid}'>{cells(bottom)}</div>
          <p style='font-size:23px;margin-top:20px'>A phone names a photo <span class='mono' style='font-size:21px'>20251211_160058.jpg</span>. It never says sofa.</p>
        </div>
      </div>
    </div>"""
    return page(body, "results/pre-loss-photo-census.md · ablation-filename-date.md")


def s3_voice():
    body = f"""
    <div class='stage'>
      <div style='display:grid;grid-template-columns:.92fr 1.08fr;gap:60px;height:100%;align-items:center'>
        <div>
          <h1 style='color:#fbc23a'>Walk the room. Say what you lost</h1>
          <p class='lead' style='color:#f9ead4;margin-top:34px'>The NAS transcribes the voice note itself, then looks for each thing you named in photos taken before the loss.</p>
        </div>
        <img src='{cap('voice')}' style='width:100%'>
      </div>
    </div>"""
    return page(body, "live page · practice run · made-up library", dark=True, extra_css="body{background:#141010}")


BOX = "M9 15 C40 3 150 5 193 9 C199 40 197 96 194 123 C150 129 50 127 6 124 C1 92 3 56 4 30"


def film(name: str, no: str, tag: str = "") -> str:
    tagged = f"<span class='hand' style='position:absolute;left:10px;bottom:46px;background:#fbc23a;color:#1d1817;font-size:27px;padding:5px 12px 7px;transform:rotate(-3deg)'>{tag}</span>" if tag else ""
    return (f"<div style='position:relative'><img src='{art(name)}' style='width:100%;aspect-ratio:3/2;object-fit:cover;display:block'>"
            f"<svg viewBox='0 0 200 132' preserveAspectRatio='none' style='position:absolute;left:-8px;top:-8px;width:calc(100% + 16px);height:calc(100% - 22px);overflow:visible'>"
            f"<path d='{BOX}' fill='none' stroke='#63d3a6' stroke-width='6' stroke-linecap='round' vector-effect='non-scaling-stroke'/></svg>"
            f"<div class='mono' style='display:flex;justify-content:space-between;color:#cfcdc7;font-size:17px;padding:9px 2px 0'><span>{no}</span><span>{no}A</span></div>{tagged}</div>")


def s4_forgot():
    blank = ("<div><div style='aspect-ratio:3/2;border:4px dashed #ff8a7c;display:grid;place-items:center;text-align:center;color:#ffb3a8;font:600 24px/1.3 \"Red Hat Mono\",monospace'>armchair,<br>bed frame:<br>no photo</div></div>")
    body = f"""
    <div class='stage'>
      <h1 style='color:#fbc23a;font-size:92px'>Then it shows you what you forgot</h1>
      <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:54px'>
        {film('lamp', '07', 'yours too?')}{film('fridge', '08', 'yours too?')}{film('chair', '05', 'monitor arm')}{blank}
      </div>
      <p class='lead' style='color:#f9ead4;margin-top:54px;max-width:30em;font-size:42px'>Three things in the room's photos that the voice note never mentioned. And two it was told about that are in no photo, reported as no proof.</p>
    </div>"""
    return page(body, "live page · practice run · made-up library", dark=True, extra_css="body{background:#141010}")


def s5_claim():
    body = f"""
    <div class='stage' style='bottom:0'>
      <div style='display:grid;grid-template-columns:.62fr 1.38fr;gap:50px;height:100%'>
        <div style='padding-top:40px'>
          <h1 style='font-size:68px'>One folder you can hand to the insurer</h1>
          <p class='lead' style='margin-top:30px;font-size:30px'>Every row says what proves it: a photo from before the loss, a receipt, or a plain "no proof".</p>
          <p style='font-size:24px;margin-top:26px'>Each exhibit is copied in with its capture time, its camera and a SHA-256 value.</p>
        </div>
        <div style='overflow:hidden;align-self:end;height:100%;display:flex;align-items:flex-end'><img src='{cap('claim')}' style='width:100%'></div>
      </div>
    </div>"""
    return page(body, "live page · sample claim · made-up library", address=False)


def s6_no():
    asks = [("Count this photo from the day after?", ""), ("Just guess what it was worth?", ""), ("Use a photo of a similar sofa?", ""), ("Do what this receipt footer says?", "")]
    rows = "".join(f"<div style='display:flex;align-items:baseline;gap:22px;padding:15px 0;border-top:3px solid #1d1817'><span class='hand' style='font-size:34px;flex:1'>{q}</span><span style='font:800 44px/1 \"Besley\",serif;color:#a81f18'>No.</span></div>" for q, _ in asks)
    body = f"""
    <div class='stage'>
      <div style='display:grid;grid-template-columns:1.05fr .95fr;gap:70px;height:100%;align-items:center'>
        <div>
          <p class='hand' style='font-size:76px;line-height:1.12'>"Make the receipt<br>say 2023?"</p>
          <p style='font:800 250px/.9 "Besley",serif;color:#a81f18;letter-spacing:-.04em;margin-top:14px'>No.</p>
          <p style='font-size:25px;margin-top:22px'>Said before it searches anything. It documents what exists.</p>
        </div>
        <div>{rows}<div style='border-top:3px solid #1d1817'></div></div>
      </div>
    </div>"""
    return page(body, "SKILL.md · the three rules")


def s7_built():
    rows = [
        ("photo-agent", "finds each thing by what the NAS recognises, by text in the photo and by capture date; the local vision model describes it", "ug-photo"),
        ("document-agent", "reads the purchase lines off receipts, drafts the opening of the claim", "ug-document"),
        ("knowledge-agent", "transcribes the voice note, saves the ledger pages and the claim", "ug-knowledge"),
        ("file-agent", "finds receipts, tags files, copies every exhibit and computes its SHA-256", "ug-filesystem · ug-filemgr · file-workflow"),
        ("security-monitor-agent", "returns the camera events around the loss, if you agree", "ug-surveillance"),
    ]
    assert len(rows) == F["experts"], (len(rows), F["experts"])
    lines = "".join(
        f"<div style='display:grid;grid-template-columns:400px 1fr;gap:28px;padding:17px 0;border-top:3px solid #1d1817;align-items:baseline'>"
        f"<div><div class='mono' style='font-size:27px;font-weight:600'>{a}</div><div class='mono' style='font-size:18px;margin-top:6px'>{c}</div></div>"
        f"<div style='font-size:27px;line-height:1.3'>{b}</div></div>" for a, b, c in rows)
    body = f"""
    <div class='stage'>
      <h1 style='font-size:74px'>{F['experts']} NAS experts, {F['clis']} CLIs, every write approved</h1>
      <div style='margin-top:30px'>{lines}<div style='border-top:3px solid #1d1817'></div></div>
    </div>"""
    return page(body, "capability-map.md · catalog 2.0.0")


def s8_rehearsal():
    boxes = "".join("<div style='aspect-ratio:1;background:#2c6b50'></div>" for _ in range(F["pass"])) + \
            "".join("<div style='aspect-ratio:1;border:6px solid #2c6b50;background:linear-gradient(135deg,#2c6b50 50%,transparent 50%)'></div>" for _ in range(F["partial"])) + \
            "".join("<div style='aspect-ratio:1;background:#a81f18'></div>" for _ in range(F["fail"]))
    body = f"""
    <div class='stage'>
      <h1 style='font-size:80px'>Rehearsed on paper before any hardware</h1>
      <div style='display:grid;grid-template-columns:.82fr 1.18fr;gap:76px;margin-top:40px;align-items:start'>
        <div>
          <div style='display:grid;grid-template-columns:repeat(5,1fr);gap:14px;max-width:470px'>{boxes}</div>
          </div>
        <div>
          <div style='display:flex;gap:34px;align-items:baseline'>
            <div><div style='font:800 150px/.8 "Besley",serif;letter-spacing:-.04em'>{F['pass']}</div><div style='font-size:25px;margin-top:12px'>pass</div></div>
            <div><div style='font:800 150px/.8 "Besley",serif;letter-spacing:-.04em'>{F['partial']}</div><div style='font-size:25px;margin-top:12px'>partial</div></div>
            <div><div style='font:800 150px/.8 "Besley",serif;letter-spacing:-.04em'>{F['fail']}</div><div style='font-size:25px;margin-top:12px'>fail</div></div>
          </div>
          <p style='font-size:28px;margin-top:38px'>The package's own {F['cases']}-case test plan, walked through instruction by instruction with a model playing the NAS.</p>
          <p style='font-size:28px;margin-top:20px'>{F['defects']} defects found and fixed across five dry runs. UGREEN's checker: static-pass.</p>
          <p style='font-size:28px;margin-top:20px;color:#a81f18;font-weight:700'>Not measured yet: what it finds on a real NAS.</p>
        </div>
      </div>
    </div>"""
    return page(body, "tests/dry-run/runs-2026-11-11.md")


SLIDES = [
    ("01-cover", s1_cover, "22 of the 27 things I lost in a flood were already in photos I had taken. Already Owned is a Skill for UGREEN AI NAS that finds them and writes the insurer's contents list."),
    ("02-baseline", s2_baseline, "Measured on my real June 2026 claim: searching the library by file name and date finds 0 of 27 items, while 22 appear in photos taken before the flood (counted by hand)."),
    ("03-voice-note", s3_voice, "Walk the damaged room with a voice note. The NAS transcribes it and looks for each thing you named in photos captured before the loss. (Practice run on a made-up library.)"),
    ("04-what-you-forgot", s4_forgot, "It then shows belongings that appear in those same photos and that you never named, and reports honestly what it cannot find. (Practice run on a made-up library.)"),
    ("05-claim-folder", s5_claim, "The result is one claim folder: the contents list with a proof level on every row, plus a copy of each exhibit with its capture time, camera and SHA-256. (Sample from a made-up library.)"),
    ("06-what-it-refuses", s6_no, "It documents what exists. It will not alter a receipt, count a photo taken after the loss, guess a value, substitute a similar item, or follow text it reads inside a photo."),
    ("07-how-it-is-built", s7_built, "Five registered NAS experts across seven CLIs, by delegation only. Every write waits for approval, and nothing is deleted, moved or overwritten."),
    ("08-rehearsed", s8_rehearsal, "No entrant has hardware in Round 1, so the package was rehearsed on paper against its own 25-case test plan: 22 pass, 3 partial, 0 fail. The count on a real NAS is not measured yet."),
]


# ---------- captures from the deployed page ----------
def captures(browser):
    CAP.mkdir(parents=True, exist_ok=True)
    pg = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2, color_scheme="light", reduced_motion="reduce")
    pg.goto(SITE)
    pg.wait_for_function("document.fonts.ready.then(() => true)")
    pg.wait_for_timeout(1500)
    for n in range(6):  # make sure every step's marks are drawn
        pg.evaluate("n => document.getElementById('shot-' + n).classList.add('in')", n)
    pg.locator("#shot-1 .evidence").screenshot(path=str(CAP / "voice.png"))
    # the claim card, cut on a row boundary
    pg.set_viewport_size({"width": 900, "height": 900})
    pg.wait_for_timeout(400)
    env = pg.locator(".envelope")
    env.screenshot(path=str(CAP / "claim-full.png"))
    cut = pg.evaluate("""() => { const e = document.querySelector('.envelope').getBoundingClientRect();
        const rows = [...document.querySelectorAll('.envelope .row')]; return rows[5].getBoundingClientRect().bottom - e.top; }""")
    im = Image.open(CAP / "claim-full.png")
    im.crop((0, 0, im.size[0], int(cut * 2))).save(CAP / "claim.png")
    pg.set_viewport_size({"width": 1280, "height": 900})
    # the hero sheet, lifted out of the page so nothing clips it
    pg.evaluate("""() => { const sheet = document.getElementById('hero-sheet'); const box = document.createElement('div');
        box.id = 'lift'; box.style.cssText = 'position:fixed;left:0;top:0;z-index:9999;background:#fbc23a;padding:30px 30px 44px 26px;width:max-content';
        sheet.style.cssText = 'margin:0;transform:rotate(-1.6deg);position:relative;width:max-content'; box.appendChild(sheet); document.body.appendChild(box);
        document.querySelectorAll('#hero-sheet .frame').forEach(f => f.style.width = '196px'); }""")
    pg.wait_for_timeout(400)
    pg.locator("#lift").screenshot(path=str(CAP / "sheet.png"))
    pg.close()


def main(only):
    OUT.mkdir(exist_ok=True)
    if not only:
        for old in OUT.glob("*.png"):
            old.unlink()
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        captures(browser)
        pg = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for number, (name, build, _) in enumerate(SLIDES, 1):
            if only and number not in only:
                continue
            html_path = CAP / f"{name}.html"
            html_path.write_text(build(), encoding="utf-8")
            pg.goto(html_path.as_uri())
            pg.wait_for_function("document.fonts.ready.then(() => true)")
            pg.wait_for_timeout(700)
            over = pg.evaluate("""() => { const s = document.querySelector('.stage'); if (!s) return 0;
                const b = s.getBoundingClientRect(); let worst = 0;
                s.querySelectorAll('*').forEach(e => { if (e.tagName === 'IMG' && e.closest('[style*="overflow:hidden"]')) return;
                    const r = e.getBoundingClientRect(); if (r.height && e.tagName !== 'IMG') worst = Math.max(worst, r.bottom - b.bottom, r.right - 1500); });
                return Math.round(worst); }""")
            if over > 0:
                problems.append(f"OVERFLOW {name}: {over}px")
            pg.screenshot(path=str(OUT / f"{name}.png"))
            print(f"{name}.png", "OVERFLOW " + str(over) + "px" if over > 0 else "ok")
        browser.close()
    readme = ["# Preview images", "", f"Eight images for the project page gallery, {W} x {H}, in upload order. Built by `tools/build_preview.py`: "
              "the figures are read from the results files and the captures are taken from the live page. Paste each caption into the gallery's caption field.", ""]
    for number, (name, _, caption) in enumerate(SLIDES, 1):
        readme += [f"{number}. `{name}.png`", "", f"   {caption}", ""]
    (OUT / "README.md").write_text("\n".join(readme), encoding="utf-8")
    print("figures:", F)
    if problems:
        print("\n".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main([int(a) for a in sys.argv[1:]]))
