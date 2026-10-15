#!/usr/bin/env python3
"""Genera landings de servicios desde scripts/landings_data.json.

- servicios/<slug>.html para los 6 servicios de valor estándar y las 18 instalaciones
- servicios/instalaciones-automotrices.html (página que reúne todo)
- index.html: sección "valor estándar" con 6 modales + sección y modal de instalaciones
- Menú "Especializados" del index, sitemap.xml y enlaces desde páginas de servicio existentes
Idempotente: python3 scripts/build_landings_servicios.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://electromecanico247.com"
WA = "https://wa.me/56973622291?text="
e = html.escape
DATA = json.load(open(os.path.join(ROOT, "scripts", "landings_data.json"), encoding="utf-8"))
EST, INS = DATA["estandar"], DATA["instalaciones"]
ALL = {x["slug"]: x for x in EST + INS}
HUB = "instalaciones-automotrices"
TITULO_EST = "Mis estimados clientes: nuestro servicio a domicilio tiene un valor estándar para todas las comunas"
COMUNAS = [("santiago", "Santiago"), ("providencia", "Providencia"), ("nunoa", "Ñuñoa"), ("las-condes", "Las Condes"),
           ("maipu", "Maipú"), ("la-florida", "La Florida"), ("puente-alto", "Puente Alto"), ("san-miguel", "San Miguel"),
           ("estacion-central", "Estación Central"), ("pedro-aguirre-cerda", "Pedro Aguirre Cerda"),
           ("la-cisterna", "La Cisterna"), ("penalolen", "Peñalolén")]
ACCENT = "#0d7377"


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def write(p, s):
    open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def h1_existente(slug):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", read(f"servicios/{slug}.html"), re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else slug.replace("-", " ").capitalize()


def wa(texto):
    return WA + texto.replace(" ", "%20")


HEAD_COMMON = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G3PYMQQNC2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G3PYMQQNC2');</script>
  <link rel="icon" type="image/jpeg" href="/favicon.jpg">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="/css/styles.css">
  <style>
    body { background:#fff; }
    .svc-nav { position:fixed; top:0; left:0; right:0; z-index:1000; display:flex; align-items:center; gap:14px; padding:12px 20px; background:rgba(26,26,26,.88); }
    .svc-nav a { color:#fff; text-decoration:none; font-weight:700; font-size:.9rem; }
    .svc-nav .svc-brand { margin-right:auto; }
    .svc-nav .svc-wa { background:#25D366; padding:7px 14px; border-radius:20px; }
    @media (max-width:576px) { .svc-nav .svc-hide-sm { display:none; } }
    .hero-section { width:100%; background:url('/images/electromecanico-a-domicilio-en-santiago.jpg') no-repeat center center / contain; background-color:#fff; aspect-ratio:16/9; max-height:45vh; margin-top:64px; }
    .hero-text-section { padding:40px 0 30px; text-align:center; color:#1a1a2e; }
    .hero-text-section .lead { color:#4a5568; max-width:720px; margin:16px auto; }
    .svc-faq { background:#fff; border:0.5px solid rgba(60,60,67,.18); border-radius:14px; padding:14px 16px; margin-bottom:10px; }
    .svc-faq summary { font-weight:600; cursor:pointer; }
    .svc-box { background:#f0f4f8; border-radius:14px; padding:16px; height:100%; }
    .svc-link-card { display:block; background:#fff; border-radius:14px; padding:14px; height:100%; text-decoration:none; color:#1a1a2e; box-shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.08); }
    .svc-link-card:hover { color:#0d7377; }
    .svc-link-card i { color:#0d7377; font-size:1.4rem; }
    @media (max-width:768px) { .hero-section { max-height:35vh; } }
  </style>
  <link rel="stylesheet" href="/css/ios-skin.css"/>'''

NAV = '''<nav class="svc-nav">
  <a href="/" class="svc-brand"><strong>ELECTROMECANICO</strong> <small style="color:#999;">en Santiago</small></a>
  <a href="/#servicios" class="svc-hide-sm">Servicios</a>
  <a href="/servicios/instalaciones-automotrices" class="svc-hide-sm">Instalaciones</a>
  <a href="/galeria"><i class="fas fa-images"></i> Galería</a>
  <a href="https://wa.me/56973622291" target="_blank" rel="noopener" class="svc-wa"><i class="fab fa-whatsapp"></i> WhatsApp</a>
</nav>'''

FOOTER = '''<footer class="bg-dark text-white-50 py-4">
  <div class="container text-center small">
    <p class="mb-2">&copy; 2026 Electromecánico en Santiago · Servicio a domicilio en toda la Región Metropolitana · WhatsApp +56 9 7362 2291</p>
    <p class="mb-0"><a href="/" class="text-white-50">Inicio</a> · <a href="/#servicios" class="text-white-50">Servicios</a> ·
      <a href="/servicios/instalaciones-automotrices" class="text-white-50">Instalaciones</a> · <a href="/galeria" class="text-white-50">Galería</a> ·
      <a href="/contacto" class="text-white-50">Contacto</a> · <a href="/faq" class="text-white-50">FAQ</a> · <a href="/politica-privacidad" class="text-white-50">Privacidad</a></p>
  </div>
</footer>'''


def redirect_snippet():
    """Script de redirección del dominio antiguo (tomado del index para mantenerlo igual en todo el sitio)."""
    idx = read("index.html")
    i = idx.find("<!-- REDIRECT 301")
    if i < 0:
        return ""
    j = idx.index("</script>", i) + len("</script>")
    return idx[i:j] + "\n\n"


def page(slug, title, desc, body, lds):
    url = f"{SITE}/servicios/{slug}"
    ld_html = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
{redirect_snippet()}  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Generado por scripts/build_landings_servicios.py: editar scripts/landings_data.json y re-ejecutar -->
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/electromecanico-a-domicilio-en-santiago-og-image.jpg">
  <meta property="og:locale" content="es_CL">
{HEAD_COMMON}
{ld_html}
</head>
<body>
{NAV}
<section class="hero-section" id="inicio" role="img" aria-label="Electromecánico a domicilio en Santiago"></section>
{body}
{FOOTER}
</body>
</html>
'''


def breadcrumb(slug, nombre, mid=None):
    items = [("Inicio", SITE + "/")]
    if mid:
        items.append(mid)
    items.append((nombre, f"{SITE}/servicios/{slug}"))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def landing(x, grupo):
    slug, nombre = x["slug"], x["nombre"]
    title = f"{nombre} a domicilio en Santiago | Electromecánico en Santiago" if "domicilio" not in nombre.lower() else f"{nombre} en Santiago | Electromecánico en Santiago"
    est_note = (f'<div class="alert mt-3 mb-0" style="background:#e6f4f4;color:#0d7377;border:none;border-radius:14px;">'
                f'<i class="fas fa-tag me-2"></i><strong>Valor estándar:</strong> nuestro servicio a domicilio tiene el mismo valor para todas las comunas. Consúltalo por WhatsApp.</div>')
    incluye = "".join(f'<div class="col-md-6"><div class="svc-box"><i class="fas fa-check me-2" style="color:#14a098;"></i>{e(i)}</div></div>' for i in x["incluye"])
    senales = "".join(f'<li class="mb-2"><i class="fas fa-exclamation-circle me-2" style="color:{ACCENT};"></i>{e(s)}</li>' for s in x["senales"])
    pasos = [("fa-comments", "Nos contactas", "Escríbenos por WhatsApp con tu vehículo, comuna y problema."),
             ("fa-map-marker-alt", "Vamos a tu domicilio", "Llegamos donde está tu auto, en toda la Región Metropolitana."),
             ("fa-search", "Diagnóstico", "Revisamos y te explicamos qué necesita antes de empezar."),
             ("fa-tools", "Trabajo y prueba", "Realizamos el trabajo y lo probamos contigo.")]
    pasos_html = "".join(f'<div class="col-6 col-md-3"><div class="svc-box text-center"><div style="font-size:1.5rem;color:{ACCENT};"><i class="fas {ic}"></i></div>'
                         f'<div class="fw-bold mt-2">{i}. {e(t)}</div><div class="text-muted small mt-1">{e(d)}</div></div></div>'
                         for i, (ic, t, d) in enumerate(pasos, 1))
    faq = "".join(f'<details class="svc-faq"><summary>{e(q)}</summary><p class="text-muted mb-0 mt-2">{e(a)}</p></details>' for q, a in x["faq"])
    rel_new = "".join(f'<div class="col-6 col-md-4"><a class="svc-link-card" href="/servicios/{r}"><i class="fas {ALL[r]["icono"]}"></i><div class="fw-bold mt-2">{e(ALL[r]["nombre"])}</div></a></div>' for r in x["relacionados"])
    rel_old = " · ".join(f'<a href="/servicios/{r}" style="color:{ACCENT};">{e(h1_existente(r))}</a>' for r in x["existentes"])
    comunas = " · ".join(f'<a href="/comunas/{c}" style="color:{ACCENT};">{n}</a>' for c, n in COMUNAS)
    hub_link = ('<a href="/#valor-estandar" style="color:%s;">Servicios con valor estándar</a>' % ACCENT if grupo == "estandar"
                else f'<a href="/servicios/{HUB}" style="color:{ACCENT};">Todas las instalaciones automotrices</a>')
    body = f'''<section class="hero-text-section">
  <div class="container">
    <div style="font-size:2.6rem;color:{ACCENT};"><i class="fas {x["icono"]}"></i></div>
    <span class="badge mb-2" style="background:{ACCENT};color:#fff;">Servicio a domicilio en Santiago</span>
    <h1 class="display-5 fw-bold">{e(nombre)}</h1>
    <p class="lead">{e(x["desc"])}</p>
    <a href="{wa("Hola, quiero cotizar " + nombre)}" target="_blank" rel="noopener" class="btn btn-lg text-white fw-bold mt-2" style="background:{ACCENT};"><i class="fab fa-whatsapp me-2"></i>Cotizar por WhatsApp</a>
  </div>
</section>
<section class="py-5">
  <div class="container" style="max-width:900px;">
    <nav aria-label="breadcrumb" class="small mb-3"><a href="/" style="color:{ACCENT};">Inicio</a> › {hub_link} › {e(nombre)}</nav>
    <h2 class="fw-bold mb-3">Sobre el servicio</h2>
    <p class="text-muted">{e(x["intro"])}</p>
    {est_note}
    <h2 class="fw-bold mt-5 mb-3">¿Qué incluye?</h2>
    <div class="row g-3">{incluye}</div>
    <h2 class="fw-bold mt-5 mb-3">¿Cuándo lo necesitas?</h2>
    <ul class="list-unstyled">{senales}</ul>
    <h2 class="fw-bold mt-5 mb-3">Cómo trabajamos a domicilio</h2>
    <div class="row g-3">{pasos_html}</div>
    <h2 class="fw-bold mt-5 mb-3">Preguntas frecuentes</h2>
    {faq}
    <h2 class="fw-bold mt-5 mb-3">Servicios relacionados</h2>
    <div class="row g-3">{rel_new}</div>
    <p class="mt-3 text-muted small">También te puede interesar: {rel_old} · <a href="/servicios/{HUB}" style="color:{ACCENT};">Instalaciones automotrices</a> · <a href="/#valor-estandar" style="color:{ACCENT};">Servicios con valor estándar</a></p>
    <div class="p-4 mt-4 rounded" style="background:#f0f4f8;">
      <h2 class="h5 fw-bold mb-2"><i class="fas fa-images me-2" style="color:{ACCENT};"></i>Mira nuestros trabajos reales</h2>
      <p class="text-muted mb-3">Fotos de vehículos atendidos a domicilio por nuestro equipo en Santiago.</p>
      <a href="/galeria" class="btn fw-bold text-white" style="background:{ACCENT};">Ver galería de trabajos</a>
    </div>
    <h2 class="h5 fw-bold mt-5 mb-2">Atendemos en toda la Región Metropolitana</h2>
    <p class="text-muted small">{comunas} y más comunas.</p>
  </div>
</section>
<section class="py-4 text-center" style="background:{ACCENT};">
  <div class="container">
    <h2 class="text-white fw-bold h4 mb-2">¿Necesitas {e(nombre.lower())}?</h2>
    <p class="text-white-50 mb-3">Cotiza en minutos. Valor estándar del servicio a domicilio en todas las comunas.</p>
    <a href="{wa("Hola, quiero cotizar " + nombre)}" target="_blank" rel="noopener" class="btn btn-lg fw-bold" style="background:#fff;color:{ACCENT};"><i class="fab fa-whatsapp me-2"></i>WhatsApp: +56 9 7362 2291</a>
  </div>
</section>'''
    service = {"@context": "https://schema.org", "@type": "Service", "name": nombre, "description": x["desc"],
               "url": f"{SITE}/servicios/{slug}", "areaServed": {"@type": "AdministrativeArea", "name": "Región Metropolitana de Santiago"},
               "provider": {"@type": "LocalBusiness", "name": "Electromecánico en Santiago", "telephone": "+56 9 7362 2291", "url": SITE}}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in x["faq"]]}
    mid = None if grupo == "estandar" else ("Instalaciones automotrices", f"{SITE}/servicios/{HUB}")
    write(f"servicios/{slug}.html", page(slug, title, x["desc"], body, [service, faq_ld, breadcrumb(slug, nombre, mid)]))


def cards(items, link_fn, cols="col-6 col-md-4 col-lg-3"):
    return "\n".join(f'<div class="{cols}">{link_fn(x)}</div>' for x in items)


def hub():
    desc = "Instalaciones automotrices a domicilio en Santiago: ampolletas H4, H7, H11 y 9007, luces, neblineros, alzavidrios, retrovisores, pantalla Android, cámara y sensores de retroceso."
    ins = cards(INS, lambda x: f'<a class="svc-link-card" href="/servicios/{x["slug"]}"><i class="fas {x["icono"]}"></i><div class="fw-bold mt-2">{e(x["nombre"])}</div><div class="text-muted small mt-1">{e(x["desc"][:90])}…</div></a>')
    est = cards(EST, lambda x: f'<a class="svc-link-card" href="/servicios/{x["slug"]}"><i class="fas {x["icono"]}"></i><div class="fw-bold mt-2">{e(x["nombre"])}</div></a>', "col-6 col-md-4")
    body = f'''<section class="hero-text-section">
  <div class="container">
    <h1 class="display-5 fw-bold">Instalaciones automotrices a domicilio</h1>
    <p class="lead">{e(desc)}</p>
    <a href="{wa("Hola, quiero cotizar una instalación")}" target="_blank" rel="noopener" class="btn btn-lg text-white fw-bold" style="background:{ACCENT};"><i class="fab fa-whatsapp me-2"></i>Cotizar por WhatsApp</a>
  </div>
</section>
<section class="py-5" style="background:#f0f4f8;">
  <div class="container">
    <h2 class="fw-bold text-center mb-4">Instalaciones y servicios relacionados</h2>
    <div class="row g-3">{ins}</div>
  </div>
</section>
<section class="py-5">
  <div class="container" style="max-width:900px;">
    <h2 class="fw-bold text-center mb-2">{e(TITULO_EST)}</h2>
    <p class="text-center text-muted mb-4">Consulta el valor por WhatsApp: es el mismo en todas las comunas de la Región Metropolitana.</p>
    <div class="row g-3">{est}</div>
    <p class="text-center mt-4"><a href="/galeria" style="color:{ACCENT};">Ver galería de trabajos</a> · <a href="/#servicios" style="color:{ACCENT};">Todos los servicios</a> · <a href="/contacto" style="color:{ACCENT};">Contacto</a></p>
  </div>
</section>'''
    lst = {"@context": "https://schema.org", "@type": "ItemList", "name": "Instalaciones automotrices a domicilio",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x["nombre"], "url": f"{SITE}/servicios/{x['slug']}"} for i, x in enumerate(INS)]}
    write(f"servicios/{HUB}.html", page(HUB, "Instalaciones automotrices a domicilio en Santiago | Electromecánico en Santiago", desc, body,
                                        [lst, breadcrumb(HUB, "Instalaciones automotrices")]))


def replace_block(s, name, content, anchor_before):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    block = f"{start}\n{content}\n{end}"
    if start in s:
        return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, s, flags=re.S)
    assert anchor_before in s, anchor_before
    return s.replace(anchor_before, block + "\n\n" + anchor_before, 1)


def modal(mid, titulo, icono, cuerpo, footer):
    return f'''<div class="modal fade" id="{mid}" tabindex="-1" aria-labelledby="{mid}-title" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content" style="border-radius:16px;border:none;">
      <div class="modal-header" style="background:{ACCENT};color:#fff;border-radius:16px 16px 0 0;">
        <h5 class="modal-title" id="{mid}-title"><i class="fas {icono} me-2"></i>{e(titulo)}</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
      </div>
      <div class="modal-body p-4">{cuerpo}</div>
      <div class="modal-footer" style="border:none;">{footer}</div>
    </div>
  </div>
</div>'''


def build_index():
    s = read("index.html")
    est_cards = cards(EST, lambda x: f'''<div class="card h-100 shadow-sm border-0 text-center" style="border-top:4px solid {ACCENT}!important;border-radius:14px!important;cursor:pointer;" role="button" tabindex="0" data-bs-toggle="modal" data-bs-target="#modal-std-{x["slug"]}">
      <div class="card-body p-3"><div style="font-size:2rem;color:{ACCENT};" class="mb-2"><i class="fas {x["icono"]}"></i></div>
      <h3 class="h6 fw-bold text-dark mb-1">{e(x["nombre"])}</h3><p class="small text-muted mb-0">Ver detalle <i class="fas fa-arrow-right ms-1"></i></p></div></div>''', "col-6 col-md-4 col-lg-2")
    sec_est = f'''<section class="py-5 bg-white" id="valor-estandar">
  <div class="container">
    <div class="text-center mb-4">
      <span class="badge mb-2" style="background:#14a098;color:#fff;padding:6px 16px;border-radius:20px;">Valor estándar</span>
      <h2 class="fw-bold" style="color:{ACCENT};">{e(TITULO_EST)}</h2>
      <p class="text-muted mx-auto" style="max-width:640px;">El valor de la visita es el mismo en todas las comunas de la Región Metropolitana. Haz clic en un servicio para ver el detalle o consulta el valor por WhatsApp.</p>
    </div>
    <div class="row g-3 justify-content-center">
{est_cards}
    </div>
  </div>
</section>'''
    chips = " ".join(f'<a href="/servicios/{x["slug"]}" class="btn btn-sm btn-outline-secondary m-1">{e(x["nombre"])}</a>' for x in INS[:8])
    sec_ins = f'''<section class="py-5" style="background:#f0f4f8;" id="instalaciones">
  <div class="container text-center">
    <h2 class="fw-bold" style="color:{ACCENT};"><i class="fas fa-tools me-2"></i>Instalaciones y servicios relacionados</h2>
    <p class="text-muted mx-auto" style="max-width:640px;">Ampolletas, luces, neblineros, alzavidrios, retrovisores, pantalla Android, cámara y sensores de retroceso, instalados a domicilio.</p>
    <div class="mb-3">{chips}</div>
    <button type="button" class="btn btn-lg fw-bold text-white" style="background:{ACCENT};" data-bs-toggle="modal" data-bs-target="#modal-instalaciones"><i class="fas fa-list me-2"></i>Ver todas las instalaciones</button>
    <a href="/servicios/{HUB}" class="btn btn-lg btn-outline-secondary fw-bold"><i class="fas fa-external-link-alt me-2"></i>Página de instalaciones</a>
  </div>
</section>'''
    modales = []
    for x in EST:
        lis = "".join(f'<li><i class="fas fa-check-circle me-2" style="color:#14a098;"></i>{e(i)}</li>' for i in x["incluye"])
        cuerpo = (f'<p>{e(x["intro"])}</p><div class="alert" style="background:#e6f4f4;color:{ACCENT};border:none;border-radius:12px;">'
                  f'<i class="fas fa-tag me-2"></i>Valor estándar para todas las comunas.</div>'
                  f'<h6 class="fw-bold" style="color:{ACCENT};">Incluye</h6><ul class="list-unstyled mb-0">{lis}</ul>')
        footer = (f'<a href="/servicios/{x["slug"]}" class="btn btn-outline-secondary fw-bold">Ver página del servicio</a>'
                  f'<a href="{wa("Hola, quiero consultar el valor de " + x["nombre"])}" target="_blank" rel="noopener" class="btn fw-bold text-white" style="background:#14a098;"><i class="fab fa-whatsapp me-1"></i>Consultar valor</a>')
        modales.append(modal(f'modal-std-{x["slug"]}', x["nombre"], x["icono"], cuerpo, footer))
    lista = "".join(f'<div class="col-12 col-md-6"><a href="/servicios/{x["slug"]}" class="d-flex align-items-start gap-2 p-2 rounded text-decoration-none" style="background:#f0f4f8;color:#1a1a2e;">'
                    f'<i class="fas {x["icono"]} mt-1" style="color:{ACCENT};"></i><span><strong>{e(x["nombre"])}</strong><br><small class="text-muted">{e(x["desc"][:80])}…</small></span></a></div>' for x in INS)
    modales.append(modal("modal-instalaciones", "Instalaciones y servicios relacionados", "fa-tools",
                         f'<div class="row g-2">{lista}</div>',
                         f'<a href="/servicios/{HUB}" class="btn fw-bold text-white" style="background:{ACCENT};">Ver página de instalaciones</a>'))
    s = replace_block(s, "VALOR-ESTANDAR", sec_est + "\n\n" + sec_ins, "<!-- SERVICIOS PRINCIPALES -->")
    s = replace_block(s, "LANDINGS-MODALES", "\n".join(modales), "<!-- MODALES DE SERVICIOS -->")
    if f'href="/servicios/{HUB}">' not in s.split("</nav>")[0]:
        s = s.replace('<li><a class="dropdown-item" href="/servicios/trabajos-de-electricidad">Trabajos de Electricidad</a></li>',
                      f'<li><a class="dropdown-item" href="/servicios/{HUB}">Instalaciones Automotrices</a></li>\n            '
                      '<li><a class="dropdown-item" href="/servicios/trabajos-de-electricidad">Trabajos de Electricidad</a></li>', 1)
    write("index.html", s)


def sitemap():
    s = read("sitemap.xml")
    add = ""
    for slug in [HUB] + list(ALL):
        loc = f"{SITE}/servicios/{slug}"
        if loc + "<" not in s:
            add += f"  <url><loc>{loc}</loc><lastmod>2026-10-11</lastmod><priority>0.8</priority><changefreq>monthly</changefreq></url>\n"
    if add:
        write("sitemap.xml", s.replace("</urlset>", add + "</urlset>", 1))


def enlaces_entrantes():
    """Agrega 'instalaciones' a las páginas de servicio existentes reparadas (servicios_contexto.json)."""
    p = os.path.join(ROOT, "scripts", "servicios_contexto.json")
    ctx = json.load(open(p, encoding="utf-8"))
    for x in EST + INS:
        for ex in x["existentes"]:
            if ex in ctx:
                lst = ctx[ex].setdefault("instalaciones", [])
                if x["slug"] not in lst:
                    lst.append(x["slug"])
    json.dump(ctx, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(p, "a").write("\n")


if __name__ == "__main__":
    for x in EST:
        landing(x, "estandar")
    for x in INS:
        landing(x, "instalaciones")
    hub()
    build_index()
    sitemap()
    enlaces_entrantes()
    print(f"Landings: {len(ALL)} + hub; index y sitemap actualizados")
