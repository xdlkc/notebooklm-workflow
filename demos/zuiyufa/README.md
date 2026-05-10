# 《罪与罚》NotebookLM Workflow 实测 Demo

这个目录收集《罪与罚》端到端实测所用素材，供公众号/博客项目分享文章和后续 demo 整理使用。

## 目录结构

- `source/`：本次实测使用的 EPUB 和转换后的 PDF source 不提交到公开仓库；文章只保留 NotebookLM/Drive 产物与验证记录，避免把资料来源合规问题变成主题。
- `prompts/`：PPT、信息图、视频及信息图 retry/final 版本的 NotebookLM Studio prompts。
- `drive_outputs/`：最终通过 QA 并上传 Google Drive 的产物，包含 PPTX、PDF、PNG、MP4。
- `review_outputs/`：QA 未通过但用于文章说明“质量闸门”的信息图初版和 retry 版。
- `ppt_previews/`：PPT contact sheet 和从 PPTX 提取的 20 张 slide 预览图。
- `metadata/`：Notebook/source/artifact 状态、manifest、validation summary、checksums 等。
- `logs/`：生成、下载、上传、timeout/retry 相关日志和状态文件。

## Google Drive 交付目录

NotebookLM/《罪与罚》NotebookLM Workflow 实测 Demo

https://drive.google.com/drive/folders/1KgS1J-hNcQxYbzd9Ftx5chsRCWVQ0f4R

## 核心产物

- PPTX：`drive_outputs/crime_and_punishment_slide_deck.pptx`
- PPT PDF：`drive_outputs/crime_and_punishment_slide_deck.pdf`
- 最终信息图：`drive_outputs/crime_and_punishment_infographic_final_minimal.png`
- 视频：`drive_outputs/crime_and_punishment_video.mp4`
- 验证摘要：`metadata/validation_summary.md`
- 工作流 manifest：`metadata/manifest.json`
- Demo inventory：`demo_manifest.json`

## QA 备注

- 初版信息图和第一次 retry 信息图保存在 `review_outputs/`，用于说明真实 workflow 中“生成成功”不等于“质量通过”。
- 最终信息图采用极简固定中文文案，中文内容 QA 通过；保留 NotebookLM 原生水印以保持 Studio-native 输出。
- PPT 已验证 20 slides，PPTX zip 校验通过，PDF 为 20 pages，预览图正常。
- 视频已验证为 MP4，1280x720，约 414.9 秒，含 H.264 视频流和 AAC 音频流。

## 注意

当前目录包含较大的 NotebookLM 原始输出文件，适合本地 demo/文章素材整理。公开仓库不提交 EPUB/PDF source；如需复现实验，请使用用户已有文件或合规电子书来源。
