#!/usr/bin/env python3
"""Cambia el crédito de "Santiago 360" / "Grupo 360" a makeseo.app y lo agrega donde falte.

Uso (desde la raíz del sitio):
    python3 apply_makeseo_footer.py            # simulación: solo muestra qué cambiaría
    python3 apply_makeseo_footer.py --apply    # aplica los cambios
    python3 apply_makeseo_footer.py --apply --no-add   # solo reemplaza, no agrega donde falta

Qué hace en cada .html (y en README.md):
  1. Reemplaza las menciones de la agencia anterior ("En Santiago 360", "Santiago 360",
     "Grupo 360 Soluciones", "360 Soluciones", "Santiago360") por "makeseo.app".
  2. En los enlaces del crédito (los que contienen "desarrollad/diseñad/creada/developed/
     designed/made/powered" o la marca anterior) cambia el href a https://makeseo.app.
  3. Si la página no tiene ningún crédito de makeseo.app, agrega una barra de crédito
     antes de </footer> (o antes de </body> si no hay footer). Texto en inglés si
     <html lang="en...">.
Es idempotente: ejecutarlo dos veces no duplica nada. No toca "360" que no sea la marca
(p. ej. "cámara 360°").
"""
import argparse
import os
import re
import sys

NEW_NAME = "makeseo.app"
NEW_URL = "https://makeseo.app"
SKIP_DIRS = {".git", "node_modules", ".wrangler", "dist", "build", "out", ".claude"}

# Marca anterior (solo estas formas; no cualquier "360")
OLD_BRAND = re.compile(r"(?:En\s+)?Santiago\s*360(?:\s+Soluciones)?|Grupo\s+360(?:\s+Soluciones)?|\b360\s+Soluciones\b", re.I)
CREDIT_WORDS = re.compile(r"desarrollad|diseñad|disenad|cread[ao]|hecha por|developed|designed|made by|powered by|created by", re.I)
ANCHOR = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S | re.I)
HREF = re.compile(r'href\s*=\s*"[^"]*"', re.I)
LANG_EN = re.compile(r'<html[^>]*\blang\s*=\s*"en', re.I)


def credit_block(en=False):
    texto = "Website developed by" if en else "Página web desarrollada por"
    return ('<!-- MAKESEO-CREDIT:START -->\n'
            '<div class="makeseo-credit" style="background:linear-gradient(135deg,#0d7377 0%,#14a098 100%);color:#fff;'
            'padding:22px 16px;text-align:center;border-top:4px solid #ff6b35;margin-top:16px;">\n'
            f'  <a href="{NEW_URL}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;'
            'background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);padding:10px 22px;border-radius:50px;'
            'text-decoration:none;color:#fff;font-weight:600;font-size:.95rem;">'
            f'&lt;/&gt; {texto} <strong>{NEW_NAME}</strong></a>\n'
            '</div>\n<!-- MAKESEO-CREDIT:END -->\n')


def fix_anchor(m):
    attrs, inner = m.group(1), m.group(2)
    text = re.sub(r"<[^>]+>", " ", inner)
    is_credit = OLD_BRAND.search(text) or (CREDIT_WORDS.search(text) and NEW_NAME not in attrs and
                                            ("360" in text or "360" in attrs))
    if not is_credit:
        return m.group(0)
    inner = OLD_BRAND.sub(NEW_NAME, inner)
    if HREF.search(attrs):
        attrs = HREF.sub(f'href="{NEW_URL}"', attrs, count=1)
    else:
        attrs = f' href="{NEW_URL}"' + attrs
    attrs = re.sub(r'\s*rel\s*=\s*"[^"]*"', "", attrs) + ' rel="noopener"' if 'target="_blank"' in attrs else attrs
    return f"<a{attrs}>{inner}</a>"


def process_html(s, add_missing=True):
    changes = []
    s2 = ANCHOR.sub(fix_anchor, s)
    if s2 != s:
        changes.append("enlace de crédito → makeseo.app")
    s3 = OLD_BRAND.sub(NEW_NAME, s2)
    if s3 != s2:
        changes.append("texto de la agencia anterior → makeseo.app")
    if add_missing and NEW_URL not in s3 and "MAKESEO-CREDIT:START" not in s3:
        i = s3.rfind("</footer>")
        if i < 0:
            i = s3.rfind("</body>")
        if i >= 0:
            s3 = s3[:i] + credit_block(bool(LANG_EN.search(s3))) + s3[i:]
            changes.append("crédito agregado (no tenía)")
    return s3, changes


def process_readme(s):
    s2 = OLD_BRAND.sub(f"[{NEW_NAME}]({NEW_URL})", s)
    return s2, (["README: agencia anterior → makeseo.app"] if s2 != s else [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".", help="carpeta del sitio (por defecto la actual)")
    ap.add_argument("--apply", action="store_true", help="escribir los cambios (sin esto es simulación)")
    ap.add_argument("--no-add", action="store_true", help="no agregar el crédito en páginas que no lo tienen")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    total = changed = 0
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in files:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            if fn.lower().endswith((".html", ".htm")):
                if re.match(r"google[0-9a-f]+\.html$", fn):
                    continue
                total += 1
                s = open(p, encoding="utf-8", errors="surrogateescape").read()
                new, ch = process_html(s, not a.no_add)
            elif fn.lower() == "readme.md":
                s = open(p, encoding="utf-8", errors="surrogateescape").read()
                new, ch = process_readme(s)
            else:
                continue
            if ch:
                changed += 1
                print(f"{'✔' if a.apply else '•'} {rel}: {', '.join(ch)}")
                if a.apply:
                    open(p, "w", encoding="utf-8", errors="surrogateescape").write(new)
    modo = "aplicado" if a.apply else "simulación (usa --apply para escribir)"
    print(f"\n{changed} archivos con cambios de {total} páginas HTML — {modo}")
    # Verificación final: menciones que queden de la marca anterior
    if a.apply:
        quedan = []
        for dirpath, dirnames, files in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in files:
                if fn.lower().endswith((".html", ".htm", ".md")):
                    t = open(os.path.join(dirpath, fn), encoding="utf-8", errors="surrogateescape").read()
                    if OLD_BRAND.search(t):
                        quedan.append(os.path.relpath(os.path.join(dirpath, fn), root))
        print("Menciones restantes de la marca anterior:", len(quedan), quedan[:10])
    return 0


if __name__ == "__main__":
    sys.exit(main())
