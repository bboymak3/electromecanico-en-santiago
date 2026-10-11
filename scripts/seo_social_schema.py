#!/usr/bin/env python3
"""SEO técnico de todo el sitio (idempotente):

1. Imagen al compartir: og:image / twitter:image = logo (1200x630) en todas las páginas.
2. Canónicas: corrige las que apuntan a URLs inexistentes (se usa la URL propia de la página).
3. Datos estructurados (fragmentos enriquecidos): bloque @graph con AutoRepair/Organization
   (logo), WebSite, WebPage y BreadcrumbList (si la página no tenía); FAQPage en el index.
4. sitemap.xml regenerado con todas las páginas indexables + imágenes (galería y logo).

Uso: python3 scripts/seo_social_schema.py
"""
import datetime
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://electromecanico-en-santiago.pages.dev"
OG_IMG = SITE + "/images/electromecanico-a-domicilio-en-santiago-logo-og.jpg"
LOGO = SITE + "/images/electromecanico-a-domicilio-en-santiago-logo-512.jpg"
TODAY = datetime.date.today().isoformat()
SKIP = {"google7a5c4682e9b25d4f.html"}
NOINDEX = {"404.html", "en/404.html"}
os.chdir(ROOT)


def url_of(f):
    if f == "index.html":
        return SITE + "/"
    if f == "en/index.html":
        return SITE + "/en/"
    if f.endswith("/index.html"):
        return SITE + "/" + f[: -len("/index.html")]
    return SITE + "/" + f[: -len(".html")]


def exists(url):
    p = url.replace(SITE, "").strip("/")
    return p == "" or os.path.exists(p + ".html") or os.path.exists(os.path.join(p, "index.html"))


def strip_tags(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()


def meta(s, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', s)
    return html.unescape(m.group(1)) if m else None


ORG = {
    "@type": ["AutoRepair", "LocalBusiness"],
    "@id": SITE + "/#organization",
    "name": "Electromecánico en Santiago",
    "alternateName": "M&E PRO Electromecánico Profesional",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "@id": SITE + "/#logo", "url": LOGO, "width": 512, "height": 512,
             "caption": "Electromecánico en Santiago"},
    "image": {"@id": SITE + "/#logo"},
    "telephone": "+56973622291",
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Padre Alberto Hurtado 3598",
                "addressLocality": "Pedro Aguirre Cerda", "addressRegion": "Región Metropolitana",
                "postalCode": "1080000", "addressCountry": "CL"},
    "areaServed": {"@type": "AdministrativeArea", "name": "Región Metropolitana de Santiago"},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                  "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  "opens": "00:00", "closes": "23:59"},
    "sameAs": ["https://maps.app.goo.gl/ygW6nj3w9J16C86N7"],
    "contactPoint": {"@type": "ContactPoint", "telephone": "+56973622291", "contactType": "customer service",
                     "areaServed": "CL", "availableLanguage": ["es", "en"]},
}
SECCIONES = {"servicios": ("Servicios", SITE + "/servicios-domicilio"), "comunas": ("Comunas", SITE + "/#comunas"),
             "blog": ("Blog", SITE + "/blog"), "vehiculos": ("Vehículos", SITE + "/vehiculos"),
             "marcas_automotrices": ("Marcas", SITE + "/marcas_automotrices"), "en": ("English", SITE + "/en/")}


def page_name(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if m and strip_tags(m.group(1)):
        return re.sub(r"\s+", " ", strip_tags(m.group(1)))
    t = strip_tags(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    return re.split(r"\s[|\-–]\s", t)[0]


def breadcrumb(f, url, name):
    items = [("Inicio", SITE + "/")]
    parts = f.split("/")
    if len(parts) > 1:
        sec = SECCIONES.get(parts[0])
        if sec and sec[1] != url:
            items.append(sec)
        if parts[0] == "en" and len(parts) > 2 and parts[1] in SECCIONES:
            items.append((SECCIONES[parts[1]][0], SITE + "/en/" + parts[1]))
    if url != SITE + "/":
        items.append((name, url))
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def index_faq(s):
    sec = re.search(r'id="faq".*?</section>', s, re.S)
    if not sec:
        return None
    qs = re.findall(r'accordion-button[^>]*>(.*?)</button>.*?accordion-body[^>]*>(.*?)</div>', sec.group(0), re.S)
    qa = [(strip_tags(q), re.sub(r"\s+", " ", strip_tags(a))) for q, a in qs if strip_tags(q) and strip_tags(a)]
    if not qa:
        return None
    return {"@type": "FAQPage", "@id": SITE + "/#faq",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}


def replace_block(s, name, content):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    block = f"{start}\n{content}\n{end}"
    if start in s:
        return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, s, flags=re.S)
    return s.replace("</head>", block + "\n</head>", 1)


def process(f):
    s = open(f, encoding="utf-8").read()
    lang_en = f.startswith("en/")
    own = url_of(f)
    canon_fixed = False
    # 2. Canónica
    m = re.search(r'<link rel="canonical" href="([^"]*)"\s*/?>', s)
    if f not in NOINDEX:
        if m and not exists(m.group(1)):
            s = s.replace(m.group(0), f'<link rel="canonical" href="{own}">', 1)
            canon_fixed = True
        elif not m:
            s = s.replace("</title>", f'</title>\n  <link rel="canonical" href="{own}">', 1)
            canon_fixed = True
    m = re.search(r'<link rel="canonical" href="([^"]*)"', s)
    url = m.group(1) if m else own
    title = strip_tags(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    desc = meta(s, "name", "description") or title
    name = page_name(s)
    # 1. Meta sociales: se quitan las de imagen/twitter previas (fuera del bloque) y se agrega el bloque
    s = re.sub(r"<!-- SOCIAL-META:START -->.*?<!-- SOCIAL-META:END -->\n?", "", s, flags=re.S)
    s = re.sub(r'[ \t]*<meta (?:property|name)="(?:og:image(?::[a-z_]+)?|twitter:image(?::alt)?|twitter:card|og:url)" content="[^"]*"\s*/?>\n?', "", s)
    social = [f'<meta property="og:url" content="{html.escape(url)}">',
              f'<meta property="og:image" content="{OG_IMG}">',
              f'<meta property="og:image:secure_url" content="{OG_IMG}">',
              '<meta property="og:image:type" content="image/jpeg">',
              '<meta property="og:image:width" content="1200">',
              '<meta property="og:image:height" content="630">',
              '<meta property="og:image:alt" content="Logo M&amp;E PRO – Electromecánico en Santiago">',
              '<meta name="twitter:card" content="summary_large_image">',
              f'<meta name="twitter:image" content="{OG_IMG}">',
              '<meta name="twitter:image:alt" content="Logo M&amp;E PRO – Electromecánico en Santiago">']
    for prop, val in (("og:title", title), ("og:description", desc), ("og:type", "website"),
                      ("og:site_name", "Electromecánico en Santiago"), ("og:locale", "en_US" if lang_en else "es_CL")):
        if meta(s, "property", prop) is None:
            social.append(f'<meta property="{prop}" content="{html.escape(val)}">')
    for prop, val in (("twitter:title", title), ("twitter:description", desc)):
        if meta(s, "name", prop) is None:
            social.append(f'<meta name="{prop}" content="{html.escape(val)}">')
    s = replace_block(s, "SOCIAL-META", "\n".join(social))
    # 3. Datos estructurados
    if f not in NOINDEX:
        graph = [ORG,
                 {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Electromecánico en Santiago",
                  "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "es-CL"},
                 {"@type": "CollectionPage" if f in ("galeria.html", "blog/index.html") else "WebPage",
                  "@id": url + "#webpage", "url": url, "name": title, "description": desc,
                  "inLanguage": "en" if lang_en else "es-CL", "isPartOf": {"@id": SITE + "/#website"},
                  "about": {"@id": SITE + "/#organization"},
                  "primaryImageOfPage": {"@type": "ImageObject", "url": OG_IMG, "width": 1200, "height": 630},
                  "breadcrumb": {"@id": url + "#breadcrumb"}}]
        others = re.sub(r"<!-- SCHEMA-ORG:START -->.*?<!-- SCHEMA-ORG:END -->", "", s, flags=re.S)
        if '"BreadcrumbList"' not in others:
            graph.append(breadcrumb(f, url, name))
        else:
            del graph[2]["breadcrumb"]
        if f == "index.html" and '"FAQPage"' not in others:
            faq = index_faq(s)
            if faq:
                graph.append(faq)
        ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
        s = replace_block(s, "SCHEMA-ORG", f'<script type="application/ld+json">\n{ld}\n</script>')
    open(f, "w", encoding="utf-8").write(s)
    return url, canon_fixed


def sitemap(urls):
    gal = json.load(open("scripts/galeria_data.json", encoding="utf-8"))["trabajos"]
    imgs = {SITE + "/": [(OG_IMG, "Electromecánico en Santiago")],
            SITE + "/galeria": [(f'{SITE}/images/galeria/{p["file"]}.jpg', p["caption"]) for t in gal for p in t["fotos"]]}
    imgs[SITE + "/"] += imgs[SITE + "/galeria"]

    def prio(u):
        p = u.replace(SITE, "")
        if p == "/":
            return "1.0"
        if p.startswith("/en"):
            return "0.5"
        if p.startswith("/servicios/"):
            return "0.9"
        if p.startswith(("/comunas/", "/galeria")):
            return "0.8"
        if p.startswith("/blog/"):
            return "0.6"
        return "0.7"
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in sorted(set(urls), key=lambda u: (u != SITE + "/", u.replace(SITE, "").startswith("/en"), u)):
        x = f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{prio(u)}</priority>"
        for src, cap in imgs.get(u, []):
            x += f"<image:image><image:loc>{src}</image:loc><image:title>{html.escape(cap)}</image:title></image:image>"
        out.append(x + "</url>")
    out.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
    return len(set(urls))


if __name__ == "__main__":
    files = sorted(f for f in glob.glob("**/*.html", recursive=True) if os.path.basename(f) not in SKIP)
    urls, fixed = [], 0
    for f in files:
        u, c = process(f)
        fixed += c
        if f not in NOINDEX and exists(u):
            urls.append(u)
    n = sitemap(urls)
    print(f"Páginas procesadas: {len(files)}; canónicas corregidas: {fixed}; URLs en sitemap: {n}")
