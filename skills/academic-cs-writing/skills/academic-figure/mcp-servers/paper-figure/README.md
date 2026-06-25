# paper-figure MCP（中文）

English: [README_EN.md](README_EN.md)

这是给 `academic-writing` skill 使用的窄范围 MCP 图表辅助服务。

它只处理 display 相关工作：

- 将图/表想法分类为 plot、schematic、picture 或 table 路线。
- 基于内置模板生成 FigureSpec JSON 骨架，支持 pipeline/framework、architecture、taxonomy、benchmark-construction 或 minimal custom diagram。
- 校验并渲染中等复杂度的 FigureSpec JSON，输出可编辑的学术风格 SVG diagram。
- 生成 Picture Brief Markdown，包含给 AI 生成论文图片使用的 Direct Image Prompt。

它不写论文正文，不编造 claim 或结果，不管理论文工作流，也不调用图像生成 API。Picture Brief 只记录 renderer route；真正的图片生成由外部 renderer 或当前 agent 执行。

## 注册

```bash
codex mcp add paper-figure -- python3 /path/to/academic-writing/mcp-servers/paper-figure/server.py
```

非 Codex host 使用对应的 MCP 注册命令。

## Tools

- `classify_figure`
- `write_figurespec_skeleton`：可选 `template` 值包括 `pipeline`、`architecture`、`taxonomy`、`benchmark`、`minimal`。
- `write_picture_brief`
- `render_figurespec`：把 FigureSpec JSON 渲染为适合论文使用的可编辑 SVG diagram。

## 输出策略

服务只会写入调用方提供的 `cwd`。推荐路径：

```text
paper/figures/specs/<figure-id>.json
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
```

`write_picture_brief` 会根据 `GEMINI_API_KEY`、`OPENAI_API_KEY` 以及可选的 provider/model/base-url 环境变量记录图片路线，但不会调用 provider。

`render_figurespec` 适合确定性架构图、pipeline 图、workflow 图和 taxonomy schematic。复杂、密集或强注释图可以先用 FigureSpec 生成起点，再转为手写 SVG 或 TikZ。
