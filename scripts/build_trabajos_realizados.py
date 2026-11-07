#!/usr/bin/env python3
"""Landing "Trabajos Realizados" con TODOS los trabajos publicados desde el panel
Global Pro (globalprov2.pages.dev → Publicar en Web).

El mismo script sirve para electromecanico-en-santiago y para Globalpro: detecta el
sitio por el dominio canónico de quienes-somos.html.

Hace:
1. Enlace "Trabajos Realizados" / "Completed Jobs" en el menú de todas las páginas.
2. /trabajos-realizados  (desde quienes-somos.html) y /en/completed-jobs (desde en/about-us.html).
   El listado lo pinta js/trabajos-dinamicos.js (data-modo="landing").
3. Botón "Ver todos los trabajos realizados" en las secciones de trabajos (Globalpro).
4. URLs nuevas en sitemap.xml.

Uso: python3 scripts/build_trabajos_realizados.py   (idempotente)
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

URL_ES, URL_EN = "/trabajos-realizados", "/en/completed-jobs"
FILE_ES, FILE_EN = "trabajos-realizados.html", os.path.join("en", "completed-jobs.html")

CONFIGS = {
    "electromecanico": {
        "site": "https://electromecanico247.com",
        "sitio": "electromecanico",
        "color": "#0d7377",
        "wa": "56973622291",
        "marca_es": "Electromecánico en Santiago",
        "marca_en": "Electromecánico en Santiago",
        "servicio_es": "electromecánico a domicilio",
        "servicio_en": "mobile auto electrician and mechanic",
        "galeria": True,
    },
    "globalpro": {
        "site": "https://mecanico247.com",
        "sitio": "globalpro",
        "color": "#a80000",
        "wa": "56939026185",
        "marca_es": "Global Pro Automotriz",
        "marca_en": "Global Pro Automotive",
        "servicio_es": "mecánico a domicilio",
        "servicio_en": "mobile mechanic",
        "galeria": False,
    },
}


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
        f.write(s)


def detectar():
    s = read("quienes-somos.html")
    return CONFIGS["electromecanico" if "electromecanico247.com" in s else "globalpro"]


C = detectar()
SITE = C["site"]


# ---------------------------------------------------------------- menú
def li(url, label):
    return f'<li class="nav-item"><a class="nav-link" href="{url}">{label}</a></li>'


def patrones(en):
    url, label = (URL_EN, "Completed Jobs") if en else (URL_ES, "Trabajos Realizados")
    corto = f'<a href="{url}">{"Completed Jobs" if en else "Trabajos"}</a>'
    contacto = r"/en/contact[^\"]*" if en else r"/contacto"
    return url, [
        # Menú Bootstrap: antes de "Contacto"
        re.compile(r'([ \t]*)(<li class="nav-item">\s*<a class="nav-link[^"]*" href="' + contacto + r'")'),
        # Menús de landings especiales: antes de "FAQ" (#faq o /faq)
        re.compile(r'([ \t]*)(<li class="nav-item">\s*<a class="nav-link[^"]*" href="(?:/en)?(?:#|/)faq")'),
    ], [
        # Cabecera simple (blog): <a href="/blog/">Blog</a>
        (re.compile(r'([ \t]*)(<a href="(?:https://[a-z0-9.]+)?/blog/"(?: class="active")?>Blog</a>)'), corto),
        # Barra de las landings de servicios: antes del botón de WhatsApp
        (re.compile(r'([ \t]*)(<a href="https://wa\.me/[^"]*"[^>]*class="svc-wa")'), corto),
        # Barra "nav-bar" de servicios antiguos: antes del botón verde de WhatsApp
        (re.compile(r'([ \t]*)(<a href="https://wa\.me/[^"]*" target="_blank" style="background:#25D366)'),
         f'<a href="{url}" style="margin-right:16px;"><i class="fas fa-tools"></i> {"Jobs" if en else "Trabajos"}</a>'),
    ], li(url, label)


def add_nav_links():
    cambiadas, sin_menu = 0, []
    for dirpath, dirnames, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        top = rel.split(os.sep)[0]
        if top in (".git", "images", "assets", "node_modules", "scripts", "css", "js"):
            dirnames[:] = []
            continue
        for fn in files:
            if not fn.endswith(".html") or fn.startswith("google"):
                continue
            p = fn if rel == "." else os.path.join(rel, fn)
            en = top == "en"
            url, pats_li, pats_a, item_li = patrones(en)
            s = read(p)
            if f'href="{url}"' in s.split("</nav>")[0] if "</nav>" in s else f'href="{url}"' in s:
                continue  # ya tiene el enlace en el menú
            hecho = False
            for pat in pats_li:
                m = pat.search(s)
                if m:
                    indent = m.group(1)
                    sep = "\n" + indent if indent or s[m.start() - 1:m.start()] == "\n" else ""
                    s = s[:m.start()] + indent + item_li + sep + m.group(2) + s[m.end():]
                    hecho = True
                    break
            if not hecho:
                for pat, item_a in pats_a:
                    m = pat.search(s)
                    if m:
                        s = s[:m.start()] + m.group(1) + item_a + "\n" + m.group(1) + m.group(2) + s[m.end():]
                        hecho = True
                        break
            if hecho:
                write(p, s)
                cambiadas += 1
            elif "<nav" in s and fn != "404.html":
                sin_menu.append(p)
    return cambiadas, sin_menu


# ---------------------------------------------------------------- landing
def textos(en):
    if en:
        return {
            "lang": "en", "url": URL_EN, "file": FILE_EN, "plantilla": os.path.join("en", "about-us.html"),
            "title": f"Completed Jobs in Santiago | {C['marca_en']}",
            "desc": (f"Real jobs completed by {C['marca_en']}: photos of vehicles serviced at home in every "
                     f"area of Santiago. Filter by area and see each job's details."),
            "h1": "Completed Jobs",
            "hero": f"Real photos of vehicles serviced at home by our {C['servicio_en']} across Santiago.",
            "inicio": "Home", "miga": "Completed Jobs",
            "h2": "Vehicles serviced at home",
            "intro": ("Every job is documented by our technicians when the work order is closed. "
                      "Filter by area and click any vehicle to see its photos and the work performed."),
            "cargando": "Loading completed jobs...",
            "noscript": "Enable JavaScript to see our completed jobs.",
            "galeria": "", "feat": [
                ("fa-camera", "Real photos", "Taken by our technicians at the customer's address."),
                ("fa-map-marked-alt", "All of Santiago", "Home service in every area of the Metropolitan Region."),
                ("fa-shield-alt", "Guaranteed work", "Each service is documented and backed by our warranty."),
            ],
        }
    return {
        "lang": "es", "url": URL_ES, "file": FILE_ES, "plantilla": "quienes-somos.html",
        "title": f"Trabajos Realizados a Domicilio en Santiago | {C['marca_es']}",
        "desc": (f"Trabajos reales realizados por {C['marca_es']}: fotos de vehículos atendidos a domicilio "
                 f"en todas las comunas de Santiago. Filtra por comuna y revisa el detalle de cada trabajo."),
        "h1": "Trabajos Realizados",
        "hero": f"Fotos reales de vehículos atendidos por nuestro {C['servicio_es']} en Santiago.",
        "inicio": "Inicio", "miga": "Trabajos Realizados",
        "h2": "Vehículos atendidos a domicilio",
        "intro": ("Cada trabajo es documentado por nuestros técnicos al cerrar la orden de trabajo. "
                  "Filtra por comuna y haz clic en un vehículo para ver sus fotos y el trabajo realizado."),
        "cargando": "Cargando trabajos realizados...",
        "noscript": "Activa JavaScript para ver nuestros trabajos realizados.",
        "galeria": ('<div class="text-center mt-4"><a href="/galeria" class="btn btn-outline-secondary fw-bold">'
                    '<i class="fas fa-images me-2"></i>Ver galería de fotos</a></div>') if C["galeria"] else "",
        "feat": [
            ("fa-camera", "Fotos reales", "Tomadas por nuestros técnicos en el domicilio del cliente."),
            ("fa-map-marked-alt", "Toda la RM", "Atendemos a domicilio en todas las comunas de Santiago."),
            ("fa-shield-alt", "Trabajo garantizado", "Cada servicio queda documentado y con garantía."),
        ],
    }


def build_landing(en):
    t = textos(en)
    s = read(t["plantilla"])
    url = SITE + t["url"]
    url_es, url_en = SITE + URL_ES, SITE + URL_EN

    # Datos de la plantilla: se reemplazan en todo el documento (incluido el JSON-LD)
    m_url = re.search(r'<link rel="canonical" href="([^"]*)"', s)
    m_tit = re.search(r"<title>(.*?)</title>", s, flags=re.S)
    m_des = re.search(r'<meta name="description" content="([^"]*)"', s)
    if m_url:
        viejo = m_url.group(1)
        s = s.replace(viejo + ".html", url).replace(viejo + "#", url + "#").replace('"' + viejo + '"', '"' + url + '"')
    if m_tit and m_tit.group(1).strip():
        s = s.replace(m_tit.group(1).strip(), e(t["title"]))
    if m_des and m_des.group(1).strip():
        s = s.replace(m_des.group(1).strip(), e(t["desc"]))
    s = re.sub(r"<title>.*?</title>", f"<title>{e(t['title'])}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?title" content=")[^"]*', lambda m: m.group(1) + e(t["title"]), s)
    s = re.sub(r'(<meta (?:name|property)="(?:og:|twitter:)?description" content=")[^"]*', lambda m: m.group(1) + e(t["desc"]), s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*" ?/?>\n?', "", s)
    alt = (f'<link rel="alternate" hreflang="es" href="{url_es}" />\n'
           f'<link rel="alternate" hreflang="en" href="{url_en}" />\n'
           f'<link rel="alternate" hreflang="x-default" href="{url_es}" />\n')
    # Quitar JSON-LD propios de la página plantilla (migas / AboutPage)
    s = re.sub(r'[ \t]*<script type="application/ld\+json">(?:(?!</script>).)*?"(?:BreadcrumbList|AboutPage)"(?:(?!</script>).)*?</script>\n?',
               "", s, flags=re.S)
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": t["title"], "url": url,
         "description": t["desc"], "inLanguage": t["lang"]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["inicio"], "item": SITE + ("/en/" if en else "/")},
            {"@type": "ListItem", "position": 2, "name": t["miga"], "item": url}]},
    ], ensure_ascii=False, indent=2)
    s = s.replace("</head>", alt + f'<script type="application/ld+json">\n{ld}\n</script>\n</head>', 1)

    # charset al inicio del <head> (antes de los primeros 1024 bytes)
    s = re.sub(r'\s*<meta charset="UTF-8" ?/?>', "", s, count=1, flags=re.I)
    if "<!-- REDIRECT 301" in s:
        k = s.index("</script>", s.index("<!-- REDIRECT 301")) + len("</script>\n")
        s = s[:k] + '<meta charset="UTF-8">\n' + s[k:]
    else:
        s = s.replace("<head>", '<head>\n<meta charset="UTF-8">', 1)

    # Selector de idioma -> la otra versión de esta landing
    s = re.sub(r'href="[^"]*"(?=[^>]*>\s*(?:🇬🇧\s*)?EN</a>)', f'href="{URL_EN}"', s)
    s = re.sub(r'href="[^"]*"(?=[^>]*>\s*(?:🇪🇸\s*)?ES</a>)', f'href="{URL_ES}"', s)

    # Menú: marcar activo
    s = s.replace('class="nav-link active"', 'class="nav-link"')
    s = s.replace(f'<a class="nav-link" href="{t["url"]}">', f'<a class="nav-link active" href="{t["url"]}">')

    color = C["color"]
    feats = "".join(
        f'''      <div class="col-md-4"><div class="p-4 h-100 rounded-4" style="background:#f8f9fa;">
        <i class="fas {ic} mb-3" style="font-size:2rem;color:{color};"></i>
        <h3 class="h5 fw-bold">{e(ti)}</h3><p class="text-muted mb-0">{e(tx)}</p></div></div>
''' for ic, ti, tx in t["feat"])
    main = f'''<section class="page-hero">
  <div class="container">
    <h1><i class="fas fa-tools me-3"></i>{e(t["h1"])}</h1>
    <p>{e(t["hero"])}</p>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{"/en/" if en else "/"}">{e(t["inicio"])}</a></li>
        <li class="breadcrumb-item active" aria-current="page">{e(t["miga"])}</li>
      </ol>
    </nav>
  </div>
</section>

<section class="py-5" style="background:#f0f4f8;" id="trabajos-realizados-landing">
  <div class="container">
    <div class="text-center mb-4">
      <h2 class="fw-bold" style="color:{color};font-size:2rem;"><i class="fas fa-camera me-2"></i>{e(t["h2"])}</h2>
      <p style="color:#666;max-width:680px;margin:0 auto;">{e(t["intro"])}</p>
    </div>
    <div id="trabajos-dinamicos" data-modo="landing" data-lang="{t["lang"]}" data-sitio="{C["sitio"]}" data-color="{color}" data-wa="{C["wa"]}">
      <div class="text-center py-5 text-muted"><div class="spinner-border" style="color:{color};" role="status"></div><p class="mt-2">{e(t["cargando"])}</p></div>
    </div>
    <noscript><p class="text-center text-muted">{e(t["noscript"])}</p></noscript>
    {t["galeria"]}
  </div>
</section>

<section class="py-5 bg-white">
  <div class="container">
    <div class="row g-4 text-center">
{feats}    </div>
  </div>
</section>

'''
    start = s.index('<section class="page-hero">')
    s = s[:start] + main + "<!-- ======================================================================= -->\n" + s[s.index("<!-- CTA SECTION -->"):]
    s = s.replace("</body>", '<script defer src="/js/trabajos-dinamicos.js"></script>\n</body>', 1)
    s = "<!-- Generado por scripts/build_trabajos_realizados.py: no editar a mano -->\n" + s
    write(t["file"], s)


# ---------------------------------------------------------------- enlaces en secciones (Globalpro)
BTN_START, BTN_END = "<!-- LINK-TRABAJOS-REALIZADOS:START -->", "<!-- LINK-TRABAJOS-REALIZADOS:END -->"


def boton(texto="Ver todos los trabajos realizados"):
    return (f'{BTN_START}<div class="text-center mt-4"><a href="{URL_ES}" class="btn fw-bold text-white" '
            f'style="background:#ff6b00;border-radius:999px;padding:10px 26px;"><i class="fas fa-images me-2"></i>{texto}</a></div>{BTN_END}')


def add_section_links_globalpro():
    if C["sitio"] != "globalpro":
        return 0
    n = 0
    # Home: carrusel "Trabajos Realizados"
    s = read("index.html")
    if BTN_START not in s:
        anc = '<div id="carrusel-dots" style="display:flex;justify-content:center;gap:6px;margin-top:12px;"></div>'
        assert anc in s, "index.html: no se encontró el carrusel de trabajos"
        s = s.replace(anc, anc + "\n    " + boton(), 1)
        write("index.html", s)
        n += 1
    # Comunas: sección "Trabajos Realizados en <comuna>"
    for fn in sorted(os.listdir(os.path.join(ROOT, "comunas"))):
        if not fn.endswith(".html"):
            continue
        p = os.path.join("comunas", fn)
        s = read(p)
        if BTN_START in s or 'id="trabajos-realizados-comuna"' not in s:
            continue
        i = s.index('id="trabajos-realizados-comuna"')
        fin = s.index("</section>", i)
        k = s.rindex("</div>", i, fin)  # cierre del .container
        s = s[:k] + "  " + boton() + "\n  " + s[k:]
        write(p, s)
        n += 1
    return n


# ---------------------------------------------------------------- sitemap
def add_sitemap():
    s = read("sitemap.xml")
    nuevas = ""
    for u in (URL_ES, URL_EN):
        if f"{SITE}{u}<" not in s:
            nuevas += f"  <url><loc>{SITE}{u}</loc><lastmod>2026-11-07</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
    if nuevas:
        write("sitemap.xml", s.replace("</urlset>", nuevas + "</urlset>", 1))


def main():
    n, sin_menu = add_nav_links()
    build_landing(en=False)
    build_landing(en=True)
    ns = add_section_links_globalpro()
    add_sitemap()
    print(f"[{C['sitio']}] menú actualizado en {n} páginas; secciones con botón: {ns}")
    if sin_menu:
        print("  Páginas con <nav> donde no se encontró dónde insertar el enlace:", len(sin_menu))
        for p in sin_menu[:20]:
            print("   -", p)


if __name__ == "__main__":
    main()
