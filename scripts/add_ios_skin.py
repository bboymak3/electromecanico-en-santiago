#!/usr/bin/env python3
"""Enlaza /css/ios-skin.css (skin tipo iPhone) en todas las páginas HTML.

Solo agrega una etiqueta <link>; no modifica contenido. Idempotente.
Uso: python3 scripts/add_ios_skin.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = '<link rel="stylesheet" href="/css/ios-skin.css"/>'
SKIP = {"google7a5c4682e9b25d4f.html"}

added = 0
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "images", "node_modules")]
    for fn in files:
        if not fn.endswith(".html") or fn in SKIP:
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding="utf-8") as f:
            s = f.read()
        if "/css/ios-skin.css" in s:
            continue
        if "</head>" in s:
            s = s.replace("</head>", LINK + "\n</head>", 1)
        elif '<link rel="stylesheet" href="/css/styles.css">' in s:
            s = s.replace('<link rel="stylesheet" href="/css/styles.css">',
                          '<link rel="stylesheet" href="/css/styles.css">\n  ' + LINK, 1)
        else:
            print("sin punto de inserción:", os.path.relpath(path, ROOT))
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        added += 1
print(f"skin iOS enlazado en {added} páginas")
