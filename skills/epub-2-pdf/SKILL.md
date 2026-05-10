---
name: epub-2-pdf
description: Use when Codex needs to convert EPUB ebooks to PDF from the CLI, especially with Calibre ebook-convert, readable page layout, Chinese fonts, page numbers, visible PDF table of contents, or controlled PDF outline/bookmarks.
---

# EPUB to PDF

## Overview

Convert EPUB files to readable PDFs with Calibre. Prefer `ebook-convert`; use this skill when the user wants a PDF file, specific paper size/margins/fonts, page numbers, or a usable table of contents/bookmarks.

## Workflow

1. Locate the EPUB and choose an output filename in the same directory unless the user specifies otherwise.
2. Find Calibre:
   - Prefer `ebook-convert` from `PATH`.
   - On macOS, also check `/Applications/calibre.app/Contents/MacOS/ebook-convert`.
3. Inspect the EPUB TOC before choosing TOC flags:
   - `unzip -p "$epub" '*/toc.ncx'` or list with `unzip -l`.
   - If `toc.ncx` is shallow but HTML headings contain useful structure, use auto TOC.
4. Convert with A4 defaults unless the user requested another format.
5. Verify with `file`, `ls -lh`, and `pypdf` if available: page count, outline count, and a sample of final TOC pages.

## Command Builder

Use `scripts/build_ebook_convert_cmd.py` to generate a robust command instead of retyping fragile quoting:

```bash
python3 /Users/lkc/.codex/skills/epub-2-pdf/scripts/build_ebook_convert_cmd.py \
  input.epub output.pdf --toc concise
```

TOC modes:

- `source`: use EPUB's built-in TOC only.
- `visible`: source TOC plus `--pdf-add-toc`.
- `detailed`: force `h1/h2/h3`; useful but may include chapter summaries.
- `medium`: force `h1/h2` only.
- `concise`: force `h1` plus `h2` entries that do not start with digits; good for "卷/部/上下卷" without chapter summaries.

Run the printed command after reviewing it.

## Recommended Defaults

For Chinese novels:

```bash
--paper-size a4
--pdf-page-margin-left 36
--pdf-page-margin-right 36
--pdf-page-margin-top 48
--pdf-page-margin-bottom 48
--pdf-page-numbers
--pdf-serif-family "Songti SC"
```

If Calibre fails with permission errors writing `~/Library/Preferences/calibre`, rerun the same `ebook-convert` command with the required sandbox approval.

## TOC Heuristics

Avoid blindly using `h3`: many EPUBs put "chapter number + plot summary" in `h3`, which creates unusably long PDF bookmarks. If the user complains that the directory includes content summaries, regenerate with `--toc concise`.

For visible TOC pages, add:

```bash
--pdf-add-toc --toc-title "目录"
```

Calibre appends the visible TOC near the end of the PDF. PDF sidebars use the PDF outline/bookmarks.

## Verification

Use this Python snippet when `pypdf` is installed:

```bash
python3 - <<'PY'
from pypdf import PdfReader

r = PdfReader("output.pdf")

def flatten(items):
    out = []
    for item in items:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

items = flatten(r.outline)
print("pages", len(r.pages))
print("outline", len(items))
print([x.get("/Title", "") for x in items[:20]])
PY
```

Report the output path, size, pages, outline count, and any caveats.
