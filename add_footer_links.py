#!/usr/bin/env python3
"""Add the Grupo 360 footer links to every HTML page with a footer."""

from pathlib import Path


LINK_BLOCK = '''\n  <div class="gp-agency-footer-links" style="margin-top:12px;text-align:center;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;">\n    <a href="https://maps.app.goo.gl/Jz2QTADrNNneQtGd9" target="_blank" rel="noopener noreferrer">Página web desarrollada por Grupo 360 Soluciones</a>\n    <a href="http://coporo.pages.dev/" target="_blank" rel="noopener noreferrer">Diseño de páginas webs - SEO Local -</a>\n  </div>\n'''
STANDALONE_FOOTER = f'''\n<footer class="gp-agency-footer" style="padding:20px;text-align:center;">{LINK_BLOCK}\n</footer>\n'''


def update_pages(root: Path) -> int:
    updated = 0
    for page in root.rglob("*.html"):
        content = page.read_text(encoding="utf-8")
        if "gp-agency-footer-links" in content:
            continue
        if "</footer>" in content.lower():
            updated_content = content.replace("</footer>", LINK_BLOCK + "</footer>", 1)
        elif "</body>" in content.lower():
            updated_content = content.replace("</body>", STANDALONE_FOOTER + "</body>", 1)
        else:
            continue
        if updated_content != content:
            page.write_text(updated_content, encoding="utf-8")
            updated += 1
    return updated


if __name__ == "__main__":
    print(f"Updated {update_pages(Path(__file__).parent)} HTML pages")