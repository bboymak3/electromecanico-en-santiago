#!/usr/bin/env python3
"""Separa el texto del banner en las páginas donde el título quedaba montado sobre la imagen.

css/styles.css convierte .hero-section en el banner con imagen (texto incluido en la imagen).
Algunas páginas (sobre todo en inglés) tenían su título y botones DENTRO de .hero-section,
así que se superponían al banner. Se deja .hero-section vacía (solo banner, como en el
index en español) y el mismo contenido pasa a una .hero-text-section justo debajo.
No elimina contenido. Idempotente.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = re.compile(r'<section class="hero-section"([^>]*)>(.*?)</section>', re.S)
CSS = """<style>
  .hero-text-section .btn-outline-light { color:#0d7377; border-color:#0d7377; }
  .hero-text-section .btn-outline-light:hover { background:#0d7377; color:#fff; }
  .hero-text-section .hero-title, .hero-text-section .hero-subtitle { color:#1a1a2e; text-shadow:none; }
  .hero-text-section .hero-subtitle { color:#4a5568; }
  .hero-text-section > .container > .row { justify-content:center; }
</style>"""

n = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    m = HERO.search(s)
    if not m or not re.sub(r"<!--.*?-->", "", m.group(2), flags=re.S).strip():
        continue
    attrs = re.sub(r'\s*style="[^"]*"', "", m.group(1))  # banner unificado: sin imagen de fondo propia
    new = (f'<section class="hero-section"{attrs}></section>\n'
           f'<section class="hero-text-section">{m.group(2)}</section>')
    s = s[:m.start()] + new + s[m.end():]
    if "HERO-TEXT-FIX" not in s:
        s = s.replace("</head>", f"<!-- HERO-TEXT-FIX -->\n{CSS}\n</head>", 1)
    open(f, "w", encoding="utf-8").write(s)
    n += 1
print(f"páginas corregidas: {n}")
