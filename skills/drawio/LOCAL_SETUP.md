# 本地环境

本技能默认运行在用户本机，路径都相对本文件所在目录。

## 前提

- Python 3.10+
- Chrome（脑图导出 PNG/PDF 用；找不到时可设 `CHROME` 环境变量）
- 可选：本地 draw.io webapp（`http://127.0.0.1:8130/local.html`），用于渲染/导出 `.drawio`

## 检查

```bash
python scripts/check_webapp.py
```

显示 `webapp: ready` 就可以自动渲染；`not running` 时先产 `.drawio` 源文件，
再让用户启动本地 webapp，或用 draw.io 桌面版/网页版导出。

## 左右脑图（离线，不需要 webapp）

```bash
python assets/mindmap-svg/render_mindmap.py input.json out --png --pdf
```

## 其他图型

1. 用本技能生成 `.drawio`。
2. 需要 PNG/SVG/JPG/PDF 时：
   - 本地 webapp 在跑：打开 `http://127.0.0.1:8130/local.html`，导入后导出；
   - 没装：用 draw.io 桌面版/网页版打开 `.drawio` 导出；
   - 用户可以另外下载可选的本地 webapp 包。
