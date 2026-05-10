---
name: upload-books-to-notebooklm
description: Use when Codex needs to batch upload local book files, PDFs, or numbered book series into Google NotebookLM notebooks, especially when notebook titles must be clean book names like 《书名》 and multi-volume files must be grouped together.
---

# Upload Books To NotebookLM

## Overview

Batch local books into NotebookLM with clean notebook names and series-aware grouping. Use the bundled planner first, then create notebooks and upload sources with explicit notebook IDs.

## Workflow

1. Locate the input directory. If the user says files were moved, honor that path; common examples include `../已上传` or an explicit archive folder.
2. Verify NotebookLM is usable:

```bash
notebooklm status
notebooklm list --json
```

`notebooklm status` may exit 0 even when no notebook is selected, so the real gate is `notebooklm list --json`: it must exit 0 and return a `notebooks` array. If it fails with `AUTH_REQUIRED`, `CSRF token not found`, or a final URL like `https://notebooklm.google?location=unsupported`, stop before creating notebooks, run `notebooklm auth check --test`, and have the user refresh login/network access. Do not continue bulk creation when token fetch is failing; it can leave partially-created empty notebooks.

If the standalone `notebooklm` skill is available, load it for CLI command details and authentication troubleshooting.

3. Preview grouping before upload:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/upload-books-to-notebooklm/scripts/upload_books_to_notebooklm.py" --input "<book-dir>" --json
```

Check that:

- Notebook titles are exactly `《书名》`.
- Authors, edition notes, scan/watermark notes, and bracket metadata are not in notebook titles.
- Numbered volumes such as `毛泽东传 01`, `毛泽东传 02` are one notebook.
- A single file containing multiple volumes, such as `[全四册]`, remains one source in one notebook.

4. Execute only after the plan matches the request:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/upload-books-to-notebooklm/scripts/upload_books_to_notebooklm.py" --input "<book-dir>" --execute --wait-ready
```

The script creates new notebooks, uploads sequentially, uses explicit `-n <notebook_id>` source targets, and reports source statuses.

5. Run a fresh final verification. For every created notebook, `notebooklm source list -n <id> --json` must show the expected source count and all sources `ready` before claiming completion.

## Naming Rules

- Always wrap notebook titles in Chinese book brackets: `《...》`.
- Strip author suffixes after separators like ` - `, ` – `, or ` — `.
- Strip square-bracket metadata like `[扫描版]`, `[有目录]`, `[2024新版]`, `[公开版]`.
- Strip trailing Arabic volume numbers only when separated from the title, such as ` 01`, ` 02`, ` 12`.
- Do not strip numbers that are part of the title, such as `2025总结` or `1878-1928`.

## Failure Handling

If a source uploads but NotebookLM reports `error`, investigate the file before retrying:

- Check whether the PDF is encrypted, malformed, or has broken content streams.
- If a PDF is structurally bad but text extraction works, extract page text into several `.txt` parts and upload those parts to the same notebook.
- Delete failed sources only after replacement sources are uploaded and `ready`; never delete a `ready` source unless the user explicitly asks.
- Keep the original notebook title unchanged even when using text fallback parts.

When retrying or resuming after partial failures:

- Re-list notebooks and sources first; reuse existing notebooks by exact title instead of blindly creating new notebooks.
- Before every `source add`, run `notebooklm source list -n <notebook_id> --json` and skip files whose source title already matches the original filename or stem. This prevents duplicate uploads when a previous attempt timed out or was interrupted.
- `notebooklm source add` can return errors such as `Server disconnected without sending a response` even though NotebookLM accepted the upload and created a `preparing` source. After any upload error, immediately list sources for that notebook and treat a matching source as accepted rather than retrying and duplicating it.
- Do not upload probe/test files into a real target notebook. If testing whether uploads work, create a disposable notebook or use an intentionally disposable source, then clean it up only with user confirmation.
- If the user explicitly says not to wait for processing, create/reuse notebooks and submit missing sources, but do not call `source wait` or require `ready`; report submitted, skipped-existing, and failed counts from JSONL logs.

## Script Notes

`scripts/upload_books_to_notebooklm.py` supports:

- `--input DIR`: directory to scan.
- `--recursive`: include subdirectories.
- `--json`: emit a machine-readable dry-run plan.
- `--execute`: create notebooks and upload files.
- `--wait-ready`: poll source statuses after upload.

Supported default source file extensions are `.pdf`, `.txt`, `.md`, and `.docx`. Convert EPUB or unsupported image-only material before using this workflow.
