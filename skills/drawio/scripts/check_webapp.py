# -*- coding: utf-8 -*-
"""Check whether the optional local draw.io webapp is running."""
import sys
import urllib.request

URL = "http://127.0.0.1:8130/local.html"

try:
    with urllib.request.urlopen(URL, timeout=2) as resp:
        if resp.status == 200:
            print("webapp: ready " + URL)
            sys.exit(0)
except Exception:
    pass

print("webapp: not running")
sys.exit(1)
