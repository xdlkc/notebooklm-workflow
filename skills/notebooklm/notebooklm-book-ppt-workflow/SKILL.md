---
name: notebooklm-book-ppt-workflow
description: NotebookLM-first workflow for creating source-grounded book-sharing PPT/slide decks. Use when asked to make a 读书分享 PPT, book presentation, book club deck, course-style slides, or to ensure all PPT content comes from NotebookLM/book sources rather than model memory. Extract structure, core ideas, cases, timeline, people, concepts, quotes, and takeaways from NotebookLM before generating slides.
---

# NotebookLM Book PPT Workflow

Create book-sharing PPTs with a strict source-grounding rule:

> All chapters, claims, examples, timelines, people, quotes, and conclusions must come from NotebookLM extraction outputs based on the notebook's sources. The agent may organize, compress, and format, but must not add outside knowledge or model memory.

Load `notebooklm` before executing this workflow. Load `powerpoint` when creating/editing/downloading `.pptx` files.

## Output Modes

Ask or infer the mode before outlining:

1. **Original-chapter mode** — follow the book's table of contents / chapter order.
2. **Theme-reconstructed mode** — reorganize by themes for better presentation flow; still map each section back to book chapters/content.
3. **Question-driven mode** — organize around a central question, e.g. “Why is this book worth reading?” or “What can ordinary readers learn?”

Default: **theme-reconstructed mode with chapter/source mapping**.

## Directory Layout

Use one working directory per book:

```bash
OUT=/tmp/book_ppt_<slug>
mkdir -p "$OUT"
```

Save every prompt/output so the final PPT can be audited:

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
prompts.md
slides.pptx / slides.pdf
SUMMARY.md
```

## Workflow

### 0. Verify NotebookLM source

Confirm the notebook and source readiness before asking for content:

```bash
export NOTEBOOKLM_HOME="/Users/lkc/.notebooklm/profiles/default"  # if default auth path fails
notebooklm use <full-notebook-uuid>
notebooklm status
notebooklm source list --json > "$OUT/source_list.json"
```

Write `00_source_check.md` with notebook title, source file names, and status. If sources are not `ready`, wait or stop.

### 1. Extract book structure from NotebookLM

Save as `01_book_structure.md`:

```text
请基于当前笔记本中的书籍来源，提取本书的目录结构或章节结构。

要求：
1. 尽量按照原书顺序列出。
2. 如果原文没有清晰目录，请根据内容识别章节或主要部分。
3. 每章包括：章节标题、核心主题、主要人物/事件/概念、该章在全书中的作用。
4. 不要加入书外信息。
5. 中文输出。
```

### 2. Extract source-grounded content layers

Run these NotebookLM asks as plain text (avoid `--json` for long Chinese answers):

**Core ideas → `02_core_ideas.md`**
```text
请基于当前书籍来源，提炼本书的核心观点。
要求：输出 8-12 条；每条包括观点标题、解释、书中支撑它的事件/案例/论述、适合放入读书分享 PPT 的一句话表达。不要加入书外知识。如果某个观点只是推论，请明确标注“推论”。
```

**Key cases/stories → `03_key_cases.md`**
```text
请基于当前书籍来源，提取本书中最适合读书分享的关键故事、案例或场景。按重要性列出 10-15 个。每个包括：案例名称、出现在哪一部分或章节、发生了什么、说明了什么观点、为什么适合放进 PPT。不要加入书外信息。
```

**Timeline → `04_timeline.md`**
```text
请基于当前书籍来源，整理本书涉及的关键时间线。按时间顺序列出重要事件。每个事件包括：时间或阶段、事件、相关人物、对全书主题的意义、可用于 PPT 的简短表达。如果书中没有明确年份，请用阶段性表述。不要加入书外信息。
```

**People → `05_people.md`**
```text
请基于当前书籍来源，提取本书中的关键人物和他们的作用。每个人包括：身份、与作者/主角/主题的关系、在书中出现的关键事件、代表的观点或作用。不要加入书外信息。
```

**Concepts/frameworks → `06_concepts.md`**
```text
请基于当前书籍来源，提取本书中的关键概念、方法、模型或框架。列出 10-20 个；每个包括概念名称、书中含义、出现场景、相关案例、适合 PPT 的解释方式。不要使用书外定义替代书中语境。
```

**Quotes/expressions → `07_quotes.md`**
```text
请基于当前书籍来源，提取适合读书分享 PPT 使用的金句、关键表达或高度概括的句子。优先提取书中原文或接近原文的表达；如果是总结改写，请标注“改写总结”。不要编造原文引语。
```

**Misreadings/risks → `08_misreadings.md`**
```text
请基于当前书籍来源，整理本书中容易被误解、被过度简化或值得辩论的观点。每个包括：常见误读、书中更准确的说法、为什么容易误解、PPT 中如何表达以避免误导。不要加入书外争议。
```

**Reader takeaways → `09_reader_takeaways.md`**
```text
请基于当前书籍来源，整理普通读者可以从本书中获得的启发。不要鸡汤化，不要脱离书中内容。每条启发必须对应书中的观点、案例或人物经历。输出：启发、来自书中哪类内容、适合放入 PPT 的表达。
```

### 3. Build `10_content_brief.md`

Combine the extracted files into a fact base. Label each section by source file:

```markdown
# 读书分享 PPT 内容事实库

## 1. 书籍来源
...
## 2. 原书结构
来自：01_book_structure.md
...
```

Hard rule: later PPT outputs may only use facts appearing in `10_content_brief.md` or in explicitly referenced NotebookLM extraction files.

### 4. Create slide outline

Generate `11_slide_outline.md` from the content brief:

```text
请基于以下 NotebookLM 已提取内容，设计一套读书分享 PPT 大纲。

要求：
1. 所有内容只能来自给定素材，不得加入外部知识。
2. 每页包括：页码、页面标题、本页核心信息、使用的素材来源、建议图示形式。
3. 输出 12-18 页，适合 20-30 分钟读书分享。
4. 如果某页内容是主题重组，请标注它对应原书的哪些章节或内容。
5. 不要直接写成最终 PPT 文案，先输出大纲。
```

### 5. Create slide script

Generate `12_slide_script.md`:

```text
请基于以下 PPT 大纲和 NotebookLM 内容事实库，生成逐页 PPT 文案。

要求：
1. 每页包含：标题、3-5 个要点、必要解释文字、可选讲稿提示、图示建议、内容来源标记。
2. 所有观点、案例、时间线、人物、概念必须来自内容事实库。
3. 不要加入外部知识。
4. 如果某个表达是总结改写，请标注“总结表达”。
5. 如果某个信息无法在素材中找到，不要补写，标注“素材不足”。
```

### 6. Fact-check before PPT generation

Generate `13_fact_check.md`:

```text
请审查以下 PPT 文案是否完全基于 NotebookLM 内容事实库。

检查：
1. 是否有未在事实库中出现的人物、事件、年份、概念。
2. 是否有过度推断。
3. 是否有把总结改写伪装成原文引用。
4. 是否有与原书结构或核心观点不一致的地方。
5. 是否有投资建议、医学建议、法律建议等不应出现的内容。

输出：问题列表、问题所在页、为什么有问题、建议修改方式。
```

Revise to `14_slide_script_verified.md`. Do not generate the deck until issues are resolved or explicitly accepted.

### 7. Generate PPT

Choose one of two paths:

**A. NotebookLM Slide Deck artifact** — faster, less layout control:

```text
请根据下面这份已经基于本书来源整理好的读书分享 PPT 文案，生成一套中文 Slide Deck。

硬性要求：
1. 只使用下方提供的逐页内容，不要新增人物、事件、年份、案例或观点。
2. 保持每页标题和核心结构。
3. 每页保留足够信息量，不要压缩成轻量卡片。
4. 每页 3-5 个要点，必要时加入简短解释。
5. 如果空间有限，优先保留事实、案例和核心观点，而不是空泛总结。
6. 输出适合 20-30 分钟读书分享的详细幻灯片。
7. 不要加入外部知识。

以下是逐页内容：
[粘贴 14_slide_script_verified.md]
```

Run with `--format detailed --length default --language zh_Hans` and save the artifact ID.

**B. Build `.pptx` directly** — recommended for strict structure/info density. Use `14_slide_script_verified.md` as the only content source, then apply `powerpoint` QA.

### 8. QA

Content QA (`15_ppt_content_qa.md`): check each slide against `14_slide_script_verified.md`; flag new facts, fake quotes, unsupported claims, wrong chronology, or advice.

Visual QA (`16_ppt_visual_qa.md`): check readability, hierarchy, overflow, charts/diagrams, and whether each slide has a clear takeaway.

### 9. Delivery / file handoff

Prefer delivering the original `.pptx` without compression or conversion.

1. **Try the user's requested messaging platform first** with the original file.
2. **If Feishu/Lark rejects or omits the file**, inspect the exact platform error and do not keep retrying the same upload blindly:
   - IM file upload rejects files over 30 MB with `234006 / The file size exceed the max value`.
   - Drive `upload_all` is capped at 20 MB.
   - For files over 20 MB, Drive multipart upload is required, but `upload_prepare` may still return `1061043 / file size beyond limit` if the Feishu tenant is unverified/basic and its cloud-space upload cap is 20 MB.
3. **If the user cannot verify the Feishu organization and still needs the original file**, use one of these non-destructive fallbacks:
   - Upload the original `.pptx` to Google Drive with `gws` CLI, then create an anyone-with-link reader permission and send both preview and download links.
   - Send through another platform with a higher file limit (e.g. Telegram) if connected.
   - Split the binary into sub-limit parts and provide reassembly commands only if the user can merge files locally; verify the reassembled SHA256 matches the original.
   - Use an external temporary file host only as a fallback and label it temporary.

**Google Drive via `gws` delivery recipe**

Use this when `gws` is already configured or the user says they configured it locally:

```bash
# 1) Verify persistent auth; this should show auth_method=oauth2 and token_valid=true
gws auth status

# 2) Test Drive access
gws drive files list --params '{"pageSize": 1, "fields":"files(id,name,mimeType,webViewLink)"}'

# 3) Upload from inside the file's directory. gws rejects --upload paths outside cwd,
# especially macOS /tmp -> /private/tmp symlink paths, so cd first and use ./filename.
cd "$OUT"
gws drive files create \
  --json '{"name":"slides.pptx","mimeType":"application/vnd.openxmlformats-officedocument.presentationml.presentation"}' \
  --upload ./slides.pptx \
  --upload-content-type application/vnd.openxmlformats-officedocument.presentationml.presentation \
  --params '{"fields":"id,name,mimeType,size,webViewLink,webContentLink"}'

# 4) Make the uploaded file readable by link. Replace FILE_ID from step 3.
gws drive permissions create \
  --params '{"fileId":"FILE_ID","fields":"id"}' \
  --json '{"type":"anyone","role":"reader"}'

# 5) Verify final metadata and share links.
gws drive files get \
  --params '{"fileId":"FILE_ID","fields":"id,name,size,mimeType,webViewLink,webContentLink,permissions(id,type,role)"}'
```

Pitfalls:
- If `gws auth status` shows `auth_method: none`, the local OAuth client may exist but the CLI is not logged in. Have the user run/complete `gws auth login --services drive` so `gws` persists credentials; do not rely on one-off authorization-code exchange unless there is no other option.
- If Google returns `403 access_denied` saying the app has not completed verification, add the user's Google account to the OAuth app's **Test users** or publish the OAuth app.
- Do not store or display OAuth codes, client secrets, access tokens, or refresh tokens in skill files, memory, or final summaries.

## Non-negotiable Rules

- Do not write from memory just because the book is familiar.
- Do not infer chapters from the book title.
- Do not add people, years, concepts, examples, or quotes unless NotebookLM extracted them from the sources.
- Keep original quotes separate from paraphrases/summaries.
- If data is missing, write `素材不足`; do not fill gaps.
- Distinguish original-chapter structure from theme-reconstructed structure.
- Preserve intermediate files so the PPT is auditable.

## Field-Tested Pitfalls

- Long Chinese NotebookLM asks can timeout on `GET_NOTEBOOK`; retry the same ask once before changing the prompt.
- Very large pasted briefs can fail silently. In testing, an ~82KB `10_content_brief.md` pasted into `notebooklm ask` produced an empty answer. If this happens, ask NotebookLM to generate the outline from the current book source and the previously extracted fact layers, or pass a compact brief instead of the full file.
- Fact-checking is mandatory, not optional. In a test on 《韦伯作品集：经济与社会》, `13_fact_check.md` caught an externally introduced historical case and a stitched quote masquerading as an original quote. Always revise to `14_slide_script_verified.md` before deck generation.
- Treat NotebookLM extraction files as intermediate hypotheses until fact-checked against the source; extraction itself can still contain hallucinated or over-broad examples.

## Final Summary Template

```markdown
# 读书分享 PPT 生成总结

Notebook: ...
Sources: ...
Mode: original-chapter / theme-reconstructed / question-driven
Generated files: ...
Deck artifact / PPTX: ...
Grounding: all slide content derived from NotebookLM extraction files 01-09 and verified via 13_fact_check.md.
Known limitations: ...
```
