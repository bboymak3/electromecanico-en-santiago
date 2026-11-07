#!/usr/bin/env python3
"""Inserta el contenedor de "Trabajos realizados" publicados desde el panel
Global Pro (globalprov2.pages.dev, sitio "electromecanico") en:

- index.html          -> se suman al grid "Trabajos Realizados" (#trabajos-realizados)
- galeria.html        -> se suman al grid de fichas (#fichas)
- comunas/*.html      -> se suman a "Trabajos realizados en <comuna>" o crean la sección
- en/index.html       -> sección "Completed Jobs"
- en/comunas/*.html   -> sección "Completed jobs in <comuna>"

El render lo hace js/trabajos-dinamicos.js (si no hay publicaciones no se ve nada).

Uso: python3 scripts/add_trabajos_dinamicos.py   (idempotente)
build_galeria.py lo ejecuta al final, porque regenera galeria.html.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- TRABAJOS-DINAMICOS:START -->", "<!-- TRABAJOS-DINAMICOS:END -->"
SCRIPT = '<script defer src="/js/trabajos-dinamicos.js"></script>'


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
        f.write(s)


def contenedor(modo, lang, comuna="", target=""):
    attrs = f'id="trabajos-dinamicos" data-modo="{modo}" data-lang="{lang}"'
    if comuna:
        attrs += f' data-comuna="{comuna}"'
    if target:
        attrs += f' data-target="{target}"'
    return f"{START}\n<div {attrs}></div>\n{END}\n"


def aplicar(p, block, anchor):
    s = read(p)
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", lambda m: block, s, flags=re.S)
    else:
        assert anchor in s, f"{p}: no se encontró el ancla {anchor!r}"
        s = s.replace(anchor, block + anchor, 1)
    if SCRIPT not in s:
        idx = s.rfind("</body>")
        assert idx != -1, f"{p}: sin </body>"
        s = s[:idx] + SCRIPT + "\n" + s[idx:]
    write(p, s)


def main():
    n = 0
    aplicar("index.html", contenedor("home", "es", target="#trabajos-realizados .row"),
            "<!-- GALERIA-SECCION:START -->")
    n += 1
    aplicar("galeria.html", contenedor("galeria", "es", target="#fichas .row"),
            '<section class="py-5" style="background:#f0f4f8;" id="fichas">')
    n += 1
    aplicar("en/index.html", contenedor("home", "en"), '<section id="galeria-de-tralows"')
    n += 1
    for fn in sorted(os.listdir(os.path.join(ROOT, "comunas"))):
        if fn.endswith(".html"):
            aplicar(os.path.join("comunas", fn),
                    contenedor("comuna", "es", fn[:-5], "#trabajos-realizados-comuna .row"),
                    '<section class="py-5" id="vehiculos-comuna"')
            n += 1
    for fn in sorted(os.listdir(os.path.join(ROOT, "en", "comunas"))):
        if fn.endswith(".html"):
            aplicar(os.path.join("en", "comunas", fn), contenedor("comuna", "en", fn[:-5]),
                    '<section class="py-5" id="vehicles-commona"')
            n += 1
    print(f"Páginas con trabajos dinámicos: {n}")


if __name__ == "__main__":
    main()
