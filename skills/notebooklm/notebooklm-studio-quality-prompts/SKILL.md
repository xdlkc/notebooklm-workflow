---
name: notebooklm-studio-quality-prompts
description: Generate higher-quality NotebookLM Studio artifacts for a notebook or book, including slide decks, reports, mind maps, infographics, data tables, quizzes, flashcards, audio, and video. Use when creating, regenerating, QA-ing, or validating NotebookLM outputs; when the user wants richer, less generic Studio artifacts; or when Chinese Studio infographics need more text without garbled characters.
---

# NotebookLM Studio Quality Prompts

Use this before `notebooklm generate ...` for Studio artifacts. Do not rely on default prompts; default outputs are often generic, shallow, and repetitive.

## Global prompt requirements

Every artifact prompt should specify:

- Audience and use case, e.g. `中文读书分享 / 社群讨论 / 复盘练习 / 课程素材`.
- Output language, normally `中文（简体）`.
- Source grounding: use only the notebook sources; include book-specific concepts, cases, terms, and examples.
- Anti-generic constraint: avoid generic self-help summaries; preserve concrete distinctions, examples, counterexamples, and practice instructions.
- Quality self-check: ask NotebookLM to check missing key concepts, vague statements, duplicated sections, and unsupported claims.

Reusable suffix:

```text
请避免泛泛而谈。必须基于当前 NotebookLM 来源，保留书中的关键概念、区别、例子、练习步骤和容易误解的地方。不要只输出励志口号。输出前自检：是否有具体例子、是否覆盖核心框架、是否有可执行动作、是否删除重复和空话。
```

## Artifact-specific prompt patterns

### Slide Deck

Always choose a PPT mode before generating. If the user says the deck is too short, too sparse, or each page has too little content, regenerate with **Detailed mode**. If the user needs a fast overview or social sharing deck, use **Concise mode**.

**Concise mode** — for quick reading / teaser sharing:
- 10-14 slides.
- Each slide visible body: about 60-100 Chinese characters.
- 2-3 information blocks per slide.
- Focus on one idea per slide; put longer explanation in speaker-note logic.
- Strong visuals, fewer words, no dense tables.

**Detailed mode** — for book sharing / high-information-density presentations:
- 18-24 slides by default; do not accept NotebookLM’s 8-10 page default when the user asks for depth.
- Each slide visible body: about 110-180 Chinese characters; case-study slides may reach about 220 characters if still readable.
- 3-5 information blocks per slide; include at least one concrete source-specific detail, example, contrast, or practice action on most slides.
- Split big ideas into separate slides: framework, mechanism, example, implication, practice.
- Include section-divider slides only when useful; do not waste many pages on decorative dividers.
- Require varied layouts: metaphor scene, process flow, comparison matrix, case storyboard, stakeholder map, decision tree, formula, checklist, timeline, dashboard.
- Forbid pure title+bullet pages and forbid repeated 2×2 card pages.
- Ask NotebookLM to include a final self-check for page count, text density, source specificity, repeated layouts, and text overflow.

Reusable Detailed mode prompt skeleton:

```text
请生成中文详细版 PPT，不是简洁概览。目标是读书分享/课程讲解，信息密度要高。
页数：18–24页。每页正文 110–180 个汉字，案例页可到 220 字，但必须可读。
每页 3–5 个信息块；每页至少包含一个来源中的具体概念、故事、人物、例子、对比或实践动作。
不要只写抽象口号。不要只做10页。不要纯标题+bullet。不要连续使用同一版式。
每页给出具体视觉结构，并让版式在流程图、对比矩阵、案例拆解、棋盘/地图、公式、清单、时间线、关系图之间变化。
最后输出自检：页数是否足够、每页信息是否足够、是否有具体案例、是否有重复版式、是否可能文字溢出。
```

Use strict screen-text and visual-blueprint constraints. Separate screen text from speaker notes. Limit visible text according to the selected mode, require varied visual structures, and forbid repeated simple card layouts. If the deck will be used as PPT, include visual complexity and overflow self-check.

### Report / Study Guide

Prompt pattern:

```text
请生成一份中文深度学习指南，不是普通摘要。结构：
1. 一句话核心问题
2. 全书核心框架图解说明
3. 关键概念分层解释：概念、为什么重要、与相近概念的区别、书中/生活例子
4. 章节脉络与论证推进
5. 典型场景案例拆解：错误表达、NVC改写、背后需要
6. 可练习清单：每天/每周如何练
7. 常见误区与反例
8. 可用于读书分享的金句和讨论问题
要求：中文；保留具体事实和案例；每节至少有一个例子；避免鸡汤化。
```

### Mind Map

Prompt pattern:

```text
请生成中文思维导图，要求层级清楚且不扁平：
第1层：核心问题、核心框架、关键技能、典型障碍、练习路径、应用场景。
第2层：每类下列出具体概念。
第3层：为重要概念补充区别/例子/操作动作。
避免只列名词；每个叶子节点尽量是可理解短语。
```

### Infographic

Prompt pattern:

```text
请生成中文信息图，目标是让读者一眼理解本书方法论。要求：
- 选择一个明确视觉隐喻，不要做普通摘要海报。
- 必须包含：核心框架、关键步骤、常见错误、一个具体例子、实践动作。
- 版式要有信息层级：主标题、主流程、对比/警示区、行动清单。
- 避免小字堆砌；每个文本块短而具体。
- 风格专业、适合读书分享，不要幼稚卡通。
```

For Chinese infographics, add stricter text-fidelity constraints when quality matters or a previous image had garbled/incorrect Chinese:

```text
中文文字必须清晰、简短、可读，不能出现乱码、错字、拼音、英文混杂或截断。
请做“少字大图版”：全图最多 12 个中文文本块，每个文本块不超过 8 个汉字；不要小字段落、脚注式小字或装饰性碎字。
优先用视觉隐喻、流程箭头、对比区和图标表达信息，而不是堆文字。
```

When the user explicitly wants **NotebookLM Studio-native / 原汁原味** output and also wants **more text / high information density**, do not switch to external rendering unless the user allows it. Instead use a Studio-safe high-text strategy:

1. Generate multiple Studio variants in parallel or sequence (at least 2-4) and QA each downloaded PNG visually.
2. Prefer `--style bento-grid` or `--style professional` with a table/card layout over wall-of-text, hand-drawn, or complex textured layouts; these reduce Chinese rendering errors.
3. Give NotebookLM fixed copy to reuse rather than letting it freely compose long Chinese sentences. Use sections like `第一分区`, `卡片1`, `标题`, `说明`, and short but information-bearing lines.
4. Use one of these two text budgets depending on the user's tolerance:
   - balanced: 16-20 text blocks, each 4-12 Chinese characters;
   - high-text card/table: 4 sections, each card has title line + explanation line, each line 4-12 Chinese characters.
5. Prefer explicit card copy in the form `卡片1：标题 / 说明` or `标题：... 说明：...`. In field tests, a four-section/twelve-card bento grid with fixed copy was more stable than a `问题/答案` twelve-question table: even when copy was supplied, Q&A layouts caused character substitutions such as wrong final words or duplicated characters.
6. Avoid long paragraphs, footnotes, decorative microtext, handwriting-style small text, pinyin, and English except the NotebookLM brand mark. Also avoid repeated decorative slogans around the main visual; they often become duplicated or garbled.
7. Generate at least two variants for high-text Chinese infographics and visually QA every downloaded PNG. Treat a single obvious wrong character as a fail even if the layout is attractive.
8. If a candidate has no乱码 but a few stiff phrases, it may be preferable to a prettier candidate with obvious错字/乱码. Choose the best Studio-native result only after visual QA.

Reusable high-text Studio infographic prompt skeleton:

```text
请生成中文 NotebookLM Studio 原生信息图。目标是“字多、清晰、无乱码”的读书分享速查图。
请尽量只使用下面给出的中文文案，不要自由改写成长句。
版式：竖版；四个大分区；卡片式/表格式；每区颜色不同；适合手机阅读。
文字规则：每个卡片标题一行 + 说明一行；每行 4–12 个汉字；清晰印刷体；不要手写小字、英文、拼音、脚注、装饰小字、截断文字。
[分区标题与卡片文案逐条列出]
视觉要求：NotebookLM Studio 原生；卡片边界清楚；图标辅助理解；文字占约 50%，图形图标占约 50%。
```

### Data Table

Prompt pattern:

```text
请生成中文结构化表格，用于复习和制作二次内容。列必须包括：
概念 | 精确定义 | 易混淆点 | 书中/生活场景 | 错误表达示例 | 更好的表达 | 可练习动作 | 适用场景
要求至少覆盖核心框架、关键技能、常见误区和应用场景。每一行都要具体，不要只有一句抽象解释。
```

### Quiz

Prompt pattern:

```text
请生成中文测验，目标是检验是否真正理解，而不是背概念。题型混合：
- 概念辨析题
- 场景判断题
- 表达改写题
- 多选陷阱题
- 简答题
每题给出答案和解析，解析必须说明为什么其他选项不合适。覆盖核心概念、常见误区和实践应用。
```

### Flashcards

Prompt pattern:

```text
请生成中文抽认卡，用于主动回忆和练习。卡片类型混合：
- 概念定义卡
- 区别辨析卡
- 场景应用卡
- 表达改写卡
- 误区提醒卡
每张卡正面必须是具体问题，背面包含简明答案 + 例子/提示。避免正面只是“什么是X”的低难度卡。
```

### Audio Overview

Prompt pattern:

```text
请生成中文音频概览脚本，形式像高质量读书播客。要求：
- 开头用一个真实沟通困境引入，不要百科式介绍。
- 两位主持人应有分工：一人追问和质疑，一人解释框架。
- 每个核心概念都配一个生活场景。
- 加入误区纠偏和实践建议。
- 语气自然，但信息密度高，避免鸡汤。
```

### Video Overview

Prompt pattern:

```text
请生成中文视频讲解，要求有明确分镜：开场问题、核心框架、案例演示、错误与改写、练习步骤、结尾行动。
每段说明画面应该展示什么，不要只做旁白摘要。视觉风格应服务于概念理解。
```

For higher-quality NotebookLM video overviews, make the prompt storyboard-like rather than encyclopedia-like:

- Start with a concrete conflict or user pain point, not a definition.
- Require 6-8 segments: hook, problem, core framework, one source-specific case, wrong expression vs better expression, practice steps, recap/action.
- For every segment, specify `画面元素`, `旁白重点`, and `观众要记住的一句话`.
- Ask for book-specific examples and terms; avoid generic motivational advice.
- Prefer visual styles that support conceptual explanation (`whiteboard`, `classic`, `paper-craft`, or `watercolor`) over purely decorative styles.
- After video generation, create a companion “视频卡片/分镜卡” via `notebooklm ask` so the user can review, repurpose, or remake the video:

```text
请基于当前来源，生成一份中文“视频卡片/分镜卡”脚本，用于配合视频概览交付。要求：8张卡片，每张包括：卡片标题（不超过10字）、画面元素、旁白要点、一个来自来源的实践动作。结构覆盖：开场冲突、核心障碍、核心框架、具体案例、错误与改写、练习步骤、常见误区、结尾行动。不要泛泛鸡汤，保持高信息密度但每张卡片简短。
```

Quality gate for video deliverables:

- Verify the artifact status is `completed` before download.
- Download the MP4 and check duration/size with `ffprobe` when available.
- Prefer uploading the original MP4 first with a generous Drive upload timeout; a ~55 MB NotebookLM video can upload successfully when the network is stable. Compress only after a real upload failure or if the user asks for a smaller review copy.
- If Drive upload of the original MP4 fails due to size/network reset, keep the original local file and upload a clearly labeled compressed review copy; see `notebooklm-artifacts-to-drive` for the ffmpeg compression pattern.
- Deliver both the video and the companion video-card Markdown when the user says “视频卡片/视频卡卡”.

PPT/slide-deck QA for NotebookLM Studio validation:

- Download PPTX when available, not only PDF.
- Verify archive integrity with `unzip -t`.
- Count slides and embedded media from the PPTX archive. NotebookLM decks are often image-based, with one large slide image per slide:
  ```bash
  python3 - <<'PY'
  import zipfile, re, json
  ppt='/path/to/slides.pptx'
  with zipfile.ZipFile(ppt) as z:
      slides=[n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
      media=[n for n in z.namelist() if n.startswith('ppt/media/')]
      print(json.dumps({'slide_count':len(slides),'media_count':len(media)}, indent=2))
  PY
  ```
- For image-based NotebookLM decks, extract embedded slide images and create a contact sheet; inspect for overflow, truncation, Chinese rendering errors, excessive text-only slides, and layout repetition before delivery. If Pillow is unavailable, make a lightweight HTML contact sheet from extracted `ppt/media/*` images and inspect it with browser vision:
  ```bash
  python3 - <<'PY'
  import zipfile, re, shutil
  from pathlib import Path
  ppt=Path('/path/to/slides.pptx')
  out=Path('/tmp/ppt_media'); shutil.rmtree(out, ignore_errors=True); out.mkdir()
  imgs=[]
  with zipfile.ZipFile(ppt) as z:
      for n in z.namelist():
          if n.startswith('ppt/media/') and n.lower().endswith(('.png','.jpg','.jpeg')):
              p=out/Path(n).name; p.write_bytes(z.read(n)); imgs.append(p)
  imgs=sorted(imgs, key=lambda p:int(re.search(r'(\d+)',p.name).group(1)) if re.search(r'(\d+)',p.name) else 0)
  html=['<!doctype html><meta charset="utf-8"><style>body{font-family:sans-serif;background:#eee}.grid{display:grid;grid-template-columns:repeat(3,420px);gap:14px}.card{background:white;padding:8px}.card img{width:400px;height:auto;border:1px solid #ccc}.n{font-size:18px;font-weight:bold}</style><div class=grid>']
  for i,p in enumerate(imgs,1): html.append(f'<div class=card><div class=n>Slide {i}</div><img src="{p.as_uri()}"></div>')
  html.append('</div>')
  Path('/tmp/ppt_contact_sheet.html').write_text('\n'.join(html),encoding='utf-8')
  print('/tmp/ppt_contact_sheet.html')
  PY
  ```
- Record pass/fail notes in a short validation summary when testing prompts across multiple artifacts.

## Generate-all workflow

1. Locate the exact notebook, set context with the full UUID, and verify sources are `ready` before generating:
   ```bash
   NOTEBOOKLM_HOME=/path/to/home notebooklm list --json > "$OUT/notebooks.json"
   NOTEBOOKLM_HOME=/path/to/home notebooklm use <full-notebook-uuid>
   NOTEBOOKLM_HOME=/path/to/home notebooklm source list --json > "$OUT/sources.json"
   NOTEBOOKLM_HOME=/path/to/home notebooklm artifact list --json > "$OUT/artifacts_before.json"
   ```
2. Create a local `prompts.md` recording exact prompts for every artifact, plus per-artifact prompt files if the prompts are long.
3. Generate fast/sync artifacts first: mind map, report, data table.
4. Generate heavier artifacts separately: slide deck, infographic, quiz, flashcards, audio, video. Save every `--json` response and artifact ID.
5. Wait for completed artifacts where useful; record artifact IDs and statuses. For mixed Studio batches such as PPT + video + infographic, download fast-completed artifacts (often infographic) immediately and QA them while slide deck/video continue running.
6. If slide deck/video/audio or other long artifacts are still `pending`/`in_progress` near the end of the conversation, do not just promise to check later. Persist a self-contained working directory with prompts, notebook ID, artifact IDs, status files, and a wait/download/upload script. Schedule a one-shot follow-up cron job (or equivalent background handoff) to re-check artifact status, download completed outputs, verify them, upload to Drive, and report links back to the originating conversation.
7. Download each artifact in useful formats: PPTX and PDF for slide decks, MP4 for video, PNG for infographic.
8. Verify downloads: `unzip -t` for PPTX, `ffprobe` duration/size for MP4 when available, and visual QA for Chinese PNG/PPT slide images.
9. Upload with `notebooklm-artifacts-to-drive` using `NotebookLM/<notebook name>/<artifact file>`.
10. If outputs are generic, visually broken, garbled, or too sparse, revise prompts before regenerating rather than accepting defaults.

## Quality gate before delivery

Check the downloaded outputs for:

- Does the output contain book-specific concepts and examples?
- Does it include practice or application, not only summary?
- Are distinctions and misconceptions explicit?
- Are there enough concrete cases for reuse in PPT/social posts/discussion?
- For visual artifacts, is the result more than a simple title + blocks layout?
- For Chinese visual artifacts, inspect the rendered/downloaded file for乱码、错字、截断、小字过多. If any are visible, do not deliver it as final; regenerate with a short-text prompt and stronger text-fidelity constraints.

If the answer is no, regenerate the weak artifact with a stricter prompt.