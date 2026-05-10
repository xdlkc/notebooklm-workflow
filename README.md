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

## How the skills work together

This repository is organized as a small workflow stack, not as one monolithic skill. Hermes/Codex loads the skill that matches the user request, and that skill then tells the agent which helper skills, CLIs, prompts, and safety checks to use.

| Layer | Skill / directory | Role in the workflow |
|---|---|---|
| Source acquisition | `skills/zlibrary-cli/`, `skills/epub-2-pdf/`, `skills/upload-books-to-notebooklm/`, `skills/blog-2-notebooklm/` | Find or prepare authorized sources, convert EPUB/PDF when needed, and add local files or URLs into NotebookLM. |
| Notebook operations | `skills/notebooklm/` | The core API/CLI wrapper: authenticate, create/list notebooks, add sources, wait for indexing, generate Studio artifacts, download outputs, and inspect artifact status. |
| Book-to-PPT workflow | `skills/notebooklm/notebooklm-book-ppt-workflow/` | A source-grounded book-sharing workflow: extract structure, concepts, cases, timelines, quotes, takeaways, fact-check the script, then generate or build a deck. |
| Studio artifact quality | `skills/notebooklm/notebooklm-studio-quality-prompts/` | Artifact-specific prompts for slide decks, reports, mind maps, infographics, tables, quizzes, flashcards, audio, and video so Studio outputs are not generic. |
| Rich slide/deck QA | `skills/notebooklm/notebooklm-rich-slide-decks/` plus PowerPoint tooling | Guidance for dense, high-information slide decks, PPTX validation, visual QA, and compressed review copies. |
| Delivery / showcase | `skills/notebooklm/notebooklm-artifacts-to-drive/` | Upload originals to Google Drive, create share links, keep large originals out of git, and commit repo-friendly previews/manifest files. |

Typical routing examples:

- “把这本书做成 NotebookLM 笔记本” -> `upload-books-to-notebooklm` + `notebooklm`.
- “把 EPUB 先变 PDF 再上传” -> `epub-2-pdf` -> `upload-books-to-notebooklm` -> `notebooklm`.
- “做一套读书分享 PPT” -> `notebooklm-book-ppt-workflow` -> `notebooklm` -> PowerPoint tooling -> `notebooklm-artifacts-to-drive`.
- “生成所有 Studio 产物” -> `notebooklm-studio-quality-prompts` -> `notebooklm generate ...` -> `notebooklm-artifacts-to-drive`.
- “把产物放进 workflow repo 做 demo” -> `notebooklm-artifacts-to-drive` repo-friendly artifact flow: manifest + compressed copies + README preview images.

## How to run the workflow

### 1. Install/update the skills

Install this repository's `skills/` directory into Hermes, then start a fresh Hermes session so the skill index is reloaded. See [Installing these skills into Hermes](#installing-these-skills-into-hermes) below.

### 2. Verify the runtime tools

At minimum, a NotebookLM workflow usually needs:

```bash
export NOTEBOOKLM_HOME="$HOME/.notebooklm/profiles/default"
notebooklm list --json
gws auth status
```

Optional source-prep workflows may also need:

```bash
zlib profile                                   # only for authorized Z-Library use
/Applications/calibre.app/Contents/MacOS/ebook-convert --version 2>/dev/null || ebook-convert --version
```

### 3. Give the agent a workflow-level request

Use a prompt that names the goal, the source, the artifact types, and delivery expectations. Example:

```text
使用 notebooklm-workflow 的 skills，把这本书做成一个 NotebookLM 读书分享 workflow：
1. 使用我提供的合法 PDF/EPUB 作为来源，不要加入书外知识；
2. 创建或复用 NotebookLM notebook，等待 source ready；
3. 生成：详细 PPT、学习指南、思维导图、信息图、数据表、quiz、flashcards、audio/video overview；
4. 每类 artifact 使用对应的高质量 prompt，保存 prompt log 和 artifact IDs；
5. 原始大文件上传到 Google Drive 的 NotebookLM/<notebook name>/；
6. 如果要放进 repo，只提交 prompt logs、manifest、压缩预览版和 README 截图，不提交书籍 PDF、认证信息或大型原始二进制。
```

### 4. What the agent should do internally

A complete run normally follows this sequence:

```text
Prepare source
  -> optional: zlib search/download, EPUB->PDF conversion, PDF verification
Create/reuse NotebookLM notebook
  -> add source(s), wait until ready
Plan prompts
  -> artifact-specific prompts for PPT/report/map/infographic/table/quiz/flashcards/audio/video
Generate artifacts
  -> save generation JSON/logs and artifact IDs
Download completed artifacts
  -> PPTX/PDF/PNG/CSV/MD/JSON/MP4/MP3 as available
QA and package
  -> source-grounding check, PPTX archive check, visual/text checks, file-size check
Deliver
  -> original full-quality files to Drive; compressed copies/previews to repo when needed
Document
  -> README/demo manifest with links, prompts, screenshots, and reproduction notes
```

For book-sharing PPTs, `notebooklm-book-ppt-workflow` adds an audit trail before deck generation:

```text
00_source_check.md
01_book_structure.md
02_core_ideas.md
03_key_cases.md
04_timeline.md
05_people.md
06_concepts.md
07_quotes.md
08_misreadings.md
09_reader_takeaways.md
10_content_brief.md
11_slide_outline.md
12_slide_script.md
13_fact_check.md
14_slide_script_verified.md
15_ppt_content_qa.md
16_ppt_visual_qa.md
```

### 5. Output layout for reusable demos

Use the 《人类简史》 demo as the reference shape:

```text
demos/<slug>/
  README.md                         # workflow narrative, screenshots, QA checklist
  prompts/                          # reusable artifact prompts
  assets/                           # mockups and README preview images
  drive_outputs/                    # prompt logs + manifest linking original Drive files
  compressed_outputs/               # compressed PPTX/PDF/MP4 review copies
```

The repo should contain reproducible instructions and lightweight review artifacts. Original source books, private auth state, browser cookies, OAuth tokens, Z-Library sessions, and full-quality large binaries should stay outside git.

## Article / visual explainer

See [`docs/notebooklm-workflow-article.md`](docs/notebooklm-workflow-article.md) for a long-form Chinese article explaining how the workflow works. It combines:

- an image-generation hero illustration;
- SVG architecture and artifact-matrix diagrams;
- selected PPT preview images from the Sapiens demo;
- a Remotion storyboard plus a reusable `remotion-workflow-teaser.tsx` draft for turning the workflow into a short explainer video.

## Demo / Best-practice example

See [`demos/sapiens/`](demos/sapiens/) for a complete best-practice example using a 《人类简史》 NotebookLM notebook as the target output shape. It includes:

- a reproducible NotebookLM CLI workflow for creating a book notebook and generating Studio artifacts;
- prompt files for slide deck, study guide/report, mind map, infographic, data table, quiz, flashcards, audio, and video;
- real Drive-delivered prompt logs plus a final infographic PNG committed under `demos/sapiens/drive_outputs/`;
- compressed PPTX/PDF/MP4 viewing copies committed under `demos/sapiens/compressed_outputs/`;
- a Drive artifact manifest linking to the original full-quality PPTX/PDF/MP4 outputs;
- lightweight SVG mock screenshots showing the desired artifact gallery, dense slide style, and Chinese infographic quality target;
- a QA checklist for source grounding, Chinese visual text, PPTX validation, and long-running artifact handoff.

Preview:

![Sapiens final NotebookLM infographic](demos/sapiens/drive_outputs/sapiens_infographic_final.png)

Selected detailed slide previews:

| Cover | Three revolutions | Wheat trap |
|---|---|---|
| ![Slide 1 cover](demos/sapiens/assets/slide-previews/detailed-slide-01-cover.jpg) | ![Slide 3 three revolutions](demos/sapiens/assets/slide-previews/detailed-slide-03-three-revolutions.jpg) | ![Slide 8 wheat trap](demos/sapiens/assets/slide-previews/detailed-slide-08-wheat-trap.jpg) |
| Universal orders | Modern engine | Future DNA |
| ![Slide 12 universal orders](demos/sapiens/assets/slide-previews/detailed-slide-12-universal-orders.jpg) | ![Slide 15 modern engine](demos/sapiens/assets/slide-previews/detailed-slide-15-modern-engine.jpg) | ![Slide 19 future DNA](demos/sapiens/assets/slide-previews/detailed-slide-19-future-dna.jpg) |

Full artifact indexes:

- [`demos/sapiens/drive_outputs/README.md`](demos/sapiens/drive_outputs/README.md) — original full-quality Drive artifacts and prompt logs.
- [`demos/sapiens/compressed_outputs/README.md`](demos/sapiens/compressed_outputs/README.md) — compressed PPTX/PDF/MP4 viewing copies committed to git.

> The demo does not commit the book PDF, private auth data, or original full-quality video/PPT binaries. Use your own legally available source inside NotebookLM.

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
