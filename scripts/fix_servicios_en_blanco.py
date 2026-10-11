#!/usr/bin/env python3
"""Repara las páginas de /servicios que se veían en blanco y les agrega contexto.

Problema: un bloque <style> quedó cortado (".hero-text-sectio<section ...") sin
</style></head><body>, por lo que todo el contenido quedaba dentro del CSS.

Arreglo (sin borrar contenido): cierra el <style>, agrega </head><body>, un menú
superior, saca 'text-white-50' del subtítulo del hero (texto blanco sobre blanco)
e inserta una sección de contexto por servicio desde servicios_contexto.json
(señales de falla, cómo trabajamos, FAQ, comunas, relacionados, galería) +
JSON-LD Service y FAQPage. Idempotente.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://electromecanico-en-santiago.pages.dev"
LANDINGS = json.load(open(os.path.join(ROOT, "scripts", "landings_data.json"), encoding="utf-8"))
DATA = json.load(open(os.path.join(ROOT, "scripts", "servicios_contexto.json"), encoding="utf-8"))
e = html.escape

COMUNAS = [("santiago", "Santiago"), ("providencia", "Providencia"), ("nunoa", "Ñuñoa"), ("las-condes", "Las Condes"),
           ("maipu", "Maipú"), ("la-florida", "La Florida"), ("puente-alto", "Puente Alto"), ("san-miguel", "San Miguel"),
           ("estacion-central", "Estación Central"), ("pedro-aguirre-cerda", "Pedro Aguirre Cerda"),
           ("la-cisterna", "La Cisterna"), ("penalolen", "Peñalolén")]


def h1_of(s):
    return re.search(r"<h1[^>]*>([^<]*)</h1>", s).group(1).strip()


def nav(accent):
    return f'''<style>
  .svc-nav {{ position:fixed; top:0; left:0; right:0; z-index:1000; display:flex; align-items:center; gap:14px; padding:12px 20px; background:rgba(26,26,26,.88); }}
  .svc-nav a {{ color:#fff; text-decoration:none; font-weight:700; font-size:.9rem; }}
  .svc-nav .svc-brand {{ margin-right:auto; }}
  .svc-nav .svc-wa {{ background:#25D366; padding:7px 14px; border-radius:20px; }}
  @media (max-width:576px) {{ .svc-nav .svc-hide-sm {{ display:none; }} }}
</style>
<nav class="svc-nav">
  <a href="/" class="svc-brand"><strong>ELECTROMECANICO</strong> <small style="color:#999;">en Santiago</small></a>
  <a href="/#servicios" class="svc-hide-sm">Servicios</a>
  <a href="/galeria"><i class="fas fa-images"></i> Galería</a>
  <a href="https://wa.me/56973622291" target="_blank" rel="noopener" class="svc-wa"><i class="fab fa-whatsapp"></i> WhatsApp</a>
</nav>'''


def ld(slug, titulo, desc, d):
    service = {"@context": "https://schema.org", "@type": "Service", "name": titulo,
               "serviceType": d["nombre"], "description": desc, "url": f"{SITE}/servicios/{slug}",
               "areaServed": {"@type": "AdministrativeArea", "name": "Región Metropolitana de Santiago"},
               "provider": {"@type": "LocalBusiness", "name": "Electromecánico en Santiago",
                            "telephone": "+56 9 7362 2291", "url": SITE}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in d["faq"]]}
    return "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>'
                     for x in (service, faq))


def contexto(slug, titulo, d, accent, titles):
    senales = "".join(f'<li class="mb-2"><i class="fas fa-exclamation-circle me-2" style="color:{accent};"></i>{e(x)}</li>' for x in d["senales"])
    pasos = [("fa-comments", "Nos contactas", "Cotiza por WhatsApp o teléfono y cuéntanos qué le pasa a tu vehículo."),
             ("fa-map-marker-alt", "Vamos a tu domicilio", "Llegamos a tu casa, oficina o donde esté el auto, en toda la Región Metropolitana."),
             ("fa-search", "Diagnóstico", f"Revisamos el sistema con herramientas profesionales y te explicamos qué necesita antes de empezar."),
             ("fa-tools", "Reparación y prueba", "Realizamos el trabajo en el lugar y probamos el vehículo contigo antes de terminar.")]
    pasos_html = "".join(
        f'<div class="col-6 col-md-3"><div class="p-3 h-100 text-center rounded" style="background:#f0f4f8;">'
        f'<div style="font-size:1.6rem;color:{accent};"><i class="fas {ic}"></i></div>'
        f'<div class="fw-bold mt-2">{i}. {e(t)}</div><div class="text-muted small mt-1">{e(x)}</div></div></div>'
        for i, (ic, t, x) in enumerate(pasos, 1))
    faq_html = "".join(
        f'<details class="svc-faq"><summary>{e(q)}</summary><p class="text-muted mb-0 mt-2">{e(a)}</p></details>'
        for q, a in d["faq"])
    comunas = " · ".join(f'<a href="/comunas/{c}" style="color:{accent};">{n}</a>' for c, n in COMUNAS)
    rel = "".join(f'<a href="/servicios/{r}" class="btn btn-outline-secondary btn-sm m-1">{e(titles.get(r, r))}</a>' for r in d["relacionados"])
    nuevas = {x["slug"]: x["nombre"] for g in LANDINGS.values() for x in g}
    ins = "".join(f'<a href="/servicios/{r}" class="btn btn-outline-secondary btn-sm m-1">{e(nuevas[r])}</a>' for r in d.get("instalaciones", []) if r in nuevas)
    if ins:
        rel += f'</div>\n      <h2 class="h5 fw-bold mt-4 mb-2">Instalaciones relacionadas</h2>\n      <div>{ins} <a href="/servicios/instalaciones-automotrices" class="btn btn-sm m-1 text-white" style="background:{accent};">Ver todas</a>'
    return f'''<style>
    .svc-faq {{ background:#fff; border:0.5px solid rgba(60,60,67,.18); border-radius:14px; padding:14px 16px; margin-bottom:10px; }}
    .svc-faq summary {{ font-weight:600; cursor:pointer; }}
  </style>
  <section class="py-5 bg-white" id="contexto-servicio">
    <div class="container" style="max-width:900px;">
      <h2 class="fw-bold mb-3">¿Cuándo necesitas el servicio de {e(d["nombre"])}?</h2>
      <p class="text-muted">Estas señales indican que conviene revisar tu vehículo. Atenderlas a tiempo evita fallas mayores y reparaciones más costosas.</p>
      <ul class="list-unstyled">{senales}</ul>

      <h2 class="fw-bold mt-5 mb-3">Cómo trabajamos a domicilio</h2>
      <div class="row g-3">{pasos_html}</div>

      <h2 class="fw-bold mt-5 mb-3">Preguntas frecuentes sobre {e(d["nombre"])}</h2>
      <div id="faq-{slug}">{faq_html}</div>

      <div class="p-4 mt-5 rounded" style="background:#f0f4f8;">
        <h2 class="h5 fw-bold mb-2"><i class="fas fa-images me-2" style="color:{accent};"></i>Mira nuestros trabajos reales</h2>
        <p class="text-muted mb-3">Revisa fotos de vehículos atendidos a domicilio por nuestro equipo en Santiago.</p>
        <a href="/galeria" class="btn fw-bold text-white" style="background:{accent};">Ver galería de trabajos</a>
      </div>

      <h2 class="h5 fw-bold mt-5 mb-2">Atendemos en toda la Región Metropolitana</h2>
      <p class="text-muted small">{comunas} y más comunas.</p>

      <h2 class="h5 fw-bold mt-4 mb-2">Servicios relacionados</h2>
      <div>{rel}</div>
    </div>
  </section>'''


def main():
    titles = {}
    for slug in DATA:
        titles[slug] = h1_of(open(os.path.join(ROOT, "servicios", slug + ".html"), encoding="utf-8").read())
    fixed = 0
    for slug, d in DATA.items():
        p = os.path.join(ROOT, "servicios", slug + ".html")
        s = open(p, encoding="utf-8").read()
        titulo = titles[slug]
        accent = "#14a098" if "background:#14a098" in s else "#0d7377"
        desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
        hero = '<section class="hero-section" id="inicio"></section>'
        if "</head>" not in s and hero in s:
            # Se descarta solo el fragmento de CSS truncado entre la última regla completa y el hero
            i = s.index(hero)
            cut = s.rindex("}", 0, i) + 1
            head_end = (f'\n  .hero-text-section .lead {{ color: #4a5568; }}\n  </style>\n{ld(slug, titulo, desc, d)}\n'
                        f'</head>\n<body>\n{nav(accent)}\n\n')
            s = s[:cut] + head_end + s[i:]
            s = s.replace('<p class="lead text-white-50 mx-auto"', '<p class="lead mx-auto"', 1)
            fixed += 1
        block = contexto(slug, titulo, d, accent, titles)
        start, end = "<!-- SERVICIO-CONTEXTO:START -->", "<!-- SERVICIO-CONTEXTO:END -->"
        if start in s:
            s = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: f"{start}\n  {block}\n  {end}", s, flags=re.S)
        else:
            s = s.replace('  <section class="py-4"', f"  {start}\n  {block}\n  {end}\n  <section class=\"py-4\"", 1)
        open(p, "w", encoding="utf-8").write(s)
    print(f"Páginas reparadas: {fixed}; contexto actualizado en {len(DATA)} páginas")


if __name__ == "__main__":
    main()
