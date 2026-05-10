---
name: notebooklm-rich-slide-decks
description: Generate or redesign high-information-density NotebookLM Slide Deck/PPT artifacts instead of sparse, repetitive, text-heavy card-style decks. Use when the user says NotebookLM/PPT/slide deck has too little information, too few pages, every page looks similar, the deck is all text, wants concise and detailed PPT variants, wants a richer/deeper deck, wants to regenerate slides with more substance, or needs a 20-50 minute book/article/research presentation from NotebookLM sources.
---

# NotebookLM Rich Slide Decks

Use this skill when creating or regenerating NotebookLM Slide Deck artifacts where information density matters. It complements the general `notebooklm` and `powerpoint` skills.

## Workflow

### A. Choose concise vs detailed mode first

When generating NotebookLM Slide Decks, explicitly choose a mode instead of relying on NotebookLM defaults:

- **Concise mode**: use when the user wants a quick overview, teaser, social-sharing deck, or “简洁版”. Target 10-14 slides, 60-100 visible Chinese characters per slide, 2-3 information blocks per slide, strong visuals, and one core idea per page.
- **Detailed mode**: use when the user says the deck has too few pages, too little content per page, is too sparse, or asks for “详细版/读书会/课程讲解/高信息密度”. Target 18-24 slides, 110-180 visible Chinese characters per slide, 3-5 information blocks per slide, and source-specific concepts/cases/practice actions on most pages.

If the user asks for both, generate and label both versions separately (e.g. `*_简洁版.pptx` and `*_详细版.pptx`) and upload both to Drive.

### B. Regenerate when the problem is information density

Use this path when the deck is too sparse, too short, or missing important source details.

1. Load `notebooklm` before using NotebookLM CLI.
2. Identify the target notebook and verify sources are ready:
   ```bash
   export NOTEBOOKLM_HOME="$HOME/.notebooklm/profiles/default"  # optional: set to your authenticated NotebookLM profile root
   notebooklm use <full-notebook-uuid>
   notebooklm status
   notebooklm source list --json
   ```
3. If the existing deck is sparse, inspect the prior prompt/logs if available. Sparse decks often come from words like:
   - `短幻灯片`
   - `简洁`
   - `小红书卡片`
   - `适合8页卡片`
   - `概览`
4. Write a richer prompt to a file before generating, so it can be shared later:
   ```bash
   OUT=/tmp/notebooklm_<topic>_studio
   mkdir -p "$OUT"
   $EDITOR "$OUT/rich_slide_deck_prompt.md"
   ```
5. Generate a detailed default-length slide deck:
   ```bash
   PROMPT=$(python3 - <<'PY'
   from pathlib import Path
   print(Path('/tmp/notebooklm_<topic>_studio/rich_slide_deck_prompt.md').read_text().strip())
   PY
   )
   notebooklm generate slide-deck "$PROMPT" --format detailed --length default --language zh_Hans --retry 2 --json \
     | tee "$OUT/rich_slide_deck.json"
   notebooklm artifact list --json > "$OUT/artifacts_after_rich_slide_deck.json"
   ```
6. Return the new `task_id`/artifact ID and current status. Do not wait in the main conversation unless the user explicitly asks.
7. When complete, optionally download:
   ```bash
   notebooklm download slide-deck "$OUT/slides.pdf" -a <artifact_id> -n <notebook_id>
   notebooklm download slide-deck "$OUT/slides.pptx" --format pptx -a <artifact_id> -n <notebook_id>
   ```

### B. Redesign when the problem is repetitive/text-heavy visuals

Use this path when the user says the PPT “每页都差不多”, “都是文字”, “像 Word”, “模板化”, or otherwise criticizes slide design rather than source depth. NotebookLM's Slide Deck generator often improves content density but still produces repetitive text-card pages; do not keep regenerating the same style.

1. Load `powerpoint` and, if the deck came from NotebookLM, load `notebooklm` only to identify/download the completed slide deck/report/source artifacts. If the user refers vaguely to “你发的那个 PPT”, “那个 PPT”, or “this deck”, first identify the exact deck/book from recent files, session history, filenames, or artifact titles; when multiple recent decks exist, state the inferred title before rebuilding or ask a targeted clarification instead of redesigning the wrong presentation.
2. Treat the NotebookLM deck/report/extraction outputs as the content brief, but rebuild a new `.pptx` directly for layout control. Prefer source-grounded content from `notebooklm-book-ppt-workflow` if available.
3. Create a topic-specific visual system: palette, motif, and slide archetypes. For book-sharing decks, vary slides across at least these kinds of layouts:
   - cover visual metaphor
   - why-it-matters / 3-column framing
   - timeline
   - method loop or causal model
   - process/experiment flow
   - comparison table
   - mechanism diagram
   - variable/relationship map
   - risk or decision dashboard
   - takeaway/conclusion page
4. Keep information density, but convert paragraphs into visual structures: cards, grids, flows, callouts, diagrams, comparison rows, and large concept labels. Avoid text-only slides and avoid using the same card grid repeatedly.
5. QA loop:
   - Verify archive integrity with `unzip -t output.pptx`.
   - Run a programmatic bounds/shape/text sanity check when using `python-pptx`.
   - Render or thumbnail inspect. On macOS, if LibreOffice/markitdown are unavailable, `qlmanage -t -s 1200 -o previews output.pptx` can at least create a Quick Look thumbnail for visual inspection; use full slide rendering when available.
   - Fix at least one visual issue found during inspection, then re-run the affected QA.

## Rich Deck Prompt Template

Adapt this template to the book/topic. Replace bracketed fields and add domain-specific subtopics.

```text
请生成一套信息量充足的中文详细版幻灯片，用于 35-50 分钟读书分享/课程讲解，而不是轻量卡片或概览。主题：「[主题]」。

页数与密度：
1. 页数目标 18-24 页，不要只生成 8-10 页。
2. 每页正文约 110-180 个汉字；案例拆解页可到 220 字但必须可读。
3. 每页 3-5 个信息块；每页至少包含一个来源中的具体概念、故事、人物、例子、对比或实践动作。
4. 不要只做概览，要展开关键细节：[列出必须覆盖的事件、概念、人物、方法、案例、时间线]。

结构建议：
- 封面
- 为什么这个主题重要
- 总框架/核心问题
- 关键机制 1：框架 + 例子
- 关键机制 2：机制 + 反例
- 关键案例/转折点（可拆多页）
- 角色/利益相关方关系图
- 方法论/公式/模型
- 风险、限制或常见误读
- 普通读者/听众能学到什么
- 讨论问题或实践清单
- 总结：如何把本主题用于理解现实问题

视觉要求：
- 不要纯标题+bullet，不要连续使用同一版式。
- 每页给出具体视觉结构，在流程图、对比矩阵、案例拆解、地图/棋盘、公式、清单、时间线、关系图之间变化。
- 风格：知识密度高、适合读书会/课程分享、中文表达自然、有故事性但不鸡汤。
- 避免不可靠承诺、夸张营销和未经来源支持的结论。
- 如果资料允许，请尽量引用来源中的具体事件、人物、年份、案例和方法。

最后输出自检：页数是否足够、每页信息是否足够、是否有具体案例、是否有重复版式、是否可能文字溢出。
```

For a concise version, explicitly ask for 10-14 slides, 60-100 visible Chinese characters per slide, 2-3 information blocks, and one idea per slide; label it separately from the detailed version.

## Example: 《战胜一切市场的人》

```text
请生成一套信息量充足的中文深度幻灯片，用于 20-30 分钟读书分享，而不是小红书轻量卡片。主题：「《战胜一切市场的人》：爱德华·索普如何把概率、数学和风险控制用于赌场与金融市场」。

要求：
1. 每页包含明确标题、3-5 个要点、必要的解释文字和例子。
2. 不要只做概览，要展开关键细节：索普的成长背景、二十一点计数策略、可穿戴计算机、赌场优势、转向华尔街、可转债套利、期权定价、量化投资、市场中性、风险控制、资金管理、长期复利。
3. 结构建议：封面、为什么这本书重要、索普是谁、从物理/数学到赌场、二十一点与概率优势、可穿戴计算机与轮盘实验、从赌场到华尔街、可转债套利与市场中性、期权定价和量化投资启蒙、风险控制与资金管理、索普与凯利公式/长期复利的关系、普通读者能学到什么、常见误读：这不是发财秘籍、总结：如何用概率思维面对不确定性。
4. 风格：知识密度高、适合读书会/课程分享、中文表达自然、有故事性但不鸡汤。
5. 避免具体投资建议、荐股和收益承诺。
6. 如果资料允许，请尽量引用书中具体事件、人物、年份、案例和方法。
```

## Pitfalls

- `--length short` and prompts mentioning `卡片` or `简洁` tend to create sparse decks.
- A rich thematic outline is not necessarily the book's original chapter order. If the user asks whether slides follow the source text/chapters, explicitly verify against the source list/fulltext or table of contents, and regenerate with wording like `请严格根据原书目录/章节顺序组织，不要自行改编章节结构` when chapter fidelity matters.
- NotebookLM generation is long-running and may stay `pending`/`in_progress`; report IDs instead of blocking. If `notebooklm artifact wait` fails with transient `RPC LIST_ARTIFACTS` / connection errors, do not assume failure: retry `notebooklm artifact list --json` after a short delay and check the target artifact ID. Once `status=completed`, download directly by `-a <artifact_id>`.
- Quiz/flashcards do not support `--language`, but slide-deck does; use `--language zh_Hans` for Chinese slides.
- Use full notebook UUIDs. Partial IDs can fail or target the wrong notebook.
- Downloading PPTX is possible via CLI even if the web UI only shows PDF.
- For QA of NotebookLM image-based PPTX exports, verify `unzip -t`, count slides with `python-pptx`, extract embedded slide images, make a contact sheet, and visually inspect for: page count vs requested mode, content density, overflow/truncation, Chinese乱码/错字, layout repetition, and text-only pages before uploading.
