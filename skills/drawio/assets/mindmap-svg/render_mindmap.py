# -*- coding: utf-8 -*-
"""Render a static left/right radial mind map as standalone SVG/PNG/PDF.

Input JSON:
{
  "title": "可选标题",
  "subtitle": "可选副标题",
  "branches": [
    {
      "label": "分支名",
      "side": "left|right",              # 可选，缺省按数量均分
      "color": "#5c6bc0",                # 可选，缺省用内置六色
      "leaves": ["叶子 1", "叶子 2"]
    }
  ]
}

Usage:
  python render_mindmap.py input.json out.svg
  python render_mindmap.py input.json out --png --pdf
"""
import argparse
import html
import json
import os
import shutil
import subprocess
import sys

W = 2000
MARGIN_Y = 100

ROOT = {"label": "", "w": 210, "h": 84}
BRANCH_W, BRANCH_H = 190, 48
LEAF_W, LEAF_H = 245, 34
LEAF_GAP = 8
GROUP_GAP = 44
H_ROOT_GAP = 90
H_BRANCH_GAP = 64
FONT = "Microsoft YaHei, PingFang SC, sans-serif"
ROOT_COLOR, ROOT_STROKE = "#1a237e", "#0d1553"

PALETTE = [
    {"solid": "#5c6bc0", "tint": "#e8eaf6", "border": "#c5cae9", "dark": "#283593"},
    {"solid": "#26a69a", "tint": "#e0f2f1", "border": "#b2dfdb", "dark": "#00695c"},
    {"solid": "#fb8c00", "tint": "#fff3e0", "border": "#ffe0b2", "dark": "#e65100"},
    {"solid": "#8e24aa", "tint": "#f3e5f5", "border": "#e1bee7", "dark": "#6a1b9a"},
    {"solid": "#00acc1", "tint": "#e0f7fa", "border": "#b2ebf2", "dark": "#006064"},
    {"solid": "#e53935", "tint": "#ffebee", "border": "#ffcdd2", "dark": "#c62828"},
]

CHROME_CANDIDATES = [
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome():
    env = os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    for candidate in CHROME_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("找不到 Chrome，请安装 Chrome 或用环境变量 CHROME 指定路径")


def esc(s):
    return html.escape(str(s), quote=True)


def group_height(b):
    leaves_h = len(b["leaves"]) * LEAF_H + (len(b["leaves"]) - 1) * LEAF_GAP
    return max(BRANCH_H, leaves_h)


def side_height(items):
    if not items:
        return 0
    return sum(group_height(b) for b in items) + GROUP_GAP * (len(items) - 1)


def rect(x, y, w, h, fill, stroke, rx, shadow=True, font_size=14, font_weight=500,
         text_color="#ffffff", label=""):
    filt = ' filter="url(#shadow)"' if shadow else ""
    return (
        f'<g{filt}>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + h / 2:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="{FONT}" font-size="{font_size}" '
        f'font-weight="{font_weight}" fill="{text_color}">{esc(label)}</text>'
        f'</g>'
    )


def curve(x1, y1, x2, y2, color, width):
    dx = max(30, abs(x2 - x1) * 0.45)
    c1x = x1 + dx if x2 > x1 else x1 - dx
    c2x = x2 - dx if x2 > x1 else x2 + dx
    return (
        f'<path d="M {x1:.1f} {y1:.1f} C {c1x:.1f} {y1:.1f}, {c2x:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    )


def build_svg(data):
    root_label = data.get("root") or data.get("title") or "Mind map"
    branches = data["branches"]
    if not branches:
        raise ValueError("branches 不能为空")

    for i, b in enumerate(branches):
        color = PALETTE[i % len(PALETTE)]
        b.setdefault("color", color["solid"])
        b.setdefault("tint", color["tint"])
        b.setdefault("border", color["border"])
        b.setdefault("dark", color["dark"])
        b["leaves"] = list(b.get("leaves") or [])

    left = [b for b in branches if b.get("side") == "left"]
    right = [b for b in branches if b.get("side") == "right"]
    rest = [b for b in branches if b.get("side") not in ("left", "right")]
    if rest:
        half = (len(rest) + 1) // 2
        left.extend(rest[:half])
        right.extend(rest[half:])

    H = max(side_height(left), side_height(right), group_height(branches[0])) + MARGIN_Y * 2
    root_cx, root_cy = W / 2, H / 2
    root_x, root_y = root_cx - ROOT["w"] / 2, root_cy - ROOT["h"] / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        '<defs><filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.18"/>'
        '</filter></defs>'
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
    ]

    for side_name, items in (("left", left), ("right", right)):
        total = side_height(items)
        y = (H - total) / 2
        for b in items:
            gh = group_height(b)
            b["group_top"] = y
            b["group_h"] = gh
            b["branch_cy"] = y + gh / 2
            if side_name == "left":
                b["branch_x"] = root_x - H_ROOT_GAP - BRANCH_W
                b["leaf_x"] = b["branch_x"] - H_BRANCH_GAP - LEAF_W
            else:
                b["branch_x"] = root_x + ROOT["w"] + H_ROOT_GAP
                b["leaf_x"] = b["branch_x"] + BRANCH_W + H_BRANCH_GAP
            n = len(b["leaves"])
            leaves_h = n * LEAF_H + (n - 1) * LEAF_GAP
            b["leaf_start_y"] = b["branch_cy"] - leaves_h / 2
            y += gh + GROUP_GAP

    for b in branches:
        if b["side"] == "left":
            x1, x2 = root_x, b["branch_x"] + BRANCH_W
        else:
            x1, x2 = root_x + ROOT["w"], b["branch_x"]
        parts.append(curve(x1, root_cy, x2, b["branch_cy"], b["color"], 3))

    for b in branches:
        if b["side"] == "left":
            x1, x2 = b["branch_x"], b["leaf_x"] + LEAF_W
        else:
            x1, x2 = b["branch_x"] + BRANCH_W, b["leaf_x"]
        for i, _leaf in enumerate(b["leaves"]):
            ly = b["leaf_start_y"] + i * (LEAF_H + LEAF_GAP) + LEAF_H / 2
            parts.append(curve(x1, b["branch_cy"], x2, ly, b["border"], 1.6))

    parts.append(rect(root_x, root_y, ROOT["w"], ROOT["h"], ROOT_COLOR, ROOT_STROKE, 16,
                      font_size=26, font_weight=700, label=root_label))

    for b in branches:
        parts.append(rect(b["branch_x"], b["branch_cy"] - BRANCH_H / 2, BRANCH_W, BRANCH_H,
                          b["color"], b["border"], 11, font_size=18, font_weight=600,
                          label=b["label"]))
        for i, leaf in enumerate(b["leaves"]):
            ly = b["leaf_start_y"] + i * (LEAF_H + LEAF_GAP)
            parts.append(rect(b["leaf_x"], ly, LEAF_W, LEAF_H, b["tint"], b["border"], 9,
                              font_size=14, font_weight=500, text_color=b["dark"], label=leaf))

    parts.append("</svg>")
    return "".join(parts), W, H


def wrap_html(svg, w, h):
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<style>@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0;background:#fff;overflow:hidden}}</style>'
        f'</head><body>{svg}</body></html>'
    )


def run_chrome(args):
    chrome = find_chrome()
    subprocess.run([chrome] + args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def export_png(html_path, png_path, w, h, scale):
    run_chrome([
        "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--force-device-scale-factor={scale}",
        f"--window-size={w},{h}",
        f"--screenshot={png_path}",
        "file:///" + html_path.replace("\\", "/"),
    ])
    try:
        from PIL import Image, ImageChops
        im = Image.open(png_path).convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bbox = ImageChops.difference(im, bg).getbbox()
        if bbox:
            pad = 30
            box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                   min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
            im.crop(box).save(png_path)
    except Exception:
        pass


def export_pdf(html_path, pdf_path):
    run_chrome([
        "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        "file:///" + html_path.replace("\\", "/"),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="输入 JSON")
    ap.add_argument("output", help="输出前缀，例如 out（生成 out.svg / out.png / out.pdf）")
    ap.add_argument("--png", action="store_true", help="同时导出 PNG")
    ap.add_argument("--pdf", action="store_true", help="同时导出 PDF")
    ap.add_argument("--scale", type=float, default=2.0, help="PNG 倍率，默认 2")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    svg, w, h = build_svg(data)
    base = os.path.splitext(args.output)[0]
    os.makedirs(os.path.dirname(os.path.abspath(base)), exist_ok=True)

    svg_path = base + ".svg"
    open(svg_path, "w", encoding="utf-8").write(svg)

    html_path = base + ".html"
    open(html_path, "w", encoding="utf-8").write(wrap_html(svg, w, h))

    print("SVG:", svg_path, f"({w}x{h})")
    if args.png:
        png_path = base + ".png"
        export_png(html_path, png_path, w, h, args.scale)
        print("PNG:", png_path)
    if args.pdf:
        pdf_path = base + ".pdf"
        export_pdf(html_path, pdf_path)
        print("PDF:", pdf_path)


if __name__ == "__main__":
    main()
