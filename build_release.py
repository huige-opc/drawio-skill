# -*- coding: utf-8 -*-
"""Build distribution zips: drawio skill (WorkBuddy) + optional local webapp."""
import hashlib
import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
VERSION = "1.0.0"
SKIP_DIRS = {"__pycache__", ".git", "test", "dist"}
SKIP_FILES = {".DS_Store"}


def add_tree(zf, src_dir, arc_prefix, skip_dirs=SKIP_DIRS, skip_files=SKIP_FILES):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            if name in skip_files or name.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, src_dir)
            zf.write(full, os.path.join(arc_prefix, rel).replace("\\", "/"))


def build_skill():
    out = os.path.join(DIST, f"drawio-skill-v{VERSION}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        add_tree(zf, os.path.join(ROOT, "skills", "drawio"), "drawio", skip_files={"LICENSE"})
        zf.write(os.path.join(ROOT, "LICENSE"), "drawio/LICENSE")
    return out


def build_webapp():
    out = os.path.join(DIST, f"drawio-webapp-v{VERSION}-win.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        add_tree(zf, os.path.join(ROOT, "webapp"), "drawio-webapp", skip_dirs={"test", "__pycache__", ".git"})
        lic_dir = os.path.join(ROOT, "build_assets", "licenses")
        zf.write(os.path.join(lic_dir, "drawio-Apache-2.0.txt"), "drawio-webapp/LICENSE")
        zf.write(os.path.join(ROOT, "THIRD_PARTY_NOTICES.md"), "drawio-webapp/THIRD_PARTY_NOTICES.md")
        add_tree(zf, lic_dir, "drawio-webapp/LICENSES", skip_dirs=set())
        zf.writestr(
            "drawio-webapp/启动本地drawio.bat",
            "@echo off\r\nchcp 65001 >nul\r\ncd /d \"%~dp0\"\r\n"
            "start \"\" \"http://127.0.0.1:8130/local.html\"\r\npython serve.py 8130\r\n",
        )
        zf.writestr(
            "drawio-webapp/使用说明.txt",
            "本地 draw.io\r\n\r\n1. 需要 Python 3 和 Chrome\r\n2. 双击 启动本地drawio.bat\r\n"
            "3. 浏览器打开 http://127.0.0.1:8130/local.html\r\n4. 打开 .drawio，导出 PNG/SVG/JPG/PDF\r\n",
        )
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(DIST, exist_ok=True)
    outputs = [build_skill(), build_webapp()]
    lines = []
    for path in outputs:
        size = os.path.getsize(path)
        lines.append(f"{os.path.basename(path)}\t{size}\t{sha256(path)}")
        print(os.path.basename(path), size, sha256(path))
    with open(os.path.join(DIST, "SHA256SUMS.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
