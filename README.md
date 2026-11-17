# drawio-skill

本地 draw.io 技能包：生成/编辑 `.drawio`，附带可选的本地 webapp 用于渲染和导出。

## 下载

- **技能包**：`drawio-skill-vX.zip` → 解压后把 `drawio/` 文件夹导入 WorkBuddy（含 `SKILL.md`）。
- **可选 webapp**：`drawio-webapp-vX-win.zip` → 解压，双击 `启动本地drawio.bat`。
  需要 Python 3 和 Chrome；不装也能用技能生成 `.drawio`，只是不能本地导出图片。

## 使用

- 让模型按 `SKILL.md` 生成 `.drawio`。
- 左右脑图可直接用内置 `assets/mindmap-svg` 出 PNG/PDF（只需要 Chrome）。
- 本地 webapp 在跑时，自动用 `127.0.0.1:8130` 打开/导出。

## 构建

```bash
python build_release.py
```

生成 `dist/drawio-skill-v1.0.0.zip`、`dist/drawio-webapp-v1.0.0-win.zip` 和 `SHA256SUMS.txt`。
