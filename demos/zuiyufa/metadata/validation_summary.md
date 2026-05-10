# 《罪与罚》NotebookLM Workflow 实测验证摘要

生成时间：2026-05-10 21:02:36 CST

## Notebook
- 标题：《罪与罚》NotebookLM Workflow 实测 Demo
- Notebook ID：6302f94b-2292-4b6a-a642-ac916368845d
- Source ID：f9163618-e9d2-4b0d-92e2-aa56f0e57202
- Source 状态：ready

## 本地素材
- EPUB：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/source/Crime and Punishment (Dostoevsky, Fyodor [Dostoevsky, Fyodor]).epub
- PDF Source：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/source/crime_and_punishment_dostoevsky.pdf（424 页）
- PPTX：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/downloads/crime_and_punishment_slide_deck.pptx（20 slides）
- PPT PDF：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/downloads/crime_and_punishment_slide_deck.pdf（20 pages）
- 最终信息图：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/downloads/crime_and_punishment_infographic_final_minimal.png（1536 x 2752 PNG）
- 视频：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/downloads/crime_and_punishment_video.mp4（MP4，1280x720，约 414.9 秒，含 H.264 视频流和 AAC 音频流）

## QA 结论
- EPUB 下载：通过。
- EPUB 转 PDF：通过；Calibre 转换有封面图片缺失警告，但正文 PDF 成功生成。
- NotebookLM Source：通过，状态 ready。
- PPT：通过；PPTX zip 校验无错误，20 张幻灯片，导出 PDF 20 页，contact sheet 图片加载正常。
- 信息图：最终最小文案版通过；保留 NotebookLM 自动水印以维持 Studio-native/原汁原味输出。初版和第一次 retry 均未交付，原因是中文文字错误。
- 视频：通过；ffprobe 显示 H.264 1280x720 视频流、AAC 单声道音频流，时长约 414.9 秒。

## 卡点与修复
1. zlib 普通下载要求 TTY，非交互环境失败；改用 skill 内 noninteractive_download.go。
2. ebook-convert 不在 PATH；改用 Calibre app 内置命令。
3. NotebookLM auth profile 有嵌套目录；改用正确 NOTEBOOKLM_HOME。
4. NotebookLM PDF 上传出现 RPC timeout；显式指定 file 类型和 PDF MIME 后成功。
5. artifact list 间歇性 RPC timeout；通过重试、轮询和状态文件复验处理。
6. 信息图中文稳定性不足；没有绕过质量闸门，而是缩短固定文案后重新生成。

## 校验文件
- Manifest：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/manifest.json
- Checksums：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/checksums.sha256

## Google Drive 交付
- 文件夹：NotebookLM/《罪与罚》NotebookLM Workflow 实测 Demo
- 文件夹链接：https://drive.google.com/drive/folders/1KgS1J-hNcQxYbzd9Ftx5chsRCWVQ0f4R
- 明细：/Users/lkc/Code/notebooklm-workflow/.work/crime-and-punishment/drive_uploads.json
