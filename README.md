# BPUSFOODTEAM — GitHub Pages site

A three-level resource hub: **BPUSFOODTEAM (home) → Banner → Category**, with a downloadable file list and a unique web address + QR code for every page.

## Structure

```
index.html                     BPUSFOODTEAM home (3 banner tiles)
thorntons/ ampm/ ta/           Banner pages (6 category tiles each)
  hot-dispensed/ frozen-dispensed/ cold-dispensed/
  bakery/ roller-grill/ hot-food/      Category pages (file lists)
files/<banner>/<category>/     <-- DROP YOUR FILES HERE
qr-codes/                      PNG QR code for every page
links.csv                      Every web address + matching QR file
assets/style.css               Styling
build.py                       Regenerates all pages, QR codes, links.csv
```

## One-time setup

1. **Create the repo.** On GitHub: *New repository* → name it `bpusfoodteam` → Public (required for free Pages) → Create.
2. **Upload.** Unzip this folder and drag **the contents** (not the outer folder) into the repo via *Add file → Upload files* → Commit.
3. **Turn on Pages.** Repo → *Settings* → *Pages* → Source: **Deploy from a branch** → Branch: **main**, Folder: **/ (root)** → Save. The site is live in ~2 minutes at `https://<org-or-username>.github.io/bpusfoodteam/`.
4. **Set the real URL.** Open `build.py`, change the `SITE_URL` line to your live address, then re-run `python build.py`. This is what makes the QR codes point to the right place.
5. **Re-upload** `links.csv` and the `qr-codes/` folder after that rebuild.

## Adding or updating files

1. Put the file in `files/<banner>/<category>/` — e.g. `files/thorntons/roller-grill/Crispy-Roller-Grill-Guide.pdf`.
2. Run `python build.py` (this rewrites the category page so the new file is listed).
3. Commit/upload the changed files.

**No-code alternative:** you can upload straight through the GitHub website into the `files/...` folder, but you'll need to add the link line to that category's `index.html` manually. Running `build.py` does it for you.

Web addresses and QR codes **never change** when you swap files — the QR code is tied to the category page, not the document. Print once, update the contents as often as you like.

## QR codes

`links.csv` pairs every page with its QR image, ready to drop into labels, WorkJam posts, or equipment signage. All 22 codes (1 home + 3 banner + 18 category) are pre-generated in `qr-codes/`.

## Notes

- Keep file names short and descriptive — they appear verbatim on the page.
- PDF is the safest format for site-facing docs; it opens in-browser on tablets.
- `.nojekyll` is included so folders/files starting with `_` aren't ignored.
- If a page 404s, confirm the folder contains an `index.html` and that Pages is set to root.
