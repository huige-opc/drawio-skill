# drawio-skill

本地 draw.io 技能包：让 AI 生成可编辑的 `.drawio` 文件，并可选配一个完全离线的本地 webapp 来编辑、渲染和导出。

适用于任何支持 `SKILL.md` 的 Agent（WorkBuddy、Claude Code、Codex 等），不依赖 draw.io 官网，也不需要安装 draw.io 桌面版。

## 能做什么

- 生成/修改 `.drawio`：架构图、流程图、时序图、ERD、UML、BPMN、泳道图、甘特图、思维导图等。
- 从代码、SQL、OpenAPI、Terraform、K8s 等来源生成图。
- 左右脑图可直接出 PNG/PDF（内置 `mindmap-svg`，只需要 Chrome）。
- 可选本地 webapp：打开 `.drawio`，导出 PNG / SVG / JPG / PDF，保存直接到本机。

## 适合谁

- 用支持技能的 Agent，想让 AI 直接产图的用户。
- 需要可编辑图源文件，而不是一张死图片的人。
- 不想连 draw.io 官网、不想装桌面版的人。

## 快速开始

### 1. 导入技能

从 Releases 下载 `drawio-skill-vX.zip`，解压后把里面的 `drawio/` 文件夹导入你的 Agent。

任何支持 `SKILL.md` 的工具都用同一套方法：文件夹根目录有 `SKILL.md`，技能名是 `drawio`。

### 2. 可选：安装本地 webapp

需要导出 `.drawio` 为图片时再装：

1. 从 Releases 下载 `drawio-webapp-vX-win.zip`。
2. 解压到任意目录。
3. 双击 `启动本地drawio.bat`。
4. 浏览器打开 `http://127.0.0.1:8130/local.html`。

前提：Python 3 和 Chrome。macOS/Linux 可以运行 `python serve.py 8130`。

不装 webapp 也能用技能生成 `.drawio`，只是导出图片需要你自己用 draw.io 打开。

### 3. 开始使用

直接对模型说需求，例如：

- 「把这张流程图画成 `.drawio`」
- 「画一个三层架构图：前端、API、数据库」
- 「画一个下单流程的时序图」
- 「做一张 8 周的内容生产甘特图」
- 「做一张左右脑图，主题是 AI 工作流，导出 PNG」
- 「把 Redis 移到左边，颜色换成青色」

## 环境要求

| 功能 | 需要 |
| --- | --- |
| 生成 `.drawio` | Python 3.10+（技能脚本） |
| 脑图导出 PNG/PDF | Python 3 + Chrome |
| `.drawio` 导出 PNG/SVG/JPG/PDF | 本地 webapp 或任意 draw.io 客户端 |

## 目录结构

```
skills/drawio/
  SKILL.md              技能入口
  LOCAL_SETUP.md        本地环境说明
  scripts/              生成/转换/校验脚本
  references/           图型、布局、样式规则
  assets/mindmap-svg/   左右脑图离线渲染器
build_release.py        打包技能包和 webapp 包
build_assets/licenses/  打包用许可证
```

`webapp/` 和 `dist/` 不提交到仓库：webapp 走 Release 附件，dist 是构建产物。

## 自己构建

需要本地先有 `webapp/` 目录（官方 draw.io webapp 解压版）。

```bash
python build_release.py
```

输出：

- `dist/drawio-skill-vX.zip`
- `dist/drawio-webapp-vX-win.zip`
- `dist/SHA256SUMS.txt`

## 常见问题

**导入后没反应？**
确认 Agent 导入的文件夹根目录有 `SKILL.md`，且 `name: drawio`。

**不能导出图片？**
确认本地 webapp 已启动，或直接用 draw.io 打开 `.drawio` 导出。

**没有 Python？**
技能脚本和 webapp 都需要 Python 3；先安装 Python。

**8130 端口被占用？**
换端口运行 `python serve.py 8131`，并让模型使用对应地址。

## 许可证

- 技能与本地新增代码：MIT
- draw.io webapp：Apache License 2.0
- jsPDF：MIT

详见 `LICENSE`、`THIRD_PARTY_NOTICES.md` 和 Release 包内的 `LICENSES/`。
