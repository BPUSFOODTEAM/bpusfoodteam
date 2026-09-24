# BPUSFOODTEAM — GitHub Pages site

Live site: **https://bpusfoodteam.github.io/bpusfoodteam/**
Repository: https://github.com/BPUSFOODTEAM/bpusfoodteam

Three levels: **BPUSFOODTEAM (home) → Banner → Category**, with a unique web address + QR code for every page.

## Adding a document

1. In GitHub, click into the banner folder, then the category folder — e.g. `ampm` → `bakery`.
2. **Add file → Upload files**, drag the document in, commit.
3. Done. The document sits in the same folder as that page's `index.html`, and the GitHub Action rebuilds the page so it appears in the list.

There is no separate `files` folder. The folder that holds the page holds the documents.

## Structure

```
index.html                 BPUSFOODTEAM home (3 banner tiles)
thorntons/ ampm/ ta/       Banner pages (6 category tiles each)
  bakery/
    index.html             The Bakery page
    <your documents>       <-- upload here
qr-codes/                  PNG QR code for every page
links.csv                  Every web address + matching QR file
assets/style.css           Styling
build.py                   Regenerates pages, QR codes, links.csv
.github/workflows/         Runs build.py automatically on every upload
```

## Requirements for auto-rebuild

Settings → Actions → General → Workflow permissions → **Read and write permissions** → Save.

## Notes

- File names appear verbatim on the page, so keep them short and descriptive. Spaces are fine.
- PDF is the safest format — it opens in-browser on tablets.
- QR codes are tied to the category page, not the document. Swap documents freely; printed codes keep working.
- `.nojekyll` is included so files starting with `_` are not ignored.
