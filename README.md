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

## Installing these skills into Hermes

Install the complete skill directories so supporting `references/`, `scripts/`, `templates/`, and `assets/` files are preserved. From a clone of this repository:

```bash
git clone https://github.com/xdlkc/notebooklm-workflow.git
cd notebooklm-workflow
mkdir -p "$HOME/.hermes/skills"
rsync -a --delete \
  --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "skills/" "$HOME/.hermes/skills/"
```

To install into a named Hermes profile, copy into that profile's skills directory instead of the default `~/.hermes/skills` path, for example:

```bash
PROFILE_SKILLS="$HOME/.hermes/profiles/notebooklm/skills"
mkdir -p "$PROFILE_SKILLS"
rsync -a --delete \
  --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "skills/" "$PROFILE_SKILLS/"
```

Start a fresh Hermes session after installing or updating skills so the new skill index is loaded.

## Syncing local skills and this repository

Use `rsync --delete` so renames and removed files stay in sync. Review `git diff` before committing and do not sync auth stores, cookies, tokens, generated private artifacts, or cache files.

Local default-profile skills path:

```bash
LOCAL_SKILLS="$HOME/.hermes/skills"
REPO="$HOME/Code/notebooklm-workflow"
```

Local skills updated → update the repository copy:

```bash
rsync -a --delete \
  --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "$LOCAL_SKILLS/notebooklm/" "$REPO/skills/notebooklm/"
rsync -a --delete --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "$LOCAL_SKILLS/blog-2-notebooklm/" "$REPO/skills/blog-2-notebooklm/"
rsync -a --delete --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "$LOCAL_SKILLS/upload-books-to-notebooklm/" "$REPO/skills/upload-books-to-notebooklm/"
rsync -a --delete --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "$LOCAL_SKILLS/epub-2-pdf/" "$REPO/skills/epub-2-pdf/"
rsync -a --delete --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "$LOCAL_SKILLS/zlibrary-cli/" "$REPO/skills/zlibrary-cli/"

cd "$REPO"
git diff --stat
git diff -- README.md skills/
```

Remote/repository updated → update local Hermes skills:

```bash
cd "$REPO"
git pull --ff-only
rsync -a --delete \
  --exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store' \
  "skills/" "$LOCAL_SKILLS/"
```

If you only want one skill, sync that skill directory instead of the whole `skills/` tree.

## Required tools

These skills are meant to be used by Hermes/Codex-style agents, but several workflows also require local CLIs or apps. Install only the tools needed for the workflow you plan to run.

| Tool | Required by | Purpose | Install / setup |
|---|---|---|---|
| `python3` | all helper scripts | Run repository scripts and validation helpers. | Usually preinstalled on macOS/Linux. |
| `uv` | validation and Python deps | Run Python snippets with temporary packages such as `pyyaml` or `pypdf`. Optional but recommended. | `brew install uv` or see https://docs.astral.sh/uv/ |
| `notebooklm` | `notebooklm`, `blog-2-notebooklm`, `upload-books-to-notebooklm`, NotebookLM artifact workflows | Create/list notebooks, add sources, generate/download artifacts. | `pip install notebooklm-py`; then run `notebooklm login` and verify with `notebooklm list --json`. |
| Playwright/Chromium | `notebooklm` auth and browser-backed operations | Browser automation and Google auth/session capture used by `notebooklm-py`. | Usually installed by the NotebookLM CLI when needed; if not, run `python -m playwright install chromium` in the same Python environment. |
| `ebook-convert` / Calibre | `epub-2-pdf` | Convert EPUB books to readable PDFs with Chinese fonts, page numbers, and PDF TOC/bookmarks. | Install Calibre. On macOS the binary is usually `/Applications/calibre.app/Contents/MacOS/ebook-convert`. |
| `zlib` | `zlibrary-cli` | Search/download authorized Z-Library books and manage `~/.config/zlib/session.json`. | `brew install heartleo/tap/zlib`; then run `zlib login` and verify with `zlib profile`. |
| Go 1.25+ | `zlibrary-cli/scripts/noninteractive_download.go` | Non-interactive fallback when `zlib download` fails in a non-TTY agent session. | `brew install go` or let `go run` download the requested toolchain if supported. |
| `gws` | `notebooklm-artifacts-to-drive`, book PPT delivery fallback | Upload generated artifacts to Google Drive and create share links. | Install/configure the Google Workspace CLI, then run `gws auth login --services drive` and verify with `gws auth status`. |
| PowerPoint tooling / `python-pptx` | `notebooklm-book-ppt-workflow`, `notebooklm-rich-slide-decks` when rebuilding `.pptx` | Create or QA dense book-sharing PPTX decks. | Use the agent's `powerpoint` skill/tooling; for local Python workflows install `python-pptx` as needed. |
| `unzip`, `file` | `epub-2-pdf`, PPTX QA | Inspect EPUB/PPTX archives and verify output file types. | Usually preinstalled; on macOS available via system tools. |
| `pypdf` | `epub-2-pdf` verification | Verify PDF page count, outline/bookmarks, and visible TOC pages. | `uv run --with pypdf python ...` or `pip install pypdf`. |

Recommended environment variables:

```bash
# Use the authenticated NotebookLM profile expected by these workflows.
export NOTEBOOKLM_HOME="$HOME/.notebooklm/profiles/default"

# Optional: override Z-Library domain/proxy when needed.
export ZLIB_DOMAIN="https://z-lib.sk"
# export ZLIB_PROXY="http://127.0.0.1:7890"
```

Quick readiness checks:

```bash
python3 --version
notebooklm list --json
zlib profile
/Applications/calibre.app/Contents/MacOS/ebook-convert --version 2>/dev/null || ebook-convert --version
gws auth status   # only needed for Google Drive artifact delivery
```

## Safety notes

- Do not commit NotebookLM auth storage, Z-Library sessions, cookies, OAuth tokens, browser profiles, Google Drive credentials, or generated private artifacts.
- `zlibrary-cli` should only be used for public-domain, open-license, owned, or otherwise authorized books. Do not use these workflows to bypass CAPTCHA, access controls, quotas, or copyright restrictions.
- Scripts and skills may reference local paths as examples; verify them before running on another machine.
- Keep generated outputs under a separate work directory unless they are intentionally reusable.

## Quick validation

For Hermes skills, validate individual skill folders with the local skill validator, for example:

```bash
SKILL_VALIDATOR=${SKILL_VALIDATOR:-$HOME/.hermes/skills/skill-creator/scripts/quick_validate.py}
python3 "$SKILL_VALIDATOR" skills/notebooklm
```

If the validator environment lacks PyYAML, run with uv:

```bash
SKILL_VALIDATOR=${SKILL_VALIDATOR:-$HOME/.hermes/skills/skill-creator/scripts/quick_validate.py}
uv run --with pyyaml python "$SKILL_VALIDATOR" skills/notebooklm
```
