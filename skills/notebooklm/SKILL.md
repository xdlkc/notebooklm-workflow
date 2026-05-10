---
name: notebooklm
description: Complete API for Google NotebookLM - full programmatic access including features not in the web UI. Create notebooks, add sources, generate all artifact types, download in multiple formats. Activates on explicit /notebooklm or intent like "create a podcast about X"
---

> ⚠️ **UPGRADE GUARDRAIL** — This skill holds Google SID cookies. Pinned at `notebooklm-py==0.3.4` (audited 2026-04-23, verdict LOW RISK). **Before running `hermes skills update notebooklm`, `uv pip install -U notebooklm-py`, or any other upgrade, follow the Upgrade Protocol in [SECURITY_AUDIT.md](SECURITY_AUDIT.md) — diff the new version and re-scan.** Do not auto-upgrade on community trust alone.

# NotebookLM Automation

Complete programmatic access to Google NotebookLM—including capabilities not exposed in the web UI. Create notebooks, add sources (URLs, YouTube, PDFs, audio, video, images), chat with content, generate all artifact types, and download results in multiple formats.

## Installation

**From PyPI (Recommended):**
```bash
pip install notebooklm-py
```

**From GitHub (use latest release tag, NOT main branch):**
```bash
# Get the latest release tag (using curl)
LATEST_TAG=$(curl -s https://api.github.com/repos/teng-lin/notebooklm-py/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
pip install "git+https://github.com/teng-lin/notebooklm-py@${LATEST_TAG}"
```

⚠️ **DO NOT install from main branch** (`pip install git+https://github.com/teng-lin/notebooklm-py`). The main branch may contain unreleased/unstable changes. Always use PyPI or a specific release tag, unless you are testing unreleased features.

**Skill install methods:**

- `notebooklm skill install` installs this skill into the supported local agent directories managed by the CLI.
- `npx skills add teng-lin/notebooklm-py` installs this skill from the GitHub repository into compatible agent skill directories.
- If you are already reading this file inside an agent skill directory, the skill is already installed. You only need the Python package and authentication below.

**CLI-managed install:**
```bash
notebooklm skill install
```

## Prerequisites

**IMPORTANT:** Before using any command, you MUST authenticate:

```bash
notebooklm login          # Opens browser for Google OAuth
notebooklm list           # Verify authentication works
```

If commands fail with authentication errors, re-run `notebooklm login`.

### CI/CD, Multiple Accounts, and Parallel Agents

For automated environments, multiple accounts, or parallel agent workflows:

| Variable | Purpose |
|----------|---------|
| `NOTEBOOKLM_HOME` | Custom config directory (default: `~/.notebooklm`) |
| `NOTEBOOKLM_PROFILE` | Active profile name (default: `default`) |
| `NOTEBOOKLM_AUTH_JSON` | Inline auth JSON - no file writes needed |

**CI/CD setup:** Set `NOTEBOOKLM_AUTH_JSON` from a secret containing your `storage_state.json` contents.

**Multiple accounts:** Use named profiles (`notebooklm profile create work`, then `notebooklm -p work login`). Alternatively, use different `NOTEBOOKLM_HOME` directories per account.

**Parallel agents:** The CLI stores notebook context in a shared file (`~/.notebooklm/context.json`). Multiple concurrent agents using `notebooklm use` can overwrite each other's context.

**Solutions for parallel workflows:**
1. **Always use explicit notebook ID** (recommended): Pass `-n <notebook_id>` (for `wait`/`download` commands) or `--notebook <notebook_id>` (for others) instead of relying on `use`
2. **Per-agent isolation via profiles:** `export NOTEBOOKLM_PROFILE=agent-$ID` (each profile gets its own context file)
3. **Per-agent isolation via home:** Set unique `NOTEBOOKLM_HOME` per agent: `export NOTEBOOKLM_HOME=/tmp/agent-$ID`
4. **Use full UUIDs:** Avoid partial IDs in automation (they can become ambiguous)

## Agent Setup Verification

Before starting workflows, verify the CLI is ready:

1. `notebooklm status` → Should show "Authenticated as: email@..."
2. `notebooklm list --json` → Should return valid JSON (even if empty notebooks list)
3. If either fails → Run `notebooklm login`

## When This Skill Activates

**Explicit:** User says "/notebooklm", "use notebooklm", or mentions the tool by name

**Intent detection:** Recognize requests like:
- "Create a podcast about [topic]"
- "Summarize these URLs/documents"
- "Generate a quiz from my research"
- "Turn this into an audio overview"
- "Create flashcards for studying"
- "Generate a video explainer"
- "Make an infographic"
- "Create a mind map of the concepts"
- "Download the quiz as markdown"
- "Add these sources to NotebookLM"

## Autonomy Rules

**Run automatically (no confirmation):**
- `notebooklm status` - check context
- `notebooklm auth check` - diagnose auth issues
- `notebooklm list` - list notebooks
- `notebooklm source list` - list sources
- `notebooklm artifact list` - list artifacts
- `notebooklm language list` - list supported languages
- `notebooklm language get` - get current language
- `notebooklm language set` - set language (global setting)
- `notebooklm artifact wait` - wait for artifact completion (in subagent context)
- `notebooklm source wait` - wait for source processing (in subagent context)
- `notebooklm research status` - check research status
- `notebooklm research wait` - wait for research (in subagent context)
- `notebooklm use <id>` - set context (⚠️ SINGLE-AGENT ONLY - use `-n` flag in parallel workflows)
- `notebooklm create` - create notebook
- `notebooklm ask "..."` - chat queries (without `--save-as-note`)
- `notebooklm history` - display conversation history (read-only)
- `notebooklm source add` - add sources
- `notebooklm profile list` - list profiles
- `notebooklm profile create` - create profile
- `notebooklm profile switch` - switch active profile
- `notebooklm doctor` - check environment health

**Ask before running:**
- `notebooklm delete` - destructive
- `notebooklm generate *` - long-running, may fail
- `notebooklm download *` - writes to filesystem
- `notebooklm artifact wait` - long-running (when in main conversation)
- `notebooklm source wait` - long-running (when in main conversation)
- `notebooklm research wait` - long-running (when in main conversation)
- `notebooklm ask "..." --save-as-note` - writes a note
- `notebooklm history --save` - writes a note

## Quick Reference

| Task | Command |
|------|---------|
| Authenticate | `notebooklm login` |
| Diagnose auth issues | `notebooklm auth check` |
| Diagnose auth (full) | `notebooklm auth check --test` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Rename notebook | `notebooklm rename -n <notebook_id> "New Title"` |
| Set context | `notebooklm use <notebook_id>` |
| Show context | `notebooklm status` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file | `notebooklm source add ./file.pdf` |
| Add YouTube | `notebooklm source add "https://youtube.com/..."` |
| List sources | `notebooklm source list` |
| Delete source by ID | `echo y \| notebooklm source delete <source_id>` |
| Delete source by exact title | `notebooklm source delete-by-title "Exact Title"` |
| Rename source | `notebooklm source rename <source_id> "New Title" -n <notebook_id>` |
| Wait for source processing | `notebooklm source wait <source_id>` |
| Web research (fast) | `notebooklm source add-research "query"` |
| Web research (deep) | `notebooklm source add-research "query" --mode deep --no-wait` |
| Check research status | `notebooklm research status` |
| Wait for research | `notebooklm research wait --import-all` |
| Chat | `notebooklm ask "question"` |
| Chat (specific sources) | `notebooklm ask "question" -s src_id1 -s src_id2` |
| Chat (with references) | `notebooklm ask "question" --json` |
| Chat (save answer as note) | `notebooklm ask "question" --save-as-note` |
| Chat (save with title) | `notebooklm ask "question" --save-as-note --note-title "Title"` |
| Show conversation history | `notebooklm history` |
| Save all history as note | `notebooklm history --save` |
| Continue specific conversation | `notebooklm ask "question" -c <conversation_id>` |
| Save history with title | `notebooklm history --save --note-title "My Research"` |
| Get source fulltext | `notebooklm source fulltext <source_id>` |
| Get source guide | `notebooklm source guide <source_id>` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate podcast (JSON) | `notebooklm generate audio --json` |
| Generate podcast (specific sources) | `notebooklm generate audio -s src_id1 -s src_id2` |
| Generate video | `notebooklm generate video "instructions"` |
| Generate report | `notebooklm generate report --format briefing-doc` |
| Generate report (append instructions) | `notebooklm generate report --format study-guide --append "Target audience: beginners"` |
| Generate quiz | `notebooklm generate quiz` |
| Revise a slide | `notebooklm generate revise-slide "prompt" --artifact <id> --slide 0` |
| Check artifact status | `notebooklm artifact list` |
| Wait for completion | `notebooklm artifact wait <artifact_id>` |
| Download audio | `notebooklm download audio ./output.mp3` |
| Download video | `notebooklm download video ./output.mp4` |
| Download slide deck (PDF) | `notebooklm download slide-deck ./slides.pdf` |
| Download slide deck (PPTX) | `notebooklm download slide-deck ./slides.pptx --format pptx` |
| Download report | `notebooklm download report ./report.md` |
| Download mind map | `notebooklm download mind-map ./map.json` |
| Download data table | `notebooklm download data-table ./data.csv` |
| Download quiz | `notebooklm download quiz quiz.json` |
| Download quiz (markdown) | `notebooklm download quiz --format markdown quiz.md` |
| Download flashcards | `notebooklm download flashcards cards.json` |
| Download flashcards (markdown) | `notebooklm download flashcards --format markdown cards.md` |
| Delete notebook | `notebooklm delete <id>` |
| List languages | `notebooklm language list` |
| Get language | `notebooklm language get` |
| Set language | `notebooklm language set zh_Hans` |
| List profiles | `notebooklm profile list` |
| Create profile | `notebooklm profile create work` |
| Switch profile | `notebooklm profile switch work` |
| Delete profile | `notebooklm profile delete old` |
| Rename profile | `notebooklm profile rename old new` |
| Use profile (one-off) | `notebooklm -p work list` |
| Health check | `notebooklm doctor` |
| Health check (auto-fix) | `notebooklm doctor --fix` |

**Parallel safety:** Use explicit notebook IDs in parallel workflows. Commands supporting `-n` shorthand include: `source add`, `artifact wait`, `source wait`, `research wait/status`, and `download *`. Download commands also support `-a/--artifact`. Other commands may use `--notebook` where supported. For chat, use `-c <conversation_id>` to target a specific conversation.

⚠️ Verify command support with `notebooklm <command> --help` when automating. `source add` supports `-n, --notebook TEXT` in notebooklm-py 0.3.4, so prefer `notebooklm source add <content> -n <full-notebook-uuid> --json` for parallel-safe uploads instead of relying on `notebooklm use`. Commands that still do not support `-n` include: `source list`, `source delete`, `ask`, `use`, `create`, `generate *`.

**Partial IDs:** For notebook IDs, **always use full UUIDs** — partial IDs are rejected by Google's RPC even when unique. Extract full ID via `notebooklm list --json | python3 -c "import sys,json; ..."`. Partial IDs work reliably only for `source delete` and `source wait`.

## Command Output Formats

Commands with `--json` return structured data for parsing:

**Create notebook:**
```
$ notebooklm create "Research" --json
{"id": "abc123de-...", "title": "Research"}
```

**Add source:**
```
$ notebooklm source add "https://example.com" --json
{"source_id": "def456...", "title": "Example", "status": "processing"}
```

**Generate artifact:**
```
$ notebooklm generate audio "Focus on key points" --json
{"task_id": "xyz789...", "status": "pending"}
```

**Chat with references:**
```
$ notebooklm ask "What is X?" --json
{"answer": "X is... [1] [2]", "conversation_id": "...", "turn_number": 1, "is_follow_up": false, "references": [{"source_id": "abc123...", "citation_number": 1, "cited_text": "Relevant passage from source..."}, {"source_id": "def456...", "citation_number": 2, "cited_text": "Another passage..."}]}
```

**Source fulltext (get indexed content):**
```
$ notebooklm source fulltext <source_id> --json
{"source_id": "...", "title": "...", "char_count": 12345, "content": "Full indexed text..."}
```

**Understanding citations:** The `cited_text` in references is often a snippet or section header, not the full quoted passage. The `start_char`/`end_char` positions reference NotebookLM's internal chunked index, not the raw fulltext. Use `SourceFulltext.find_citation_context()` to locate citations:
```python
fulltext = await client.sources.get_fulltext(notebook_id, ref.source_id)
matches = fulltext.find_citation_context(ref.cited_text)  # Returns list[(context, position)]
if matches:
    context, pos = matches[0]  # First match; check len(matches) > 1 for duplicates
```

**Extract IDs:** Parse the `id`, `source_id`, or `task_id` field from JSON output.

## Generation Types

Most generate commands support:
- `-s, --source` to use specific source(s) instead of all sources
- `--json` for machine-readable output (returns `task_id` and `status`)
- `--retry N` to automatically retry on rate limits with exponential backoff

Language options are command-specific. Audio/video/slide-deck/infographic/report/data-table support `--language` in notebooklm-py 0.3.4, but `generate quiz` and `generate flashcards` do **not**; put the desired language in the description prompt for those instead. Verify with `notebooklm generate <type> --help` before scripting a new artifact type.

| Type | Command | Options | Download |
|------|---------|---------|----------|
| Podcast | `generate audio` | `--format [deep-dive\|brief\|critique\|debate]`, `--length [short\|default\|long]` | .mp3 |
| Video | `generate video` | `--format [explainer\|brief]`, `--style [auto\|classic\|whiteboard\|kawaii\|anime\|watercolor\|retro-print\|heritage\|paper-craft]` | .mp4 |
| Slide Deck | `generate slide-deck` | `--format [detailed\|presenter]`, `--length [default\|short]` | .pdf / .pptx |
| Slide Revision | `generate revise-slide "prompt" --artifact <id> --slide N` | `--wait`, `--notebook` | *(re-downloads parent deck)* |
| Infographic | `generate infographic` | `--orientation [landscape\|portrait\|square]`, `--detail [concise\|standard\|detailed]`, `--style [auto\|sketch-note\|professional\|bento-grid\|editorial\|instructional\|bricks\|clay\|anime\|kawaii\|scientific]` | .png |
| Report | `generate report` | `--format [briefing-doc\|study-guide\|blog-post\|custom]`, `--append "extra instructions"` | .md |
| Mind Map | `generate mind-map` | *(sync, instant)* | .json |
| Data Table | `generate data-table` | description required | .csv |
| Quiz | `generate quiz` | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` | .json/.md/.html |
| Flashcards | `generate flashcards` | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` | .json/.md/.html |

## Features Beyond the Web UI

These capabilities are available via CLI but not in NotebookLM's web interface:

| Feature | Command | Description |
|---------|---------|-------------|
| **Batch downloads** | `download <type> --all` | Download all artifacts of a type at once |
| **Quiz/Flashcard export** | `download quiz --format json` | Export as JSON, Markdown, or HTML (web UI only shows interactive view) |
| **Mind map extraction** | `download mind-map` | Export hierarchical JSON for visualization tools |
| **Data table export** | `download data-table` | Download structured tables as CSV |
| **Slide deck as PPTX** | `download slide-deck --format pptx` | Download slide deck as editable .pptx (web UI only offers PDF) |
| **Slide revision** | `generate revise-slide "prompt" --artifact <id> --slide N` | Modify individual slides with a natural-language prompt |
| **Report template append** | `generate report --format study-guide --append "..."` | Append custom instructions to built-in format templates without losing the format type |
| **Source fulltext** | `source fulltext <id>` | Retrieve the indexed text content of any source |
| **Save chat to note** | `ask "..." --save-as-note` / `history --save` | Save Q&A answers or conversation history as notebook notes |
| **Programmatic sharing** | `share` commands | Manage sharing permissions without the UI |

## Common Workflows

### Research to Podcast (Interactive)
**Time:** 5-10 minutes total

1. `notebooklm create "Research: [topic]"` — *if fails: check auth with `notebooklm login`*
2. `notebooklm source add` for each URL/document — *if one fails: log warning, continue with others*
3. Wait for sources: `notebooklm source list --json` until all status=READY — *required before generation*
4. `notebooklm generate audio "Focus on [specific angle]"` (confirm when asked) — *if rate limited: wait 5 min, retry once*
5. Note the artifact ID returned
6. Check `notebooklm artifact list` later for status
7. `notebooklm download audio ./podcast.mp3` when complete (confirm when asked)

### Research to Podcast (Automated with Subagent)
**Time:** 5-10 minutes, but continues in background

When user wants full automation (generate and download when ready):

1. Create notebook and add sources as usual
2. Wait for sources to be ready (use `source wait` or check `source list --json`)
3. Run `notebooklm generate audio "..." --json` → parse `artifact_id` from output
4. **Spawn a background agent** using Task tool:
   ```
   Task(
     prompt="Wait for artifact {artifact_id} in notebook {notebook_id} to complete, then download.
             Use: notebooklm artifact wait {artifact_id} -n {notebook_id} --timeout 600
             Then: notebooklm download audio ./podcast.mp3 -a {artifact_id} -n {notebook_id}",
     subagent_type="general-purpose"
   )
   ```
5. Main conversation continues while agent waits

**Error handling in subagent:**
- If `artifact wait` returns exit code 2 (timeout): Report timeout, suggest checking `artifact list`
- If download fails: Check if artifact status is COMPLETED first

**Benefits:** Non-blocking, user can do other work, automatic download on completion

### Document Analysis
**Time:** 1-2 minutes

1. `notebooklm create "Analysis: [project]"`
2. `notebooklm source add ./doc.pdf` (or URLs)
3. `notebooklm ask "Summarize the key points"`
4. `notebooklm ask "What are the main arguments?"`
5. Continue chatting as needed

### Social Media / Book-Recommendation Material Pack
**Time:** 5-15 minutes for text + mind map/report; audio/video may take longer

Use when the user wants to turn an existing NotebookLM notebook (especially a book PDF) into social-media content: 小红书/公众号/LinkedIn posts, carousels, hooks, cover copy, short-video/podcast talking points, or a reusable content素材包.

1. Locate and set the exact notebook context:
   ```bash
   NOTEBOOKLM_HOME=/path/to/profile notebooklm list --json > /tmp/notebooklm_list.json
   NOTEBOOKLM_HOME=/path/to/profile notebooklm use <full-notebook-uuid>
   NOTEBOOKLM_HOME=/path/to/profile notebooklm source list --json
   ```
2. Generate several focused text素材 files with plain `ask` output (not `--json`) and save directly to Markdown. For example:
   ```bash
   OUT=/tmp/notebooklm_content_pack; mkdir -p "$OUT"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm ask "请基于这本书，为小红书推荐笔记提炼：5个核心卖点、10个共鸣场景、3个差异化角度、适合人群、应避免的鸡汤/硬广表达。中文输出，可直接用于创作。" > "$OUT/01_selling_points.md"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm ask "请生成15个标题/开头hook、8句封面大字短句、10条正文金句、每个核心原则对应的日常例子。语气适合小红书，但不要夸张低俗。" > "$OUT/02_hooks_quotes.md"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm ask "请生成8页图文脚本。每页包括：页面标题、正文要点、视觉建议。" > "$OUT/03_carousel_script.md"
   ```
3. Generate Studio artifacts for structure and deeper extraction:
   ```bash
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate mind-map --json > "$OUT/mind_map_generate.json"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm download mind-map "$OUT/mind_map.json"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate report --format study-guide --append "目标：为社交媒体推荐内容生成素材。请突出核心概念、现实场景、读者收益、适合人群、封面短句。语言和平台风格按用户要求。" --retry 2 --json > "$OUT/report_generate.json"
   ```

   If the user asks for “all Studio tools” or “尽量使用所有 studio 工具”, create an `OUT/prompts.md` with tailored prompts per artifact type, then start all available types and save each log/result:
   ```bash
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate mind-map --json > "$OUT/generate_mind_map.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate audio "<audio prompt>" --format deep-dive --length default --language zh_Hans --retry 2 --json > "$OUT/generate_audio.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate video "<video prompt>" --format explainer --style whiteboard --language zh_Hans --retry 2 --json > "$OUT/generate_video.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate report --format study-guide --append "<study-guide prompt>" --language zh_Hans --retry 2 --json > "$OUT/generate_report.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate slide-deck "<slide prompt>" --format detailed --length short --language zh_Hans --retry 2 --json > "$OUT/generate_slide_deck.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate infographic "<infographic prompt>" --orientation portrait --detail detailed --style professional --language zh_Hans --retry 2 --json > "$OUT/generate_infographic.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate data-table "<table prompt>" --language zh_Hans --retry 2 --json > "$OUT/generate_data_table.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate quiz "<Chinese quiz prompt>" --difficulty medium --quantity standard --retry 2 --json > "$OUT/generate_quiz.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm generate flashcards "<Chinese flashcard prompt>" --difficulty medium --quantity standard --retry 2 --json > "$OUT/generate_flashcards.log"
   NOTEBOOKLM_HOME=/path/to/profile notebooklm artifact list --json > "$OUT/artifacts_started.json"
   ```
   Quiz/flashcards do not accept `--language`; include “中文” in their prompts. Do not wait for long audio/video/slide/infographic/quiz/flashcard jobs unless the user explicitly asks. Download completed fast artifacts (usually mind-map/report/data-table) with `download <type> -a <artifact_id> -n <notebook_id>`, write a `SUMMARY.md` containing source readiness, artifact IDs/statuses, prompt paths, and package the output directory with `zip`.
4. Wait/download only if the artifact is likely useful now. Reports are usually worth waiting for; audio/video can be fire-and-forget:
   ```bash
   TASK_ID=$(python3 - <<'PY'
   import json; print(json.load(open('/tmp/notebooklm_content_pack/report_generate.json'))['task_id'])
   PY
   )
   NOTEBOOKLM_HOME=/path/to/profile notebooklm artifact wait "$TASK_ID" -n <full-notebook-uuid> --timeout 600
   NOTEBOOKLM_HOME=/path/to/profile notebooklm download report "$OUT/study_guide.md" -a "$TASK_ID" -n <full-notebook-uuid>
   ```
5. Combine and package outputs:
   ```bash
   cat "$OUT"/*.md > "$OUT/combined_materials.md"
   (cd /tmp && zip -qr notebooklm_content_pack.zip "$(basename "$OUT")")
   ```

**Pitfalls:**
- For long, human-readable Chinese answers, `notebooklm ask --json` can produce very large/invalid JSON or be awkward to parse. Prefer plain `notebooklm ask "..." > file.md`; reserve `--json` for IDs/status/artifact metadata.
- `generate report` and `artifact list/wait` can intermittently timeout on `GET_NOTEBOOK`/`LIST_ARTIFACTS`; retry once or use `--retry` on generation before investigating.
- Audio generation can remain `pending` for a long time even when text/report/mind-map are complete. Report the artifact ID/status instead of blocking the main conversation indefinitely.
- If multiple agents may use NotebookLM at once, prefer explicit `-n <full-notebook-uuid>` for waits/downloads and avoid relying on shared `use` context where possible.

### Bulk Import
**Time:** Varies by source count

1. `notebooklm create "Collection: [name]"`
2. Add multiple sources:
   ```bash
   notebooklm source add "https://url1.com"
   notebooklm source add "https://url2.com"
   notebooklm source add ./local-file.pdf
   ```
3. `notebooklm source list` to verify

### Bulk URL-Source Import from a Sitemap
**Time:** Varies by source count (hundreds of URLs can take 10+ minutes)

Use when the user wants each discovered URL uploaded as its own NotebookLM source, e.g. “upload every official blog URL” or explicitly corrects that a Markdown URL index is not enough. This is different from a URL index notebook: each web page becomes a separate NotebookLM source.

1. Verify auth and fetch URLs from the site sitemap. Use a browser User-Agent if needed:
   ```bash
   notebooklm status
   curl -L -A 'Mozilla/5.0' -sS https://example.com/sitemap.xml > /tmp/site_sitemap.xml
   python3 - <<'PY'
   import re, urllib.parse, pathlib
   xml = pathlib.Path('/tmp/site_sitemap.xml').read_text(encoding='utf-8', errors='replace')
   locs = sorted(set(re.findall(r'<loc>(.*?)</loc>', xml)))
   prefixes = ['/blog', '/news', '/research', '/engineering']
   urls=[]
   for u in locs:
       p=urllib.parse.urlparse(u).path.rstrip('/')
       if any(p.startswith(prefix + '/') for prefix in prefixes):
           urls.append(u)
   pathlib.Path('/tmp/site_urls.txt').write_text('\n'.join(urls)+'\n')
   print(len(urls))
   PY
   ```
2. Create a notebook and use explicit `-n <full-notebook-uuid>` for every upload. Do not rely on `notebooklm use` inside parallel upload workers:
   ```bash
   notebooklm create "<Site> 官方博客逐 URL 全集" --json | tee /tmp/site_nb1.json
   NB_ID=$(python3 - <<'PY'
   import json
   print(json.load(open('/tmp/site_nb1.json'))['notebook']['id'])
   PY
   )
   ```
3. Upload with bounded parallelism and JSONL logging. Four workers worked reliably; retry transient failures, but expect hard failures when the notebook reaches the plan limit:
   ```bash
   python3 -u - <<'PY'
   import concurrent.futures, json, pathlib, random, subprocess, time
   nb = json.load(open('/tmp/site_nb1.json'))['notebook']['id']
   urls = [u.strip() for u in pathlib.Path('/tmp/site_urls.txt').read_text().splitlines() if u.strip()]
   log = pathlib.Path('/tmp/site_url_upload.jsonl'); log.write_text('')
   def add(item):
       i,u=item; last=''
       for attempt in range(1,4):
           try:
               p=subprocess.run(['notebooklm','source','add',u,'-n',nb,'--json'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
               last=p.stdout.strip()
               if p.returncode==0:
                   return {'index':i,'url':u,'ok':True,'output':last}
           except subprocess.TimeoutExpired as e:
               last='TIMEOUT '+str(e)
           time.sleep((2**attempt)+random.random())
       return {'index':i,'url':u,'ok':False,'output':last}
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
       for r in concurrent.futures.as_completed([ex.submit(add,x) for x in enumerate(urls,1)]):
           row=r.result()
           with log.open('a') as f: f.write(json.dumps(row, ensure_ascii=False)+'\n')
           print(('OK' if row['ok'] else 'FAIL'), row['url'], flush=True)
   PY
   ```
4. Verify coverage by listing sources. `source list` may require setting context first (it does not reliably accept `-n` in all versions):
   ```bash
   notebooklm use "$NB_ID"
   notebooklm source list --json > /tmp/site_nb1_sources.json
   ```
5. If a notebook hits the source limit (for example Pro: 300 ready sources), create another notebook for the remaining URLs and continue. Failures after a round of successes can be quota/limit related rather than inaccessible URLs; retry them in a new notebook before declaring them bad.
6. Final verification should compare the original URL list against the union of `ready` source URLs from all created notebooks:
   ```bash
   python3 - <<'PY'
   import json, pathlib
   original=[u.strip() for u in pathlib.Path('/tmp/site_urls.txt').read_text().splitlines() if u.strip()]
   ready=set()
   for path in ['/tmp/site_nb1_sources.json', '/tmp/site_nb2_sources.json']:
       if pathlib.Path(path).exists():
           data=json.load(open(path))
           ready.update(s.get('url') for s in data.get('sources',[]) if s.get('status')=='ready' and s.get('url'))
   missing=[u for u in original if u not in ready]
   print('original', len(original), 'ready_unique', len(ready), 'missing', len(missing))
   if missing: print('\n'.join(missing[:20]))
   PY
   ```

**Pitfalls:**
- Clarify intent: “upload URLs/addresses” might mean a single Markdown index or individual web-page sources. If the user says “each URL” or corrects the interpretation, upload every URL independently.
- NotebookLM may accept upload attempts but only keep a plan-limited number of `ready` sources; verify `ready` source URLs, not just successful CLI return codes or raw source count.
- Do not delete failed/error sources without user confirmation; source deletion is destructive.
- Splitting across multiple notebooks may be necessary to cover all URLs.

### Website Sitemap URL Index to Notebook
**Time:** 1-3 minutes

Use when the user asks to collect all official blog/article URLs from a website and put them into NotebookLM. Prefer this when the goal is an index of URLs rather than ingesting every page as a separate NotebookLM source.

1. Check auth and create a notebook:
   ```bash
   notebooklm status
   notebooklm list --json >/tmp/notebooklm_list_check.json
   notebooklm create "<Site> 官方博客 URL 全集" --json | tee /tmp/site_notebook_create.json
   ```
2. Fetch the sitemap with a browser User-Agent if default Python/curl requests are blocked:
   ```bash
   curl -L -A 'Mozilla/5.0' -sS https://example.com/sitemap.xml > /tmp/site_sitemap.xml
   ```
3. Parse `<loc>` entries and filter to article-like sections such as `/blog/`, `/news/`, `/research/`, or `/engineering/`. Exclude section landing pages unless the user explicitly asks for them. Deduplicate and write a Markdown index grouped by section:
   ```bash
   python3 - <<'PY'
   import re, urllib.parse, pathlib, datetime
   xml = pathlib.Path('/tmp/site_sitemap.xml').read_text(encoding='utf-8', errors='replace')
   locs = sorted(set(re.findall(r'<loc>(.*?)</loc>', xml)))
   prefixes = ['/blog', '/news', '/research', '/engineering']
   urls = []
   for u in locs:
       p = urllib.parse.urlparse(u).path.rstrip('/')
       if any(p.startswith(prefix + '/') for prefix in prefixes):
           urls.append(u)
   out = pathlib.Path('/tmp/site_official_blog_urls.md')
   lines = [
       '# 官方博客 URL 全集', '',
       f'抓取时间：{datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()}',
       '来源：/sitemap.xml', '',
       f'总数：{len(urls)}', '',
   ] + [f'- {u}' for u in urls]
   out.write_text('\n'.join(lines), encoding='utf-8')
   print(out, len(urls))
   PY
   ```
4. Upload the Markdown index as one source. This avoids hitting NotebookLM per-notebook source limits while preserving every URL:
   ```bash
   NB_ID=$(python3 - <<'PY'
   import json
   print(json.load(open('/tmp/site_notebook_create.json'))['notebook']['id'])
   PY
   )
   notebooklm use "$NB_ID"
   notebooklm source add /tmp/site_official_blog_urls.md --json | tee /tmp/site_source_add.json
   notebooklm source list --json
   ```
5. Verify the source status is `ready` and report the notebook ID, source ID, URL count, and local Markdown path.

**Pitfalls:**
- Some sites return 403 without a browser-like User-Agent; retry `curl -A 'Mozilla/5.0'` before giving up.
- NotebookLM source limits apply to individual sources, so uploading hundreds of URLs individually can fail. If the task is only “addresses/URLs”, upload a single Markdown URL index.
- Always use full notebook UUIDs extracted from `create --json` or `list --json`; avoid partial IDs.

### Bulk Artifact Presence Audit
**Time:** 2-10 minutes depending on notebook count

Use when the user asks which notebooks have or have not generated a Studio artifact, e.g. “哪个笔记本没有生成过 PPT”, “which notebooks lack slide decks”, or needs coverage reporting across the whole NotebookLM account.

For a single current notebook, `notebooklm artifact list --json` is fine. For many notebooks, the CLI artifact command is context-bound and can time out; prefer the Python API with bounded concurrency and artifact-specific list methods.

```bash
# 1) Verify the CLI can list notebooks and export notebook metadata
NOTEBOOKLM_HOME=/path/to/home notebooklm list --json > /tmp/notebooklm_list.json

# 2) Audit slide-deck/PPT presence across every notebook
python3 - <<'PY'
import asyncio, json, time
from pathlib import Path
from notebooklm import NotebookLMClient

# Use the actual Playwright storage_state.json path. If NOTEBOOKLM_HOME is set,
# remember the CLI may append profiles/default under it; locate with:
#   find ~/.notebooklm -name storage_state.json
STORAGE = '/path/to/storage_state.json'
OUT = '/tmp/notebooklm_artifact_audit.json'

async def main():
    c = await NotebookLMClient.from_storage(path=STORAGE, timeout=60)
    async with c as client:
        notebooks = await client.notebooks.list()
        sem = asyncio.Semaphore(6)
        async def check(n):
            async with sem:
                last = None
                for attempt in range(3):
                    try:
                        # Swap this method for another artifact type when needed:
                        # list_reports, list_audio, list_video, list_infographics,
                        # list_data_tables, list_quizzes, list_flashcards, list_mind_maps
                        arts = await client.artifacts.list_slide_decks(n.id)
                        return {
                            'id': n.id,
                            'title': n.title,
                            'artifact_count': len(arts),
                            'artifacts': [
                                {'id': a.id, 'title': getattr(a, 'title', None),
                                 'status': str(getattr(a, 'status', None)),
                                 'type': str(getattr(a, 'type', None))}
                                for a in arts
                            ],
                            'error': None,
                        }
                    except Exception as e:
                        last = repr(e)
                        await asyncio.sleep(1.5 * (attempt + 1))
                return {'id': n.id, 'title': n.title, 'artifact_count': None, 'artifacts': [], 'error': last}

        results = []
        for i, fut in enumerate(asyncio.as_completed([check(n) for n in notebooks]), 1):
            results.append(await fut)
            if i % 25 == 0:
                print('checked', i, '/', len(notebooks), flush=True)

        data = {'checked_at': time.strftime('%Y-%m-%d %H:%M:%S'), 'total': len(notebooks), 'results': results}
        Path(OUT).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        with_artifact = [r for r in results if r['error'] is None and (r['artifact_count'] or 0) > 0]
        without_artifact = [r for r in results if r['error'] is None and r['artifact_count'] == 0]
        errors = [r for r in results if r['error']]
        print(json.dumps({'total': len(notebooks), 'with_artifact': len(with_artifact), 'without_artifact': len(without_artifact), 'errors': len(errors), 'out': OUT}, ensure_ascii=False))
        print('WITHOUT_ARTIFACT')
        for r in sorted(without_artifact, key=lambda x: x['title']):
            print(r['title'] + '\t' + r['id'])

asyncio.run(main())
PY
```

3. Create a Markdown report with: checked time, total notebooks, with/without counts, the small “with artifact” list for reverse lookup, and the full “without artifact” list. Attach or upload the report if it is long.

**Pitfalls:**
- The Python package may be installed in the Hermes venv even when system `python3` cannot import `notebooklm`; use `command -v notebooklm` to locate the venv and run its Python.
- `NotebookLMClient.from_storage` takes `path=...`, not `storage_path=...`.
- Status values in Python artifact objects may stringify to numeric codes; presence/absence is determined by list length, not the display status string.
- Keep concurrency bounded (around 4-8) and retry transient RPC failures; avoid spawning hundreds of simultaneous `artifact list` CLI calls.

### Bulk Notebook Renaming
**Time:** Varies by notebook count

Use when the user asks to normalize or translate notebook titles across many notebooks.

1. Export the current list first:
   ```bash
   notebooklm list --json > /tmp/notebooklm_list_before_rename.json
   ```
2. Identify candidates programmatically, e.g. pure-English titles:
   ```bash
   python3 - <<'PY'
   import json,re
   data=json.load(open('/tmp/notebooklm_list_before_rename.json'))
   for n in data['notebooks']:
       t=n['title']
       if re.search(r'[A-Za-z]', t) and not re.search(r'[\u4e00-\u9fff]', t):
           print(n['id'], t)
   PY
   ```
3. Rename with full UUIDs:
   ```bash
   notebooklm rename -n <full-notebook-uuid> "新标题"
   ```
4. For large batches, script sequential renames with retries and short sleeps. If a rename returns only `Error:` with no details, retry the same command once or twice before investigating; transient RPC failures can occur.
5. Verify by re-listing and checking the candidate set is empty:
   ```bash
   notebooklm list --json > /tmp/notebooklm_list_after_rename.json
   ```

**Source limits:** Varies by plan—Standard: 50, Plus: 100, Pro: 300, Ultra: 600 sources per notebook. See [NotebookLM plans](https://support.google.com/notebooklm/answer/16213268) for details. The CLI does not enforce these limits; they are applied by your NotebookLM account.
**Supported types:** PDFs, YouTube URLs, web URLs, Google Docs, text files, Markdown, Word docs, audio files, video files, images, EPUBs

**Large file uploads (>50MB):** The default foreground `source add` timeout (120s) is insufficient for large files. Before uploading, check file size: `ls -lh <file>`. If >50MB, use background mode with extended timeout:
```bash
# Check size first
ls -lh ./large.pdf
# Background upload with 600s timeout
notebooklm source add ./large.pdf --json &
```
Upload speed depends on your connection; 100-200MB files typically need 2-5 minutes. After upload, Google still needs indexing time (10-60s per source), same as smaller files.

### Bulk Import with Source Waiting (Subagent Pattern)
**Time:** Varies by source count

When adding multiple sources and needing to wait for processing before chat/generation:

1. Add sources with `--json` to capture IDs:
   ```bash
   notebooklm source add "https://url1.com" --json  # → {"source_id": "abc..."}
   notebooklm source add "https://url2.com" --json  # → {"source_id": "def..."}
   ```
2. **Spawn a background agent** to wait for all sources:
   ```
   Task(
     prompt="Wait for sources {source_ids} in notebook {notebook_id} to be ready.
             For each: notebooklm source wait {id} -n {notebook_id} --timeout 120
             Report when all ready or if any fail.",
     subagent_type="general-purpose"
   )
   ```
3. Main conversation continues while agent waits
4. Once sources are ready, proceed with chat or generation

**Why wait for sources?** Sources must be indexed before chat or generation. Takes 10-60 seconds per source.

### Deep Web Research (Subagent Pattern)
**Time:** 2-5 minutes, runs in background

Deep research finds and analyzes web sources on a topic:

1. Create notebook: `notebooklm create "Research: [topic]"`
2. Start deep research (non-blocking):
   ```bash
   notebooklm source add-research "topic query" --mode deep --no-wait
   ```
3. **Spawn a background agent** to wait and import:
   ```
   Task(
     prompt="Wait for research in notebook {notebook_id} to complete and import sources.
             Use: notebooklm research wait -n {notebook_id} --import-all --timeout 300
             Report how many sources were imported.",
     subagent_type="general-purpose"
   )
   ```
4. Main conversation continues while agent waits
5. When agent completes, sources are imported automatically

**Alternative (blocking):** For simple cases, omit `--no-wait`:
```bash
notebooklm source add-research "topic" --mode deep --import-all
# Blocks for up to 5 minutes
```

**When to use each mode:**
- `--mode fast`: Specific topic, quick overview needed (5-10 sources, seconds)
- `--mode deep`: Broad topic, comprehensive analysis needed (20+ sources, 2-5 min)

**Research sources:**
- `--from web`: Search the web (default)
- `--from drive`: Search Google Drive

## Output Style

**Progress updates:** Brief status for each step
- "Creating notebook 'Research: AI'..."
- "Adding source: https://example.com..."
- "Starting audio generation... (task ID: abc123)"

**Fire-and-forget for long operations:**
- Start generation, return artifact ID immediately
- Do NOT poll or wait in main conversation - generation takes 5-45 minutes (see timing table)
- User checks status manually, OR use subagent with `artifact wait`

**JSON output:** Use `--json` flag for machine-readable output:
```bash
notebooklm list --json
notebooklm auth check --json
notebooklm source list --json
notebooklm artifact list --json
```

**JSON schemas (key fields):**

`notebooklm list --json`:
```json
{"notebooks": [{"id": "...", "title": "...", "created_at": "..."}]}
```

`notebooklm auth check --json`:
```json
{"checks": {"storage_exists": true, "json_valid": true, "cookies_present": true, "sid_cookie": true, "token_fetch": true}, "details": {"storage_path": "...", "auth_source": "file", "cookies_found": ["SID", "HSID", "..."], "cookie_domains": [".google.com"]}}
```

`notebooklm source list --json`:
```json
{"sources": [{"id": "...", "title": "...", "status": "ready|processing|error"}]}
```

`notebooklm artifact list --json`:
```json
{"artifacts": [{"id": "...", "title": "...", "type": "Audio Overview", "status": "in_progress|pending|completed|unknown"}]}
```

**Status values:**
- Sources: `preparing` (upload accepted, pending indexing) → `processing` → `ready` (or `error`)
- Artifacts: `pending` or `in_progress` → `completed` (or `unknown`)

## Error Handling

**On failure, offer the user a choice:**
1. Retry the operation
2. Skip and continue with something else
3. Investigate the error

**Error decision tree:**

| Error | Cause | Action |
|-------|-------|--------|
| Auth/cookie error | Session expired | Run `notebooklm auth check --test` then `notebooklm login` |
| `CSRF token not found` with final URL `https://notebooklm.google?location=unsupported` | Token fetch failed because cookies are stale or NotebookLM is inaccessible from the current network/region | Stop write operations, have the user verify NotebookLM opens in a browser, refresh login/network access, then re-run `notebooklm auth check --test` and `notebooklm list --json` before retrying |
| "No notebook context" | Context not set | Use `-n <id>` or `--notebook <id>` flag (parallel), or `notebooklm use <id>` (single-agent) |
| Source add timeout (120s) | Large file upload | Check size: `ls -lh <file>`. If >50MB, use background mode with 600s timeout |
| `source add` returns `Server disconnected without sending a response` | Upload RPC connection dropped after NotebookLM may already have accepted the file | Do not immediately retry blindly. First run `notebooklm source list -n <notebook_id> --json`; if a matching source exists (often `preparing`), treat it as accepted to avoid duplicate sources. Retry only if no matching source appears. |
| "No result found for RPC ID" | Rate limiting | Wait 5-10 min, retry |
| "RPC GET_NOTEBOOK failed...null result data" | Partial ID ambiguous or rejected | Extract **full UUID** via `notebooklm list --json` and use that instead |
| Partial ID `use` fails silently (no error, context not set) | Google RPC rejects partial notebook IDs | Always use full UUID — extract with `notebooklm list --json \| python3 -c "import sys,json; ..."` |
| Download fails | Generation incomplete | Check `artifact list` for status |
| Invalid notebook/source ID | Wrong ID | Run `notebooklm list` to verify |
| RPC protocol error | Google changed APIs | May need CLI update |

## Exit Codes

All commands use consistent exit codes:

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1 | Error (not found, processing failed) | Check stderr, see Error Handling |
| 2 | Timeout (wait commands only) | Extend timeout or check status manually |

**Examples:**
- `source wait` returns 1 if source not found or processing failed
- `artifact wait` returns 2 if timeout reached before completion
- `generate` returns 1 if rate limited (check stderr for details)

## Known Limitations

**Rate limiting:** Audio, video, quiz, flashcards, infographic, and slide deck generation may fail due to Google's rate limits. This is an API limitation, not a bug.

**Reliable operations:** These always work:
- Notebooks (list, create, delete, rename)
- Sources (add, list, delete)
- Chat/queries
- Mind-map, study-guide, report, data-table generation

**Unreliable operations:** These may fail with rate limiting:
- Audio (podcast) generation
- Video generation
- Quiz and flashcard generation
- Infographic and slide deck generation

**Workaround:** If generation fails:
1. Check status: `notebooklm artifact list`
2. Retry after 5-10 minutes
3. Use the NotebookLM web UI as fallback

**Processing times vary significantly.** Use the subagent pattern for long operations:

| Operation | Typical time | Suggested timeout |
|-----------|--------------|-------------------|
| Source processing | 30s - 10 min | 600s |
| Research (fast) | 30s - 2 min | 180s |
| Research (deep) | 15 - 30+ min | 1800s |
| Notes | instant | n/a |
| Mind-map | instant (sync) | n/a |
| Quiz, flashcards | 5 - 15 min | 900s |
| Report, data-table | 5 - 15 min | 900s |
| Audio generation | 10 - 20 min | 1200s |
| Video generation | 15 - 45 min | 2700s |

**Polling intervals:** When checking status manually, poll every 15-30 seconds to avoid excessive API calls.

## Language Configuration

Language setting controls the output language for generated artifacts (audio, video, etc.).

**Important:** Language is a **GLOBAL** setting that affects all notebooks in your account.

```bash
# List all 80+ supported languages with native names
notebooklm language list

# Show current language setting
notebooklm language get

# Set language for artifact generation
notebooklm language set zh_Hans  # Simplified Chinese
notebooklm language set ja       # Japanese
notebooklm language set en       # English (default)
```

**Common language codes:**
| Code | Language |
|------|----------|
| `en` | English |
| `zh_Hans` | 中文（简体） - Simplified Chinese |
| `zh_Hant` | 中文（繁體） - Traditional Chinese |
| `ja` | 日本語 - Japanese |
| `ko` | 한국어 - Korean |
| `es` | Español - Spanish |
| `fr` | Français - French |
| `de` | Deutsch - German |
| `pt_BR` | Português (Brasil) |

**Override per command:** Use `--language` flag on generate commands:
```bash
notebooklm generate audio --language ja   # Japanese podcast
notebooklm generate video --language zh_Hans  # Chinese video
```

**Offline mode:** Use `--local` flag to skip server sync:
```bash
notebooklm language set zh_Hans --local  # Save locally only
notebooklm language get --local  # Read local config only
```

## Troubleshooting

```bash
notebooklm --help              # Main commands
notebooklm auth check          # Diagnose auth issues
notebooklm auth check --test   # Full auth validation with network test
notebooklm delete --help       # Notebook deletion
notebooklm rename --help       # Notebook renaming
notebooklm source --help       # Source management
notebooklm research --help     # Research status/wait
notebooklm generate --help     # Content generation
notebooklm artifact --help     # Artifact management
notebooklm download --help     # Download content
notebooklm language --help     # Language settings
```

**Diagnose auth:** `notebooklm auth check` - shows cookie domains, storage path, validation status
**Re-authenticate:** `notebooklm login`
**Check version:** `notebooklm --version`
**Refresh a CLI-managed install:** `notebooklm skill install`
