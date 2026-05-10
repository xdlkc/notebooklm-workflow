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

## Demo / Best-practice example

See [`demos/sapiens/`](demos/sapiens/) for a complete best-practice example using a 《人类简史》 NotebookLM notebook as the target output shape. It includes:

- a reproducible NotebookLM CLI workflow for creating a book notebook and generating Studio artifacts;
- prompt files for slide deck, study guide/report, mind map, infographic, data table, quiz, flashcards, audio, and video;
- real Drive-delivered prompt logs plus a final infographic PNG committed under `demos/sapiens/drive_outputs/`;
- a Drive artifact manifest linking to the larger PPTX/PDF/MP4 outputs without bloating git history;
- lightweight SVG mock screenshots showing the desired artifact gallery, dense slide style, and Chinese infographic quality target;
- a QA checklist for source grounding, Chinese visual text, PPTX validation, and long-running artifact handoff.

Preview:

![Sapiens final NotebookLM infographic](demos/sapiens/drive_outputs/sapiens_infographic_final.png)

Full artifact index:

- [`demos/sapiens/drive_outputs/README.md`](demos/sapiens/drive_outputs/README.md)

> The demo does not commit the book PDF, private auth data, or large video/PPT binaries. Use your own legally available source inside NotebookLM.

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

These skills are written for Hermes/Codex-style agents. Install the common tools first, then add only the workflow-specific tools you actually need.

### Common baseline

| Tool | Required for | Install / setup | Verify |
|---|---|---|---|
| `python3` | Helper scripts and validators. | Usually preinstalled on macOS/Linux. | `python3 --version` |
| `uv` | Optional but recommended for one-off Python deps such as `pyyaml` and `pypdf`. | `brew install uv` or see https://docs.astral.sh/uv/ | `uv --version` |
| `rsync` | Installing and syncing skill directories. | Usually preinstalled on macOS/Linux. | `rsync --version` |

### NotebookLM workflows

Needed by `skills/notebooklm/`, `skills/blog-2-notebooklm/`, `skills/upload-books-to-notebooklm/`, and the NotebookLM artifact/PPT workflows.

| Tool | Purpose | Install / setup | Verify |
|---|---|---|---|
| `notebooklm` | Create/list notebooks, add sources, generate/download NotebookLM artifacts. | `pip install notebooklm-py`; then run `notebooklm login`. | `notebooklm list --json` |
| Playwright/Chromium | Browser automation and Google auth/session capture used by `notebooklm-py`. | Usually installed by the NotebookLM CLI when needed. If not: `python -m playwright install chromium` in the same Python environment. | `python -m playwright --version` |
| `gws` | Upload generated artifacts to Google Drive and create share links. Required by `notebooklm-artifacts-to-drive` and Drive delivery fallbacks. | Install/configure the Google Workspace CLI, then run `gws auth login --services drive`. | `gws auth status` |
| PowerPoint tooling / `python-pptx` | Create, rebuild, or QA dense `.pptx` decks for book-sharing and rich slide workflows. | Use the agent's `powerpoint` skill/tooling; for local Python workflows install `python-pptx` as needed. | `python3 -c "import pptx; print('python-pptx ok')"` |
| `unzip`, `file` | Inspect PPTX archives and verify output file types. | Usually preinstalled; on macOS available via system tools. | `unzip -v`, `file --version` |

Recommended environment variable for NotebookLM:

```bash
export NOTEBOOKLM_HOME="$HOME/.notebooklm/profiles/default"
```

### EPUB/PDF workflows

Needed by `skills/epub-2-pdf/` and PDF/PPT verification steps.

| Tool | Purpose | Install / setup | Verify |
|---|---|---|---|
| `ebook-convert` / Calibre | Convert EPUB books to readable PDFs with Chinese fonts, page numbers, and PDF TOC/bookmarks. | Install Calibre. On macOS the binary is usually `/Applications/calibre.app/Contents/MacOS/ebook-convert`. | `/Applications/calibre.app/Contents/MacOS/ebook-convert --version 2>/dev/null || ebook-convert --version` |
| `pypdf` | Verify PDF page count, outline/bookmarks, and visible TOC pages. | `uv run --with pypdf python ...` or `pip install pypdf`. | `uv run --with pypdf python -c "import pypdf; print('pypdf ok')"` |
| `unzip`, `file` | Inspect EPUB/PPTX archives and verify output file types. | Usually preinstalled; on macOS available via system tools. | `unzip -v`, `file --version` |

### Z-Library workflows

Needed only by `skills/zlibrary-cli/`.

| Tool | Purpose | Install / setup | Verify |
|---|---|---|---|
| `zlib` | Search/download authorized Z-Library books and manage the active `~/.config/zlib/session.json`. | `brew install heartleo/tap/zlib`; then run `zlib login`. | `zlib profile` |
| Go 1.25+ | Run `zlibrary-cli/scripts/noninteractive_download.go`, the non-interactive fallback when `zlib download` fails in non-TTY agent sessions. | `brew install go`, or let `go run` download the requested toolchain if supported. | `go version` |
| `skills/zlibrary-cli/scripts/zlib_account.py` | Optional helper for explicit multi-account session switching. Stores named session copies under `~/.config/zlib/accounts/`; it does not auto-rotate accounts to bypass quotas. | Included in this repository. Use after `zlib login`. | `python3 skills/zlibrary-cli/scripts/zlib_account.py list` |

Optional Z-Library environment variables:

```bash
export ZLIB_DOMAIN="https://z-lib.sk"
# export ZLIB_PROXY="http://127.0.0.1:7890"
```

### Quick readiness checks

Run only the checks for workflows you intend to use:

```bash
python3 --version
uv --version
notebooklm list --json                         # NotebookLM workflows
python -m playwright --version                 # NotebookLM browser/auth workflows
gws auth status                                # Google Drive delivery
/Applications/calibre.app/Contents/MacOS/ebook-convert --version 2>/dev/null || ebook-convert --version
zlib profile                                   # Z-Library workflow
go version                                     # Z-Library non-interactive fallback
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
