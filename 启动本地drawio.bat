@echo off
chcp 65001 >nul
cd /d "%~dp0webapp"
start "" "http://127.0.0.1:8130/local.html"
python serve.py 8130
