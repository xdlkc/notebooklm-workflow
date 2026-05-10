# NotebookLM Workflow

Collected NotebookLM workflow assets for Hermes/Codex agents.

This repository mirrors the reusable workflow skills used locally for NotebookLM automation and artifact generation.

## Contents

- `skills/notebooklm/` — core NotebookLM CLI/API skill plus specialized sub-skills:
  - `notebooklm-book-ppt-workflow`
  - `notebooklm-rich-slide-decks`
  - `notebooklm-studio-quality-prompts`
  - `notebooklm-artifacts-to-drive`
- `skills/blog-2-notebooklm/` — import blog/article URLs into Google NotebookLM.
- `skills/upload-books-to-notebooklm/` — batch upload local book files/PDFs to NotebookLM.
- `skills/epub-2-pdf/` — convert EPUB ebooks to readable PDFs with Calibre/ebook-convert.
- `skills/zlibrary-cli/` — use and troubleshoot the `heartleo/zlib` Z-Library CLI, including login/session handling, search/download commands, and a non-interactive download helper.

## Safety notes

- Do not commit NotebookLM auth storage, cookies, OAuth tokens, browser profiles, or generated private artifacts.
- Scripts and skills may reference local paths as examples; verify them before running on another machine.
- Keep generated outputs under a separate work directory unless they are intentionally reusable.

## Quick validation

For Hermes skills, validate individual skill folders with the local skill validator, for example:

```bash
python3 /Users/lkc/.hermes/skills/skill-creator/scripts/quick_validate.py skills/notebooklm
```

If the validator environment lacks PyYAML, run with uv:

```bash
uv run --with pyyaml python /Users/lkc/.hermes/skills/skill-creator/scripts/quick_validate.py skills/notebooklm
```
