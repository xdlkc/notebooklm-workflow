请生成中文视频讲解，形式是 NotebookLM Studio 原生 video overview。目标是用《罪与罚》展示 notebooklm-workflow 的真实端到端流程：zlib 下载 EPUB、EPUB 转 PDF、PDF 上传 NotebookLM、生成 PPT/信息图/视频、复验、上传 Google Drive，最后才写文章大纲。

来源约束：关于小说内容，只使用当前 NotebookLM 来源。不要加入书外知识、百科背景或不在来源中的细节。关于 workflow 的步骤，可按当前任务给定流程解释。

请按 7 个分镜组织：
1. Hook：一本厚小说不是只要“总结”，而是要变成可讲、可看、可交付的一组材料。画面：书本进入流水线。
2. Source：以《罪与罚》为例，先准备 EPUB，再转成 PDF，上传到 NotebookLM。画面：EPUB、PDF、Notebook 三个节点。
3. Ready Gate：source ready 后才生成，避免还没索引就产出。画面：绿色通过闸门。
4. Novel Core：用拉斯柯尔尼科夫、索尼娅、波尔菲里三条人物张力说明小说不是简单犯罪故事。画面：三角关系。
5. Artifact Matrix：PPT 适合读书分享，信息图适合快速传播，视频适合异步讲解。画面：三类产物卡片。
6. QA：PPTX 要检查，信息图要看中文有没有错字，视频要确认状态和时长。画面：检查清单。
7. Delivery：验证通过后上传 Google Drive，再把实测链路写进项目文章大纲。画面：Drive 文件夹与文章大纲。

每段都要有：画面元素、旁白重点、观众要记住的一句话。语气自然、信息密度高，不要鸡汤。