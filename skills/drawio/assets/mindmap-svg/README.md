# mindmap-svg

左右放射思维导图的离线渲染器：输入 JSON，输出静态 SVG / PNG / PDF。
不依赖 drawio、浏览器插件或网站，只用 Python + 本机 Chrome 截图。

## 用法

```bash
python render_mindmap.py example.json out --png --pdf
```

生成：

- `out.svg`：矢量源文件
- `out.html`：Chrome 渲染用的包装页
- `out.png`：可选，默认 2×，自动裁白边
- `out.pdf`：可选

## JSON 格式

```json
{
  "root": "中心主题",
  "branches": [
    {
      "label": "分支名",
      "side": "left",
      "leaves": ["叶子 1", "叶子 2"]
    }
  ]
}
```

- `side` 可选 `left` / `right`；不写时按顺序左右均分。
- 颜色可选，不写用内置六色（蓝 / 青 / 橙 / 紫 / 青绿 / 红）。
- 如果一个分支色想单独指定，加 `color`、`tint`、`border`、`dark` 四个字段。
- 这个工具只做静态左右脑图，不做编辑；要改图改 JSON 重新跑，或把 `.svg` 导入 drawio 继续编辑。
