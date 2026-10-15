#!/usr/bin/env python3
"""Genera la galería de trabajos realizados a partir de scripts/galeria_data.json.

- galeria.html (landing, usando quienes-somos.html como plantilla de nav/footer)
- index.html: sección "Trabajos Realizados" + modal de galería + fichas modales
- Enlace "Galería" en el menú de las páginas en español
- URL /galeria en sitemap.xml

Uso: python3 scripts/build_galeria.py   (idempotente)
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://electromecanico247.com"
IMG_DIR = "/images/galeria/"

with open(os.path.join(ROOT, "scripts", "galeria_data.json"), encoding="utf-8") as f:
    TRABAJOS = json.load(f)["trabajos"]

e = html.escape


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
        f.write(s)


def alt_text(t, foto):
    return f"{foto['caption']} – electromecánico a domicilio en {t['comuna']}"


def gal_item(t, foto, group, extra=""):
    src = IMG_DIR + foto["file"]
    return (
        f'<button type="button" class="gal-item" data-group="{group}" data-veh="{t["slug"]}" '
        f'data-full="{src}.jpg" data-caption="{e(foto["caption"])}"{extra}>'
        f'<img src="{src}-thumb.jpg" alt="{e(alt_text(t, foto))}" loading="lazy">'
        f'<figcaption>{e(t["vehiculo"])}</figcaption></button>'
    )


def gallery_block(group):
    filters = '<button type="button" class="active" data-filter="all">Todos</button>' + "".join(
        f'<button type="button" data-filter="{t["slug"]}">{e(t["vehiculo"])}</button>' for t in TRABAJOS
    )
    items = "\n".join(gal_item(t, f, group) for t in TRABAJOS for f in t["fotos"])
    return (
        f'<div data-gal-scope>\n<div class="gal-filters">{filters}</div>\n'
        f'<div class="gal-grid">\n{items}\n</div>\n</div>'
    )


def trabajo_cards(cols="col-12 col-sm-6 col-lg-3"):
    out = []
    for t in TRABAJOS:
        f0 = t["fotos"][0]
        out.append(
            f'<div class="{cols}"><div class="trabajo-card" role="button" tabindex="0" '
            f'data-bs-toggle="modal" data-bs-target="#modal-trabajo-{t["slug"]}">'
            f'<img src="{IMG_DIR}{f0["file"]}-thumb.jpg" alt="{e(alt_text(t, f0))}" loading="lazy">'
            f'<div class="tc-body"><span class="tc-badge"><i class="fas {t["icono"]} me-1"></i>{e(t["servicio"])}</span>'
            f'<h3>{e(t["vehiculo"])}</h3><p>{e(t["resumen"])}</p>'
            f'<p class="mt-2 fw-bold" style="color:#0d7377;font-size:.8rem;"><i class="fas fa-map-marker-alt me-1"></i>{e(t["comuna"])} · Ver ficha <i class="fas fa-arrow-right ms-1"></i></p>'
            f"</div></div></div>"
        )
    return "\n".join(out)


def comuna_link(nombre):
    import unicodedata
    slug = "".join(c for c in unicodedata.normalize("NFD", nombre.lower()) if unicodedata.category(c) != "Mn").replace(" ", "-")
    if os.path.exists(os.path.join(ROOT, "comunas", slug + ".html")):
        return f'<a href="/comunas/{slug}" style="color:#0d7377;">{e(nombre)}</a>'
    return e(nombre)


def ficha_modals():
    out = []
    for t in TRABAJOS:
        wa = f"https://wa.me/56973622291?text=Hola%2C%20vi%20el%20trabajo%20en%20{t['vehiculo'].replace(' ', '%20')}%20y%20quiero%20cotizar"
        lis = "".join(f'<li><i class="fas fa-check-circle me-2" style="color:#14a098;"></i>{e(x)}</li>' for x in t["trabajos_realizados"])
        fotos = "".join(gal_item(t, f, "ficha-" + t["slug"]) for f in t["fotos"])
        out.append(f'''<div class="modal fade" id="modal-trabajo-{t["slug"]}" tabindex="-1" aria-labelledby="modal-trabajo-{t["slug"]}-title" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content" style="border-radius:16px;border:none;">
      <div class="modal-header" style="background:#0d7377;color:#fff;border-radius:16px 16px 0 0;">
        <h5 class="modal-title" id="modal-trabajo-{t["slug"]}-title"><i class="fas fa-car me-2"></i>Ficha: {e(t["vehiculo"])}</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
      </div>
      <div class="modal-body p-4">
        <table class="table table-sm ficha-table mb-3">
          <tr><th>Vehículo</th><td>{e(t["vehiculo"])}</td></tr>
          <tr><th>Servicio</th><td>{e(t["servicio"])}</td></tr>
          <tr><th>Comuna</th><td>{comuna_link(t["comuna"])}</td></tr>
          <tr><th>Modalidad</th><td>Electromecánico a domicilio</td></tr>
        </table>
        <p>{e(t["descripcion"])}</p>
        <h6 class="fw-bold" style="color:#0d7377;">Trabajos realizados</h6>
        <ul class="list-unstyled mb-3">{lis}</ul>
        <h6 class="fw-bold" style="color:#0d7377;">Fotos del trabajo</h6>
        <div class="ficha-fotos">{fotos}</div>
      </div>
      <div class="modal-footer" style="border:none;">
        <a href="/galeria" class="btn btn-outline-secondary fw-bold"><i class="fas fa-images me-1"></i> Ver galería</a>
        <a href="{wa}" target="_blank" rel="noopener" class="btn fw-bold" style="background:#14a098;color:#fff;"><i class="fab fa-whatsapp me-1"></i> Cotizar trabajo similar</a>
      </div>
    </div>
  </div>
</div>''')
    return "\n".join(out)


def gallery_modal():
    return f'''<div class="modal fade" id="modal-galeria" tabindex="-1" aria-labelledby="modal-galeria-title" aria-hidden="true">
  <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content" style="border-radius:16px;border:none;">
      <div class="modal-header" style="background:#0d7377;color:#fff;border-radius:16px 16px 0 0;">
        <h5 class="modal-title" id="modal-galeria-title"><i class="fas fa-images me-2"></i>Galería de Trabajos Realizados</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
      </div>
      <div class="modal-body p-4">
{gallery_block("galeria-modal")}
      </div>
      <div class="modal-footer" style="border:none;">
        <a href="/galeria" class="btn fw-bold" style="background:#0d7377;color:#fff;"><i class="fas fa-external-link-alt me-1"></i> Abrir página de galería</a>
      </div>
    </div>
  </div>
</div>'''


def replace_block(s, name, content, anchor_before=None, anchor_after=None):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    block = f"{start}\n{content}\n{end}"
    if start in s:
        return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, s, flags=re.S)
    anchor = anchor_before or anchor_after
    assert anchor in s, f"anchor not found: {anchor}"
    new = block + "\n" + anchor if anchor_before else anchor + block + "\n"
    return s.replace(anchor, new, 1)


def build_index():
    s = read("index.html")
    section = f'''<section class="py-5" style="background:#f0f4f8;" id="trabajos-realizados">
  <div class="container">
    <div class="text-center mb-4">
      <h2 class="fw-bold" style="color:#0d7377;font-size:2rem;"><i class="fas fa-camera me-2"></i>Trabajos Realizados</h2>
      <p style="color:#666;max-width:640px;margin:0 auto;">Fotos reales de vehículos atendidos por nuestro electromecánico a domicilio en Santiago. Haz clic en cada vehículo para ver su ficha.</p>
    </div>
    <div class="row g-4">
{trabajo_cards()}
    </div>
    <div class="text-center mt-4 d-flex justify-content-center gap-2 flex-wrap">
      <button type="button" class="btn btn-lg fw-bold" style="background:#0d7377;color:#fff;" data-bs-toggle="modal" data-bs-target="#modal-galeria"><i class="fas fa-images me-2"></i>Ver Galería de Fotos</button>
      <a href="/galeria" class="btn btn-lg btn-outline-secondary fw-bold"><i class="fas fa-external-link-alt me-2"></i>Página de Galería</a>
    </div>
  </div>
</section>'''
    fotos = [(t, f) for t in TRABAJOS for f in t["fotos"]]
    strip_items = "\n".join(gal_item(t, f, "tira-index", ' data-hidden-item' if i >= 10 else "")
                             for i, (t, f) in enumerate(fotos))
    more_btn = ('<button type="button" class="btn fw-bold btn-outline-secondary gal-more" data-step="10" '
                'style="border-radius:999px;padding:8px 22px;"><i class="fas fa-plus-circle me-2"></i>Ver más fotos</button>'
                if len(fotos) > 10 else "")
    strip = f'''    <div class="gal-strip-wrap mb-5">
      <div class="gal-strip">
{strip_items}
      </div>
      <div class="text-center mt-3 d-flex justify-content-center gap-2 flex-wrap">
        {more_btn}
        <a href="/galeria" class="btn fw-bold" style="background:#0d7377;color:#fff;border-radius:999px;padding:8px 22px;"><i class="fas fa-images me-2"></i>Ver galería de trabajos</a>
      </div>
    </div>'''
    s = replace_block(s, "GALERIA-TIRA", strip,
                      anchor_after="Cobertura en toda la Región Metropolitana.</p>\n    </div>\n")
    s = replace_block(s, "GALERIA-SECCION", section, "<!-- CONTACTO -->")
    s = replace_block(s, "GALERIA-MODALES", gallery_modal() + "\n" + ficha_modals(), "<!-- MODALES DE SERVICIOS -->")
    if "/css/galeria.css" not in s:
        s = s.replace('<link rel="stylesheet" href="/css/styles.css"/>',
                      '<link rel="stylesheet" href="/css/styles.css"/>\n  <link rel="stylesheet" href="/css/galeria.css"/>', 1)
    if "/js/galeria.js" not in s:
        s = s.replace("</body>", '<script defer src="/js/galeria.js"></script>\n</body>', 1)
    write("index.html", s)


def build_landing():
    s = read("quienes-somos.html")
    title = "Galería de Trabajos Realizados | Electromecánico a Domicilio en Santiago"
    desc = ("Galería de fotos reales de trabajos de electromecánico a domicilio en Santiago: "
            + ", ".join(t["vehiculo"] for t in TRABAJOS) + ". Electricidad automotriz, mantención y más.")
    url = SITE + "/galeria"
    og_img = SITE + IMG_DIR + TRABAJOS[0]["fotos"][0]["file"] + ".jpg"

    s = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", s, count=1)
    s = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?title" content=")[^"]*', lambda m: m.group(1) + e(title), s)
    s = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?description" content=")[^"]*', lambda m: m.group(1) + e(desc), s)
    s = re.sub(r'(<meta (?:name|property)="(?:og|twitter):image" content=")[^"]*', lambda m: m.group(1) + og_img, s)
    s = s.replace(SITE + "/quienes-somos.html", url).replace(SITE + "/quienes-somos", url)
    s = re.sub(r'\s*<meta property="og:image:(?:width|height)"[^>]*>', "", s)
    s = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>\n', "", s)
    s = s.replace('"name": "Quienes Somos"', '"name": "Galería"')
    s = s.replace('<a class="nav-link active" href="/quienes-somos">', '<a class="nav-link" href="/quienes-somos">')
    s = s.replace('<a class="nav-link" href="/galeria">', '<a class="nav-link active" href="/galeria">')
    s = s.replace("</head>", '<link rel="stylesheet" href="/css/galeria.css"/>\n</head>', 1)
    # charset al inicio del <head> para que el navegador no adivine la codificación
    s = re.sub(r'\s*<meta charset="UTF-8" ?/?>', "", s, count=1)
    if "<!-- REDIRECT 301" in s:
        k = s.index("</script>", s.index("<!-- REDIRECT 301")) + len("</script>\n")
        s = s[:k] + '<meta charset="UTF-8">\n' + s[k:]
    else:
        s = s.replace("<head>", '<head>\n<meta charset="UTF-8">', 1)

    images_ld = [
        {"@type": "ImageObject", "contentUrl": SITE + IMG_DIR + f["file"] + ".jpg",
         "name": f["caption"], "description": alt_text(t, f)}
        for t in TRABAJOS for f in t["fotos"]
    ]
    ld = json.dumps({"@context": "https://schema.org", "@type": "ImageGallery", "name": title,
                     "url": url, "description": desc, "image": images_ld}, ensure_ascii=False, indent=2)
    s = s.replace("</head>", f'<script type="application/ld+json">\n{ld}\n</script>\n</head>', 1)

    main = f'''<section class="page-hero">
  <div class="container">
    <h1><i class="fas fa-images me-3"></i>Galería de Trabajos Realizados</h1>
    <p>Fotos reales de vehículos atendidos por nuestro electromecánico a domicilio en Santiago.</p>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Inicio</a></li>
        <li class="breadcrumb-item active" aria-current="page">Galería</li>
      </ol>
    </nav>
  </div>
</section>

<section class="py-5 bg-white" id="galeria">
  <div class="container">
    <h2 class="text-center fw-bold mb-2" style="color:#0d7377;">Fotos de nuestros trabajos</h2>
    <p class="text-center text-muted mb-4">Filtra por vehículo y haz clic en una foto para ampliarla.</p>
{gallery_block("galeria")}
  </div>
</section>

<section class="py-5" style="background:#f0f4f8;" id="fichas">
  <div class="container">
    <h2 class="text-center fw-bold mb-2" style="color:#0d7377;">Fichas de vehículos atendidos</h2>
    <p class="text-center text-muted mb-4">Revisa el detalle de cada trabajo realizado a domicilio.</p>
    <div class="row g-4">
{trabajo_cards()}
    </div>
  </div>
</section>

{ficha_modals()}
'''
    start = s.index('<section class="page-hero">')
    s = s[:start] + main + s[s.index("<!-- CTA SECTION -->"):]
    # Volver al comentario separador que precede al CTA
    s = s.replace(main + "<!-- CTA SECTION -->", main + "<!-- ======================================================================= -->\n<!-- CTA SECTION -->", 1)
    s = s.replace("</body>", '<script defer src="/js/galeria.js"></script>\n</body>', 1)
    s = "<!-- Generado por scripts/build_galeria.py: editar scripts/galeria_data.json y re-ejecutar -->\n" + s
    write("galeria.html", s)


def _nav_li(m):
    indent, inner = m.group(1), m.group(2)
    close = "\n" + indent if "\n" in inner else ""
    return f'{indent}<li class="nav-item">{inner}<a class="nav-link" href="/galeria">Galería</a>{close}</li>\n{m.group(0)}'


NAV_PATTERNS = [
    # Menú Bootstrap: <li class="nav-item"> <a class="nav-link" href="/blog/">Blog</a> </li>
    (re.compile(r'^([ \t]*)<li class="nav-item">(\s*)<a class="nav-link" href="/blog/">', re.M), _nav_li),
    # Barra simple de servicios: insertar antes del botón de WhatsApp
    (re.compile(r'(<nav class="nav-bar">\n[ \t]*<a href="/">.*?</a>\n)([ \t]*)(<a href="https://wa\.me/)'),
     lambda m: f'{m.group(1)}{m.group(2)}<a href="/galeria" style="margin-left:auto;margin-right:16px;"><i class="fas fa-images"></i> Galería</a>\n{m.group(2)}{m.group(3)}'),
    # Cabecera del blog: <a href="/blog/">Blog</a>
    (re.compile(r'^([ \t]*)<a href="/blog/"(?: class="active")?>Blog</a>', re.M),
     lambda m: f'{m.group(1)}<a href="/galeria">Galería</a>\n{m.group(0)}'),
    # Footer legal de páginas sin menú: <a href="/contacto">Contacto</a> ·
    (re.compile(r'^([ \t]*)<a href="/contacto">Contacto</a> ·', re.M),
     lambda m: f'{m.group(1)}<a href="/galeria">Galería</a> ·\n{m.group(0)}'),
]
ALREADY = re.compile(r'href="/galeria"[^>]*>(?:<i[^>]*></i> )?Galería</a>')


def add_nav_links():
    changed = 0
    for dirpath, dirnames, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.split(os.sep)[0] in (".git", "en", "images", "assets"):
            dirnames[:] = []
            continue
        for fn in files:
            if not fn.endswith(".html") or fn == "galeria.html":
                continue
            p = fn if rel == "." else os.path.join(rel, fn)
            s = read(p)
            if ALREADY.search(s):
                continue
            for pat, repl in NAV_PATTERNS:
                if pat.search(s):
                    write(p, pat.sub(repl, s, count=1))
                    changed += 1
                    break
    return changed


def add_sitemap():
    s = read("sitemap.xml")
    if SITE + "/galeria<" in s:
        return
    line = f"  <url><loc>{SITE}/galeria</loc><lastmod>2026-10-11</lastmod><priority>0.8</priority><changefreq>weekly</changefreq></url>\n"
    s = s.replace("</urlset>", line + "</urlset>", 1)
    write("sitemap.xml", s)


if __name__ == "__main__":
    n = add_nav_links()
    build_landing()
    build_index()
    add_sitemap()
    print(f"Galería generada: {sum(len(t['fotos']) for t in TRABAJOS)} fotos, {len(TRABAJOS)} vehículos; menú actualizado en {n} páginas")
