#!/usr/bin/env python3
"""
BPUSFOODTEAM GitHub Pages builder.

HOW IT WORKS
  Drop documents directly into the category folder, e.g.
      ampm/bakery/1 grill- 1 facing Sept-Oct 2026.pdf
  ...then this script rebuilds that category's index.html so the
  document is listed and downloadable.

  There is no separate "files" folder. The folder that holds the
  page is the folder that holds the documents.

Run:  python build.py
"""

import csv
import html
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
QR = ROOT / "qr-codes"

# ---------------------------------------------------------------- CONFIG ----
# GitHub PAGES address (not the github.com repo address). No trailing slash.
SITE_URL = "https://bpusfoodteam.github.io/bpusfoodteam"

SITE_TITLE = "BPUSFOODTEAM"
SITE_TAGLINE = "Food &amp; Dispensed resource hub"

BANNERS = [
    ("thorntons", "Thorntons"),
    ("ampm", "ampm"),
    ("ta", "TA"),
]

CATEGORIES = [
    ("hot-dispensed", "Hot Dispensed"),
    ("frozen-dispensed", "Frozen Dispensed"),
    ("cold-dispensed", "Cold Dispensed"),
    ("bakery", "Bakery"),
    ("roller-grill", "Roller Grill"),
    ("hot-food", "Hot Food"),
]

ICONS = {
    "hot-dispensed": "&#9749;",
    "frozen-dispensed": "&#127846;",
    "cold-dispensed": "&#129380;",
    "bakery": "&#129360;",
    "roller-grill": "&#127789;",
    "hot-food": "&#127829;",
}

# Never listed as downloadable documents.
SKIP = {"index.html", ".gitkeep", ".DS_Store", "Thumbs.db", ".nojekyll"}

# ------------------------------------------------------------------ CSS -----
CSS = """
:root{
  --green:#009b3a; --green-dark:#00713b; --yellow:#ffde00;
  --ink:#111820; --muted:#5b6770; --line:#e3e7ea; --bg:#f6f8f9;
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink);background:var(--bg);line-height:1.5}
a{color:var(--green-dark);text-decoration:none}
a:hover{text-decoration:underline}
header{background:linear-gradient(135deg,var(--green-dark),var(--green));color:#fff;padding:34px 20px 30px}
header .wrap{max-width:1000px;margin:0 auto}
header h1{margin:0;font-size:2rem;letter-spacing:.5px}
header p{margin:6px 0 0;opacity:.9}
header a{color:#fff}
.bar{height:5px;background:var(--yellow)}
main{max-width:1000px;margin:0 auto;padding:28px 20px 60px}
.crumb{font-size:.85rem;color:var(--muted);margin-bottom:18px}
.crumb a{color:var(--muted)}
h2{font-size:1.15rem;margin:28px 0 12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{display:block;background:#fff;border:1px solid var(--line);border-left:5px solid var(--green);
  border-radius:8px;padding:18px 18px 16px;transition:.15s}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.09);text-decoration:none}
.card .t{font-weight:700;font-size:1.05rem;color:var(--ink)}
.card .s{font-size:.85rem;color:var(--muted);margin-top:4px}
.card .i{font-size:1.5rem;line-height:1}
ul.files{list-style:none;padding:0;margin:0;background:#fff;border:1px solid var(--line);border-radius:8px}
ul.files li{border-bottom:1px solid var(--line)}
ul.files li:last-child{border-bottom:0}
ul.files a{display:flex;justify-content:space-between;gap:12px;padding:14px 18px;align-items:center}
ul.files a:hover{background:#f0f7f2;text-decoration:none}
.name{font-weight:600;word-break:break-word}
.meta{font-size:.78rem;color:var(--muted);white-space:nowrap;text-transform:uppercase}
.empty{background:#fff;border:1px dashed var(--line);border-radius:8px;padding:26px;color:var(--muted);text-align:center}
.qr{background:#fff;border:1px solid var(--line);border-radius:8px;padding:16px;display:flex;
  gap:16px;align-items:center;margin-top:26px;flex-wrap:wrap}
.qr img{width:104px;height:104px}
.qr code{background:var(--bg);padding:3px 7px;border-radius:4px;font-size:.82rem;word-break:break-all}
footer{border-top:1px solid var(--line);padding:22px 20px;text-align:center;color:var(--muted);font-size:.82rem}
"""


def page(title, depth, crumb, body):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header><div class="wrap">
  <h1><a href="{up}index.html">{SITE_TITLE}</a></h1>
  <p>{SITE_TAGLINE}</p>
</div></header>
<div class="bar"></div>
<main>
{crumb}
{body}
</main>
<footer>{SITE_TITLE} &middot; Maintained by the US Food &amp; Dispensed Category team</footer>
</body>
</html>
"""


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def scan(banner, cat):
    """Documents sitting in the category folder alongside index.html."""
    d = ROOT / banner / cat
    d.mkdir(parents=True, exist_ok=True)
    return [p for p in sorted(d.iterdir(), key=lambda x: x.name.lower())
            if p.is_file() and p.name not in SKIP and not p.name.startswith(".")]


def qr_block(url, img_rel):
    return f"""<div class="qr">
  <img src="{img_rel}" alt="QR code">
  <div>
    <div><strong>Scan or share this page</strong></div>
    <code>{html.escape(url)}</code>
  </div>
</div>"""


def build():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(CSS)
    if QR.exists():
        shutil.rmtree(QR)
    QR.mkdir()

    import qrcode

    rows = []
    total_docs = 0

    def make_qr(url, name):
        qrcode.make(url).save(QR / f"{name}.png")

    # ---- home ----
    cards = []
    for slug, label in BANNERS:
        n = sum(len(scan(slug, c)) for c, _ in CATEGORIES)
        cards.append(
            f'<a class="card" href="{slug}/index.html"><div class="t">{label}</div>'
            f'<div class="s">{len(CATEGORIES)} categories &middot; {n} file(s)</div></a>'
        )
    make_qr(f"{SITE_URL}/", "home")
    rows.append(["BPUSFOODTEAM", "Home", f"{SITE_URL}/", "qr-codes/home.png"])
    body = (
        "<h2>Select a banner</h2>"
        f'<div class="grid">{"".join(cards)}</div>'
        + qr_block(f"{SITE_URL}/", "qr-codes/home.png")
    )
    (ROOT / "index.html").write_text(page(SITE_TITLE, 0, "", body))

    # ---- banners + categories ----
    for bslug, blabel in BANNERS:
        bdir = ROOT / bslug
        bdir.mkdir(exist_ok=True)
        cards = []
        for cslug, clabel in CATEGORIES:
            docs = scan(bslug, cslug)
            total_docs += len(docs)
            cards.append(
                f'<a class="card" href="{cslug}/index.html"><div class="i">{ICONS[cslug]}</div>'
                f'<div class="t">{clabel}</div><div class="s">{len(docs)} file(s)</div></a>'
            )

            cdir = bdir / cslug
            cdir.mkdir(exist_ok=True)
            if docs:
                items = "".join(
                    f'<li><a href="{quote(f.name)}">'
                    f'<span class="name">{html.escape(f.name)}</span>'
                    f'<span class="meta">{f.suffix.lstrip(".").upper() or "FILE"} &middot; {human(f.stat().st_size)}</span>'
                    f"</a></li>"
                    for f in docs
                )
                listing = f'<ul class="files">{items}</ul>'
            else:
                listing = (
                    '<div class="empty">No files posted yet.<br>'
                    f"Upload documents into the <code>{bslug}/{cslug}/</code> folder.</div>"
                )
            url = f"{SITE_URL}/{bslug}/{cslug}/"
            qrname = f"{bslug}-{cslug}"
            make_qr(url, qrname)
            rows.append([blabel, clabel, url, f"qr-codes/{qrname}.png"])
            crumb = (
                f'<div class="crumb"><a href="../../index.html">{SITE_TITLE}</a> / '
                f'<a href="../index.html">{blabel}</a> / {clabel}</div>'
            )
            cbody = (
                f"<h2>{blabel} &mdash; {clabel}</h2>{listing}"
                + qr_block(url, f"../../qr-codes/{qrname}.png")
            )
            (cdir / "index.html").write_text(
                page(f"{blabel} | {clabel} | {SITE_TITLE}", 2, crumb, cbody)
            )

        burl = f"{SITE_URL}/{bslug}/"
        make_qr(burl, bslug)
        rows.insert(
            len(rows) - len(CATEGORIES),
            [blabel, "Banner home", burl, f"qr-codes/{bslug}.png"],
        )
        crumb = f'<div class="crumb"><a href="../index.html">{SITE_TITLE}</a> / {blabel}</div>'
        bbody = (
            f"<h2>{blabel} &mdash; categories</h2>"
            f'<div class="grid">{"".join(cards)}</div>'
            + qr_block(burl, f"../qr-codes/{bslug}.png")
        )
        (bdir / "index.html").write_text(
            page(f"{blabel} | {SITE_TITLE}", 1, crumb, bbody)
        )

    with open(ROOT / "links.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Banner", "Category", "Web address", "QR code image"])
        w.writerows(rows)

    (ROOT / ".nojekyll").touch()
    print(f"Built {len(rows)} pages/QR codes. Listed {total_docs} document(s).")
    print(f"Site URL base: {SITE_URL}")


if __name__ == "__main__":
    build()
