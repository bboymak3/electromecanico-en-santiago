#!/usr/bin/env python3
"""Agrega el crédito 'Página web desarrollada por makeseo.app' al footer de las
páginas que no lo tienen (antes de </footer>, o antes de </body> si no hay footer).
Usa estilos en línea para verse igual aunque la página no cargue css/styles.css.
Idempotente: python3 scripts/add_makeseo_credit.py
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def credit(en=False):
    texto = "Website developed by" if en else "Página web desarrollada por"
    return ('<!-- MAKESEO-CREDIT:START -->\n'
            '<div class="gp-agency-footer-bar" style="background:linear-gradient(135deg,#0d7377 0%,#14a098 100%);color:#fff;'
            'padding:22px 16px;text-align:center;border-top:4px solid #ff6b35;margin-top:16px;">\n'
            '  <a href="https://makeseo.app" target="_blank" rel="noopener" class="gp-footer-credit" style="display:inline-flex;'
            'align-items:center;gap:10px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);padding:10px 22px;'
            'border-radius:50px;text-decoration:none;color:#fff;font-weight:600;font-size:.95rem;">'
            f'<i class="fas fa-code" style="color:#ff6b35;"></i> {texto} <strong>makeseo.app</strong></a>\n'
            '</div>\n<!-- MAKESEO-CREDIT:END -->\n')


if __name__ == "__main__":
    os.chdir(ROOT)
    n = 0
    for f in glob.glob("**/*.html", recursive=True):
        if os.path.basename(f) == "google7a5c4682e9b25d4f.html":
            continue
        s = open(f, encoding="utf-8").read()
        if "gp-footer-credit" in s:
            continue
        block = credit(f.startswith("en/"))
        i = s.rfind("</footer>")
        if i < 0:
            i = s.rfind("</body>")
        if i < 0:
            print("sin punto de inserción:", f)
            continue
        s = s[:i] + block + s[i:]
        open(f, "w", encoding="utf-8").write(s)
        n += 1
    print(f"crédito makeseo.app agregado en {n} páginas")
