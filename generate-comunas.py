#!/usr/bin/env python3
"""
Generate 52 commune-specific landing pages for GlobalPro Automotriz.
Each page is SEO-optimized with unique content mentioning the commune name.
"""

import os
import html
import unicodedata

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comunas")
BASE_URL = "https://mecanico247.com"
PHONE = "+569 39026185"
PHONE_CLEAN = "56939026185"
EMAIL = "contacto@globalpro.cl"

comunas = [
    "Alhue", "Buin", "Calera de Tango", "Cerrillos", "Cerro Navia", "Colina",
    "Conchali", "Curacavi", "El Bosque", "El Monte", "Estacion Central",
    "Huechuraba", "Independencia", "Isla de Maipo", "La Cisterna",
    "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes",
    "Lampa", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipu",
    "Maria Pinto", "Melipilla", "Nunoa", "Padre Hurtado", "Paine",
    "Pedro Aguirre Cerda", "Penalolen", "Penaflor", "Pirque", "Providencia",
    "Pudahuel", "Puente Alto", "Quilicura", "Quinta Normal", "Recoleta",
    "Renca", "San Bernardo", "San Joaquin", "San Jose de Maipo", "San Miguel",
    "San Pedro", "San Ramon", "Santiago", "Talagante", "Tiltil", "Vitacura"
]

# Display names with proper accents for the HTML content
display_names = {
    "Alhue": "Alhué",
    "Buin": "Buín",
    "Calera de Tango": "Calera de Tango",
    "Cerrillos": "Cerrillos",
    "Cerro Navia": "Cerro Navia",
    "Colina": "Colina",
    "Conchali": "Conchalí",
    "Curacavi": "Curacaví",
    "El Bosque": "El Bosque",
    "El Monte": "El Monte",
    "Estacion Central": "Estación Central",
    "Huechuraba": "Huechuraba",
    "Independencia": "Independencia",
    "Isla de Maipo": "Isla de Maipo",
    "La Cisterna": "La Cisterna",
    "La Florida": "La Florida",
    "La Granja": "La Granja",
    "La Pintana": "La Pintana",
    "La Reina": "La Reina",
    "Las Condes": "Las Condes",
    "Lampa": "Lampa",
    "Lo Barnechea": "Lo Barnechea",
    "Lo Espejo": "Lo Espejo",
    "Lo Prado": "Lo Prado",
    "Macul": "Macul",
    "Maipu": "Maipú",
    "Maria Pinto": "María Pinto",
    "Melipilla": "Melipilla",
    "Nunoa": "Ñuñoa",
    "Padre Hurtado": "Padre Hurtado",
    "Paine": "Paine",
    "Pedro Aguirre Cerda": "Pedro Aguirre Cerda",
    "Penalolen": "Peñalolén",
    "Penaflor": "Peñaflor",
    "Pirque": "Pirque",
    "Providencia": "Providencia",
    "Pudahuel": "Pudahuel",
    "Puente Alto": "Puente Alto",
    "Quilicura": "Quilicura",
    "Quinta Normal": "Quinta Normal",
    "Recoleta": "Recoleta",
    "Renca": "Renca",
    "San Bernardo": "San Bernardo",
    "San Joaquin": "San Joaquín",
    "San Jose de Maipo": "San José de Maipo",
    "San Miguel": "San Miguel",
    "San Pedro": "San Pedro",
    "San Ramon": "San Ramón",
    "Santiago": "Santiago",
    "Talagante": "Talagante",
    "Tiltil": "Tiltil",
    "Vitacura": "Vitacura"
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def slugify(name):
    """Remove accents, lowercase, replace spaces with hyphens."""
    nfkd = unicodedata.normalize('NFKD', name)
    no_accents = ''.join(c for c in nfkd if not unicodedata.category(c).startswith('M'))
    slug = no_accents.lower().replace(' ', '-')
    return slug

def generate_seo_text(comuna_display):
    """Generate unique SEO intro paragraphs mentioning the commune 3-5 times naturally."""
    c = comuna_display
    return f"""
        <p>
            Buscando un <strong>mecánico a domicilio en {c}</strong>? En <strong>GlobalPro Automotriz</strong> entendemos que los residentes de <strong>{c}</strong> necesitan soluciones rápidas y confiables para el mantenimiento de sus vehículos. Nuestro equipo de técnicos certificados se desplaza directamente a tu hogar, oficina o ubicación en <strong>{c}</strong>, llevando herramientas de diagnóstico de última generación y repuestos de calidad para resolver cualquier problema mecánico sin que tengas que moverte.
        </p>
        <p>
            Ya sea que necesites un <strong>cambio de aceite</strong>, <strong>reparación de frenos</strong>, <strong>diagnóstico con scanner</strong> o un <strong>servicio de emergencia 24/7</strong>, en GlobalPro tenemos la experiencia y el compromiso para atenderte en <strong>{c}</strong> con la misma calidad de un taller formal pero con la comodidad de estar en tu propia puerta. Nos enorgullece ser el servicio de <strong>mecánico a domicilio</strong> más confiable de la Región Metropolitana, con más de 5.000 clientes satisfechos que nos recomiendan.
        </p>
        <p>
            <strong>{c}</strong> es una de las comunas donde mayor demanda tenemos, y por eso hemos optimizado nuestros tiempos de respuesta para que un técnico esté contigo en menos de lo que imaginas. Si tu auto no arranca, tienes una falla en el sistema eléctrico, o simplemente necesitas la <strong>mantención preventiva</strong> al día, nuestro <strong>mecánico a domicilio en {c}</strong> es la solución. Contáctanos por WhatsApp y agenda tu cita hoy mismo.
        </p>
"""

def build_dropdown_items(current_comuna_display):
    """Build the communes dropdown, highlighting the current one."""
    all_comunas_display = [
        "Alhué", "Buín", "Calera de Tango", "Cerrillos", "Cerro Navia", "Colina",
        "Conchalí", "Curacaví", "El Bosque", "El Monte", "Estación Central",
        "Huechuraba", "Independencia", "Isla de Maipo", "La Cisterna",
        "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes",
        "Lampa", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
        "María Pinto", "Melipilla", "Ñuñoa", "Padre Hurtado", "Paine",
        "Pedro Aguirre Cerda", "Peñaflor", "Peñalolén", "Pirque", "Providencia",
        "Pudahuel", "Puente Alto", "Quilicura", "Quinta Normal", "Recoleta",
        "Renca", "San Bernardo", "San Joaquín", "San José de Maipo", "San Miguel",
        "San Pedro", "San Ramón", "Santiago", "Talagante", "Tiltil", "Vitacura"
    ]
    items = []
    for cd in all_comunas_display:
        if cd == current_comuna_display:
            items.append(f'<li><a class="dropdown-item active" href="#" aria-current="page">{cd}</a></li>')
        else:
            items.append(f'<li><a class="dropdown-item" href="../index.html#contacto">{cd}</a></li>')
    return ''.join(items)

# ============================================================
# TEMPLATE BUILDER
# ============================================================

def generate_page(comuna_key, comuna_display, slug):
    """Generate the full HTML page for a commune."""
    canonical = f"{BASE_URL}/comunas/{slug}.html"
    title = f"Mecanico a Domicilio en {comuna_display} | GlobalPro Automotriz - Santiago"
    description = f"Servicio de mecanico a domicilio en {comuna_display}, Santiago 24/7. Reparacion de frenos, embrague, electricidad, scanner, aire acondicionado, mantencion preventiva. +5.000 clientes atendidos. Cotiza por WhatsApp."
    wa_text = f"Hola%20necesito%20un%20mecanico%20a%20domicilio%20en%20{slugify(comuna_key).replace('-', '%20')}"

    dropdown_items = build_dropdown_items(comuna_display)
    seo_text = generate_seo_text(comuna_display)

    page = f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>

<link rel="icon" type="image/png" href="../images/mecanico-a-domicilio-en-santiago.png"/>
<link rel="apple-touch-icon" href="../images/mecanico-a-domicilio-en-santiago.png"/>

<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}"/>
<link rel="canonical" href="{canonical}"/>

<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(description)}"/>
<meta property="og:image" content="https://globalpro.pages.dev/images/mecanico-a-domicilio-en-santiago.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="es_CL"/>
<meta property="og:site_name" content="GlobalPro Automotriz"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{html.escape(title)}"/>
<meta name="twitter:description" content="{html.escape(description)}"/>
<meta name="twitter:image" content="https://globalpro.pages.dev/images/mecanico-a-domicilio-en-santiago.png"/>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
<link rel="stylesheet" href="../css/styles.css"/>
<script src="https://elfsightcdn.com/platform.js" async></script>

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-NK35S8FG');</script>
<!-- End Google Tag Manager -->

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "GlobalPro Taller Mecánico - {html.escape(comuna_display)}",
  "image": "https://globalpro.pages.dev/images/mecanico-a-domicilio-en-santiago.png",
  "telephone": "{PHONE}",
  "email": "{EMAIL}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{html.escape(comuna_display)}",
    "addressRegion": "Región Metropolitana",
    "addressCountry": "CL"
  }},
  "url": "{canonical}",
  "description": "Servicio de mecánico a domicilio en {html.escape(comuna_display)}, Santiago. Reparación de frenos, embrague, electricidad, scanner, aire acondicionado, mantenimiento preventivo. 24/7.",
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }},
  "areaServed": {{
    "@type": "City",
    "name": "{html.escape(comuna_display)}"
  }},
  "priceRange": "$$"
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "¿Cuánto cuesta el mecánico a domicilio en {html.escape(comuna_display)}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "El costo depende del servicio solicitado. Cotiza sin compromiso por WhatsApp y recibiras un presupuesto transparente sin sorpresas."
      }}
    }},
    {{
      "@type": "Question",
      "name": "¿Cuánto demoran en llegar a {html.escape(comuna_display)}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "En la mayoría de los casos atendemos en menos de 24 horas. Nuestro servicio de emergencia 24/7 puede llegar incluso el mismo día a {html.escape(comuna_display)}."
      }}
    }},
    {{
      "@type": "Question",
      "name": "¿Qué servicios de mecánica ofrecen en {html.escape(comuna_display)}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Ofrecemos mecánica general, reparación de frenos, embrague, electricidad automotriz, aire acondicionado, scanner diagnóstico, mantenimiento preventivo y más, todo a domicilio en {html.escape(comuna_display)}."
      }}
    }}
  ]
}}
</script>

<style>
  :root {{
    --gp-blood-red: #a80000;
    --gp-black: #121212;
  }}
  html {{ scroll-behavior: smooth; scroll-padding-bottom: 120px; }}
  .text-primary {{ color: var(--gp-blood-red) !important; }}
  .btn-primary {{
    background-color: var(--gp-blood-red) !important;
    border-color: var(--gp-blood-red) !important;
    color: white !important;
  }}
  .btn-primary:hover, .btn-primary:focus {{
    background-color: #800000 !important;
    border-color: #800000 !important;
    box-shadow: 0 0 15px rgba(168, 0, 0, 0.4);
  }}
  .bg-primary {{ background-color: var(--gp-blood-red) !important; }}
  .border-primary {{ border-color: var(--gp-blood-red) !important; }}
  .nav-link {{ color: #ccc !important; transition: 0.3s; }}
  .nav-link:hover, .nav-link.active {{ color: var(--gp-blood-red) !important; }}
  .logo-img {{
    background-color: var(--gp-blood-red);
    width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;
    border-radius: 8px; margin-right: 15px; overflow: hidden;
    color: white; font-weight: bold; font-size: 1.2rem;
  }}
  body, .navbar, .container, .container-fluid {{ overflow-x: hidden !important; max-width: 100%; }}
  .nav-container {{ padding: 0 15px; }}
  .whatsapp-btn {{
    background-color: #25d366; border-color: #25d366; color: white;
    font-weight: 500; padding: 8px 20px; border-radius: 50px;
  }}
  .whatsapp-btn:hover {{ background-color: #128c7e; border-color: #128c7e; color: white; }}

  .hero-section {{
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('../images/image1.jpg') no-repeat center center/cover;
    min-height: 90vh; display: flex; align-items: center; text-align: left; color: white;
  }}
  .hero-badge {{ background-color: #FFC107; color: #212529; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; }}
  .hero-title {{ font-weight: 700; font-size: 3.5rem; line-height: 1.2; margin-top: 20px; }}
  .hero-subtitle {{ font-size: 1.2rem; max-width: 500px; margin: 20px 0; }}
  .stats-container {{ margin-top: 40px; }}
  .stat-item {{ padding: 15px; }}
  .stat-number {{ font-size: 2rem; font-weight: 700; color: #FFC107; }}
  .stat-label {{ font-size: 0.9rem; text-transform: uppercase; }}

  .section-title {{ font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 20px; }}
  .section-subtitle {{ text-align: center; max-width: 700px; margin: 0 auto 60px auto; color: #6c757d; }}
  .services-section, .why-us-section {{ padding: 80px 0; }}

  .service-card {{
    border: none; transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); height: 100%;
    display: flex; flex-direction: column;
  }}
  .service-card:hover {{ transform: translateY(-10px); box-shadow: 0 8px 25px rgba(0,0,0,0.12); }}
  .service-card .card-body {{ flex-grow: 1; display: flex; flex-direction: column; }}
  .service-icon {{
    width: 80px; height: 80px; background-color: #f8f9fa; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 2rem;
    color: var(--gp-blood-red); transition: background-color 0.3s, color 0.3s; margin: 0 auto 20px auto;
  }}
  .service-card:hover .service-icon {{ background-color: var(--gp-blood-red); color: white; }}
  .service-title {{ font-size: 1.3rem; font-weight: 600; text-align: center; margin-bottom: 15px; }}
  .service-card p {{ text-align: center; flex-grow: 1; }}
  .service-card .btn {{ align-self: center; }}

  .seo-section {{
    background-color: #f8f9fa; padding: 60px 0;
    border-bottom: 5px solid var(--gp-blood-red);
  }}
  .seo-h1 {{
    color: var(--gp-blood-red); font-weight: 800; font-size: 2.5rem;
    margin-bottom: 1.5rem; text-transform: uppercase; text-align: center;
  }}
  .seo-h2 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 1.5rem; color: #333; text-align: center; }}
  .seo-text p {{ font-size: 1.1rem; line-height: 1.8; color: #555; margin-bottom: 1.5rem; text-align: justify; }}
  .seo-highlight {{
    color: var(--gp-blood-red); font-weight: bold;
    background-color: rgba(168, 0, 0, 0.05); padding: 0 5px; border-radius: 4px;
  }}

  .accordion-button:not(.collapsed) {{ background-color: var(--gp-blood-red); color: white; }}
  .accordion-button:focus {{ box-shadow: 0 0 0 0.25rem rgba(168, 0, 0, 0.25); }}

  .sticky-bottom-bar {{
    position: fixed; bottom: 0; left: 0; width: 100%; height: 90px;
    background-color: var(--gp-black); color: white; display: flex;
    justify-content: center; align-items: center; padding: 0 15px; z-index: 9999;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.6); border-top: 3px solid var(--gp-blood-red);
  }}
  .big-buttons-container {{
    display: flex; justify-content: space-between; align-items: center;
    width: 100%; max-width: 100%; gap: 10px; height: 100%;
  }}
  .btn-massive-call {{
    flex: 1; height: 70px; background-color: #D32F2F; color: white; border: none;
    border-radius: 10px; font-size: 1.5rem; font-weight: 800; text-decoration: none;
    display: flex; align-items: center; justify-content: center; gap: 15px;
    text-transform: uppercase; transition: transform 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    animation: pulse-red 2s infinite;
  }}
  @keyframes pulse-red {{
    0% {{ box-shadow: 0 0 0 0 rgba(211,47,47,0.7); }}
    70% {{ box-shadow: 0 0 0 10px rgba(211,47,47,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(211,47,47,0); }}
  }}
  .btn-massive-call:hover {{ transform: scale(1.02); background-color: #b71c1c; color: white; }}
  .btn-massive-wa {{
    flex: 1; height: 70px; background-color: #25D366; color: white; border: none;
    border-radius: 10px; font-size: 1.2rem; font-weight: 700; text-decoration: none;
    display: flex; align-items: center; justify-content: center; gap: 10px;
    transition: transform 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  }}
  .btn-massive-wa:hover {{ transform: scale(1.02); background-color: #1ebc57; color: white; }}
  .btn-small-chat {{
    width: 50px; height: 50px; background-color: #FFC107; color: black;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; text-decoration: none; flex-shrink: 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3); border: 2px solid white;
  }}
  .btn-small-chat:hover {{ background-color: #ffca2c; transform: scale(1.1); }}

  @media (min-width: 992px) {{
    .sticky-bottom-bar {{ height: 100px; padding: 0 50px; }}
    .big-buttons-container {{ max-width: 1200px; }}
    .btn-massive-call, .btn-massive-wa {{ font-size: 1.8rem; height: 80px; }}
  }}

  .main-footer {{
    background-color: #000; color: #bbb; padding: 60px 0 20px 0;
    font-size: 0.9rem; border-top: 4px solid var(--gp-blood-red);
  }}
  .footer-logo-box {{
    background-color: var(--gp-blood-red); width: 60px; height: 60px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 10px; margin-bottom: 20px;
  }}
  .footer-logo-box i {{ font-size: 1.8rem; color: white; }}
  .footer-title {{
    color: white; font-weight: 700; text-transform: uppercase; margin-bottom: 20px;
    font-size: 1.1rem; border-bottom: 2px solid var(--gp-blood-red);
    display: inline-block; padding-bottom: 5px;
  }}
  .footer-links ul {{ list-style: none; padding: 0; margin: 0; }}
  .footer-links li {{ margin-bottom: 10px; }}
  .footer-links a {{ color: #bbb; text-decoration: none; transition: color 0.3s; }}
  .footer-links a:hover {{ color: var(--gp-blood-red); padding-left: 5px; }}
  .contact-info-item {{ display: flex; align-items: flex-start; margin-bottom: 15px; }}
  .contact-info-item i {{ color: var(--gp-blood-red); margin-right: 10px; margin-top: 5px; }}
  .social-icons a {{
    display: inline-flex; width: 35px; height: 35px; background-color: #333; color: white;
    border-radius: 50%; align-items: center; justify-content: center; margin-right: 10px;
    transition: 0.3s; text-decoration: none;
  }}
  .social-icons a:hover {{ background-color: var(--gp-blood-red); transform: translateY(-3px); }}
  .copyright-bar {{
    background-color: #0a0a0a; padding: 15px 0; margin-top: 40px;
    border-top: 1px solid #333; text-align: center; font-size: 0.85rem;
  }}

  .conectamos-section {{
    background: #121212; padding: 60px 0; overflow: hidden; position: relative;
  }}
  .conectamos-section::before, .conectamos-section::after {{
    content: ''; position: absolute; top: 0; width: 120px; height: 100%;
    z-index: 2; pointer-events: none;
  }}
  .conectamos-section::before {{ left: 0; background: linear-gradient(to right, #121212, transparent); }}
  .conectamos-section::after {{ right: 0; background: linear-gradient(to left, #121212, transparent); }}
  .conectamos-heading {{
    color: #fff; font-size: 1.3rem; font-weight: 600; max-width: 800px;
    margin: 0 auto 40px auto; text-align: center; line-height: 1.6; padding: 0 20px;
  }}
  .marquee-track {{
    display: flex; width: max-content; animation: marquee-scroll 30s linear infinite;
  }}
  .marquee-track:hover {{ animation-play-state: paused; }}
  .marquee-logo-item {{
    flex-shrink: 0; padding: 0 25px; display: flex; align-items: center;
    justify-content: center; height: 80px;
  }}
  .marquee-logo-item img {{
    max-height: 60px; width: auto; filter: grayscale(100%); opacity: 0.6; transition: all 0.3s ease;
  }}
  .marquee-logo-item:hover img {{ filter: grayscale(0%); opacity: 1; transform: scale(1.1); }}
  .conectamos-subtitle {{
    color: #a80000; font-size: 1rem; font-weight: 700; text-align: center;
    margin-top: 30px; letter-spacing: 1px; text-transform: uppercase;
  }}
  @keyframes marquee-scroll {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
  }}
  @media (max-width: 768px) {{
    .hero-section {{ text-align: center; min-height: auto; padding: 120px 0 80px 0; }}
    .hero-title {{ font-size: 2.5rem; }}
    .conectamos-heading {{ font-size: 1rem; }}
    .marquee-logo-item {{ padding: 0 15px; height: 60px; }}
    .marquee-logo-item img {{ max-height: 40px; }}
  }}
  @keyframes modalSlideIn {{
    from {{ transform: translateY(30px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
  }}
  .btn-small-chat {{ animation: pulseChat 2s infinite; }}
  @keyframes pulseChat {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(255,193,7,0.7); }}
    50% {{ box-shadow: 0 0 0 10px rgba(255,193,7,0); }}
  }}
  #resultado-patente-ia {{ max-height: 300px; overflow-y: auto; }}
  #resultado-patente-ia .ot-card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px; margin-bottom: 10px; }}
  #resultado-patente-ia .ot-num {{ font-weight: 700; color: #a80000; }}
  #resultado-patente-ia .ot-estado {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600; }}
  #resultado-patente-ia .badge-ok {{ background: #d4edda; color: #155724; }}
  #resultado-patente-ia .badge-pend {{ background: #fff3cd; color: #856404; }}
  #resultado-patente-ia .dato {{ font-size: 0.85rem; margin-bottom: 3px; color: #374151; }}
  #resultado-patente-ia .notas-tec {{ background: #fffdf5; border-left: 3px solid #ffc800; padding: 6px 8px; border-radius: 4px; margin-top: 6px; font-size: 0.82rem; }}
</style>
</head>
<body>

<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NK35S8FG"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg navbar-dark fixed-top">
  <div class="container nav-container">
    <a href="../index.html" class="logo d-flex align-items-center text-decoration-none text-white">
      <div class="logo-img"><i class="fas fa-wrench"></i></div>
      <div>
        <div class="logo-text">GLOBALPRO</div>
        <div class="logo-subtext">Taller Mecánico</div>
      </div>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse desktop-menu" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="../index.html#mecanico-domicilio-seo">Mecánico a Domicilio</a></li>
        <li class="nav-item"><a class="nav-link" href="../index.html#servicios">Servicios</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle active" href="#" id="comunasDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Comunas</a>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="comunasDropdown" style="max-height: 400px; overflow-y: auto;">
            {dropdown_items}
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="../quienes-somos.html">Quiénes Somos</a></li>
        <li class="nav-item"><a class="nav-link" href="../contacto.html">Contacto</a></li>
        <li class="nav-item"><a class="nav-link" href="../blog/index.html">Blog</a></li>
        <li class="nav-item"><a class="nav-link" href="../vehiculos/index.html">Vehiculos</a></li>
        <li class="nav-item"><a class="nav-link" href="../faq.html">FAQ</a></li>
        <li class="nav-item"><a class="nav-link" href="../politica-privacidad.html">Privacidad</a></li>
        <li class="nav-item">
          <a href="https://wa.me/{PHONE_CLEAN}" class="whatsapp-btn" target="_blank">
            <i class="fab fa-whatsapp me-2"></i> WhatsApp
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<!-- ======================================================================= -->
<!-- HERO -->
<!-- ======================================================================= -->
<section class="hero-section" id="inicio">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-7">
        <span class="hero-badge">Servicio Automotriz Integral</span>
        <h1 class="hero-title">MECÁNICO A DOMICILIO EN {html.escape(comuna_display.upper())}</h1>
        <p class="hero-subtitle">En GlobalPro, somos expertos en mecánica automotriz, electromecánica y mantenimiento. Servicio a domicilio en {html.escape(comuna_display)} y toda la Región Metropolitana. ¡Tu vehículo en las mejores manos!</p>
        <div class="stats-container">
          <div class="row text-center">
            <div class="col-4">
              <div class="stat-item">
                <div class="stat-number">+1000</div>
                <div class="stat-label">Autos Reparados</div>
              </div>
            </div>
            <div class="col-4">
              <div class="stat-item">
                <div class="stat-number">+15</div>
                <div class="stat-label">Años de Experiencia</div>
              </div>
            </div>
            <div class="col-4">
              <div class="stat-item">
                <div class="stat-number">✓</div>
                <div class="stat-label">Garantía de Servicio</div>
              </div>
            </div>
          </div>
        </div>
        <div class="btn-group mt-4">
          <a href="https://wa.me/{PHONE_CLEAN}?text={wa_text}" class="btn btn-primary me-2" target="_blank">
            <i class="fab fa-whatsapp me-2"></i> Cotizar por WhatsApp
          </a>
          <a href="#servicios" class="btn btn-outline-light">
            <i class="fas fa-wrench me-2"></i> Ver Servicios
          </a>
        </div>
      </div>
      <div class="col-lg-5">
        <img src="../images/image1.jpg" alt="Mecánico a domicilio en {html.escape(comuna_display)} - GlobalPro Automotriz" class="img-fluid rounded shadow">
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- SEO SECTION -->
<!-- ======================================================================= -->
<section class="seo-section" id="mecanico-domicilio-seo">
  <div class="container">
    <div class="row">
      <div class="col-lg-12">
        <h1 class="seo-h1 text-center">
          El Mejor <span class="seo-highlight">Mecánico a Domicilio</span> en {html.escape(comuna_display)}: Solución Inmediata
        </h1>
        <h2 class="seo-h2 text-center">
          Servicio Profesional de <span class="seo-highlight">Mecánico a Domicilio</span> en {html.escape(comuna_display)} y toda la Región Metropolitana
        </h2>
        <div class="seo-text">
          {seo_text}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- RESEÑAS -->
<!-- ======================================================================= -->
<section id="resenas" class="py-5 bg-light">
  <div class="container text-center">
    <h2 class="section-title">Lo que dicen nuestros clientes</h2>
    <p class="section-subtitle">Tu confianza es nuestra mejor carta de presentación. Lee las experiencias de quienes ya confían en nuestro trabajo.</p>
    <div class="elfsight-app-4cbd3727-4380-44b3-9cd7-2525ccb8f5d8" data-elfsight-app-lazy></div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- CONECTAMOS MARQUEE -->
<!-- ======================================================================= -->
<section class="conectamos-section">
  <p class="conectamos-heading">Conectamos a propietarios de vehículos con especialistas en mantenciones, revisiones y reparaciones específicas de tu auto en donde lo necesites</p>
  <div class="marquee-track">
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33795.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33793.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33792.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33791.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33790.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-39.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-36.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-35.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33789.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-44.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33795.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33793.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33792.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33791.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33790.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-39.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-36.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-35.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33789.svg" alt="Marca automotriz"></div>
    <div class="marquee-logo-item"><img src="../images/imagen/wp-content/uploads/2024/10/Group-44.svg" alt="Marca automotriz"></div>
  </div>
  <p class="conectamos-subtitle">Atención a domicilio en las comunas de la RM</p>
</section>

<!-- ======================================================================= -->
<!-- SERVICIOS -->
<!-- ======================================================================= -->
<section class="services-section" id="servicios">
  <div class="container">
    <h2 class="section-title">Nuestros Servicios de Mecánica Automotriz</h2>
    <p class="section-subtitle">Ofrecemos una solución completa para el mantenimiento y reparación de tu vehículo en {html.escape(comuna_display)}, desde la mecánica básica hasta el diagnóstico avanzado.</p>
    <div class="row g-4">
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-oil-can"></i></div>
            <h3 class="service-title">Mecánica General y Mantenimiento</h3>
            <p>Realizamos <strong>mantenimiento preventivo</strong>, <strong>engrase general</strong>, <strong>cambio de aceite</strong> y <strong>revisión técnica</strong> para mantener tu auto en óptimas condiciones.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Mecánica%20General%20y%20Mantenimiento%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-car-battery"></i></div>
            <h3 class="service-title">Electromecánica y Electricidad</h3>
            <p>Expertos en <strong>electricidad automotriz</strong>, <strong>reparación de ECU</strong>, <strong>diagnóstico de fallas eléctricas</strong> y <strong>sistema de inyección</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Electromecánica%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-shield-alt"></i></div>
            <h3 class="service-title">Chapa y Pintura Automotriz</h3>
            <p>Recuperamos la estética de tu vehículo con <strong>reparación de carrocería</strong>, <strong>chapa y pintura</strong>, y <strong>reparación de interiores y tapicería</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Chapa%20y%20Pintura%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-temperature-low"></i></div>
            <h3 class="service-title">Aire Acondicionado y Calefacción</h3>
            <p><strong>Reparación y mantenimiento de aire acondicionado auto</strong>. Carga de gas, reparación de <strong>compresor</strong>, <strong>radiador</strong> y <strong>calefacción</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Aire%20Acondicionado%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-circle-stop"></i></div>
            <h3 class="service-title">Frenos y Suspensión</h3>
            <p>Garantizamos tu seguridad con la <strong>reparación de frenos</strong> (discos, pastillas), <strong>suspensión</strong> (amortiguadores) y <strong>dirección</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Frenos%20y%20Suspensión%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-cogs"></i></div>
            <h3 class="service-title">Reparación de Transmisión</h3>
            <p>Diagnóstico y reparación de <strong>transmisiones manuales y automáticas</strong>, <strong>embrague</strong>, <strong>caja de transferencia</strong> y <strong>diferencial</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Transmisión%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-wind"></i></div>
            <h3 class="service-title">Sistema de Escape y Turbos</h3>
            <p>Reparación y mantenimiento de <strong>escapes de autos</strong>, <strong>reparación de turbos</strong>, <strong>catalizador</strong> y <strong>silenciador</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Escape%20y%20Turbos%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-gas-pump"></i></div>
            <h3 class="service-title">Sistemas de Gas GNV/GLP</h3>
            <p>Instalación, certificación y <strong>reparación de sistemas de gas para vehículos</strong>. Conversión y mantenimiento para un ahorro garantizado.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Gas%20GNV/GLP%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-tools"></i></div>
            <h3 class="service-title">Diagnóstico Computarizado</h3>
            <p>Utilizando tecnología de <strong>scanner automotriz</strong>, ofrecemos un <strong>diagnóstico avanzado de fallas</strong> para identificar problemas a tiempo.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text=Hola,%20quiero%20cotizar%20por%20Diagnóstico%20Computarizado%20en%20{html.escape(comuna_display)}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-home"></i></div>
            <h3 class="service-title">Servicio a Domicilio</h3>
            <p>No puedes venir? Nosotros vamos a ti. Ofrecemos <strong>servicio mecánico a domicilio en {html.escape(comuna_display)}</strong> y <strong>auxilio en carretera</strong>.</p>
            <a href="https://wa.me/{PHONE_CLEAN}?text={wa_text}" class="btn btn-outline-primary mt-3" target="_blank">Cotizar Ahora</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- COMO FUNCIONA -->
<!-- ======================================================================= -->
<section class="py-5 bg-light" id="como-funciona">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="section-title">COMO FUNCIONA NUESTRO SERVICIO DE MECÁNICA A DOMICILIO</h2>
      <p class="section-subtitle">Nuestro proceso es simple, rápido y pensado para que no pierdas tiempo. Nos encargamos de todo: desde la cotización hasta la entrega de tu vehículo funcionando en perfectas condiciones.</p>
    </div>
    <div class="row g-4 text-center">
      <div class="col-md-4">
        <div style="background:#fff; border-radius:16px; padding:30px 20px; box-shadow:0 4px 15px rgba(0,0,0,0.08); height:100%;">
          <div style="width:70px; height:70px; background:linear-gradient(135deg,#a80000,#d32f2f); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; color:#fff; font-size:1.8rem; font-weight:800;">1</div>
          <h4 style="color:#a80000; font-weight:700;">COTIZA</h4>
          <p style="color:#555;">Escríbenos al WhatsApp y cotiza tu servicio en {html.escape(comuna_display)} de forma rápida y sin compromiso.</p>
          <a href="https://wa.me/{PHONE_CLEAN}?text={wa_text}" target="_blank" class="btn btn-outline-primary mt-2"><i class="fab fa-whatsapp me-1"></i> Cotizar por WhatsApp</a>
        </div>
      </div>
      <div class="col-md-4">
        <div style="background:#fff; border-radius:16px; padding:30px 20px; box-shadow:0 4px 15px rgba(0,0,0,0.08); height:100%;">
          <div style="width:70px; height:70px; background:linear-gradient(135deg,#FFC107,#FF9800); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; color:#fff; font-size:1.8rem; font-weight:800;">2</div>
          <h4 style="color:#a80000; font-weight:700;">AGENDA</h4>
          <p style="color:#555;">Elige el día y hora que más te acomode. Nuestro técnico llega a tu ubicación en {html.escape(comuna_display)}.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div style="background:#fff; border-radius:16px; padding:30px 20px; box-shadow:0 4px 15px rgba(0,0,0,0.08); height:100%;">
          <div style="width:70px; height:70px; background:linear-gradient(135deg,#28a745,#20c997); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; color:#fff; font-size:1.8rem; font-weight:800;">3</div>
          <h4 style="color:#a80000; font-weight:700;">TU AUTO LISTO EN 2 HORAS</h4>
          <p style="color:#555;">Sin filas, sin quedarte a pie. Tu vehículo reparado directamente en {html.escape(comuna_display)}.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- POR QUE ELEGIRNOS -->
<!-- ======================================================================= -->
<section class="py-5 bg-white" id="por-que-elegirnos">
  <div class="container">
    <div class="text-center mb-4">
      <h2 class="section-title">Por Qué Elegirnos para tu Servicio Mecánico a Domicilio en {html.escape(comuna_display)}</h2>
    </div>
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="row g-3">
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Técnicos calificados y verificados</strong><br><small class="text-muted">Profesionales con experiencia comprobada y certificaciones.</small></div></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Diagnóstico preciso y transparente</strong><br><small class="text-muted">Te explicamos cada falla antes de reparar.</small></div></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Servicio sin anticipos ni sorpresas</strong><br><small class="text-muted">Solo pagas después de recibir el servicio.</small></div></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Cobertura total en {html.escape(comuna_display)}</strong><br><small class="text-muted">Atendemos las 52 comunas de Santiago.</small></div></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Más de 5.000 clientes atendidos</strong><br><small class="text-muted">Calificación 4.9/5 en Google con 148+ reseñas.</small></div></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-3 mt-1" style="font-size:1.2rem;"></i><div><strong>Servicio de emergencia 24/7</strong><br><small class="text-muted">Auxilio mecánico en la vía a cualquier hora.</small></div></div></div>
        </div>
        <p class="text-center mt-4" style="color:#666;">Nuestro objetivo es que tengas la seguridad de estar en manos profesionales, sin moverte de casa en {html.escape(comuna_display)}.</p>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- PREGUNTAS FRECUENTES (FAQ) -->
<!-- ======================================================================= -->
<section class="py-5 bg-light" id="faq">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="section-title">Preguntas Frecuentes - {html.escape(comuna_display)}</h2>
      <p class="section-subtitle">Resolvemos tus dudas sobre nuestro servicio de mecánico a domicilio en {html.escape(comuna_display)}.</p>
    </div>
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="accordion" id="accordionFAQ">
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                ¿Buscas un mecánico a domicilio en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                En Global Pro Automotriz, somos la respuesta inmediata. No importa si estás en tu hogar, oficina o varado en la calle de {html.escape(comuna_display)}; nuestro servicio de mecánico a domicilio cubre toda la Región Metropolitana con rapidez y profesionalismo. Llevamos el taller mecánico a tu ubicación para que no pierdas tiempo ni dinero en grúas.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingTwo">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                ¿Cuánto demoran en llegar a {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                En la mayoría de los casos atendemos en {html.escape(comuna_display)} en menos de 24 horas. Nuestro servicio de emergencia 24/7 puede llegar incluso el mismo día. La rapidez depende de la disponibilidad de nuestros técnicos y la urgencia del caso.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingThree">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                ¿Qué servicios de mecánica ofrecen en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                Ofrecemos mecánica general, reparación de frenos, embrague, suspensión, electricidad automotriz, aire acondicionado, scanner diagnóstico, cambio de aceite, mantenimiento preventivo y correctivo, todo directamente en tu domicilio en {html.escape(comuna_display)}.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingFour">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                ¿Cuánto cuesta el mecánico a domicilio en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                El costo depende del servicio solicitado. Cotiza sin compromiso por WhatsApp y recibirás un presupuesto transparente sin sorpresas. No cobramos anticipos; solo pagas una vez finalizado el servicio en {html.escape(comuna_display)}.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingFive">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
                ¿Tienen especialistas en mecánica de electricidad y alarmas en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseFive" class="accordion-collapse collapse" aria-labelledby="headingFive" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                Absolutamente. Contamos con un eléctrico automotriz a domicilio experto en mecánica de electricidad, diagnóstico de alternadores y motores de partida. Además, realizamos la instalación y reparación de alarmas automotriz y sistemas de seguridad electrónica.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingSix">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSix" aria-expanded="false" aria-controls="collapseSix">
                ¿Hacen reparaciones de aire acondicionado en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseSix" class="accordion-collapse collapse" aria-labelledby="headingSix" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                Ofrecemos un servicio técnico integral que incluye la recarga de aire acondicionado auto y reparación de climatización directamente en {html.escape(comuna_display)}. También gestionamos soluciones para parabrisas y cristales.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="headingSeven">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSeven" aria-expanded="false" aria-controls="collapseSeven">
                ¿Puedo solicitar un cambio de aceite a domicilio en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapseSeven" class="accordion-collapse collapse" aria-labelledby="headingSeven" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">
                ¡Claro que sí! Realizamos el cambio de aceite y filtro directamente en tu domicilio en {html.escape(comuna_display)}, utilizando insumos de alta calidad. Es parte de nuestro compromiso de mantenimiento automotriz preventivo.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading8">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse8" aria-expanded="false" aria-controls="collapse8">
                ¿Qué tipos de vehículos atienden en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapse8" class="accordion-collapse collapse" aria-labelledby="heading8" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">Atendemos autos, camionetas, SUVs y vehículos comerciales livianos de todas las marcas y modelos en {html.escape(comuna_display)}.</div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading9">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse9" aria-expanded="false" aria-controls="collapse9">
                ¿Debo pagar por adelantado en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapse9" class="accordion-collapse collapse" aria-labelledby="heading9" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">No. Solo pagas una vez realizado el servicio. No cobramos anticipos ni sorpresas en el precio.</div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header" id="heading10">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse10" aria-expanded="false" aria-controls="collapse10">
                ¿El diagnóstico incluye scanner en {html.escape(comuna_display)}?
              </button>
            </h2>
            <div id="collapse10" class="accordion-collapse collapse" aria-labelledby="heading10" data-bs-parent="#accordionFAQ">
              <div class="accordion-body">Sí, si el tipo de falla lo requiere, se incluye sin costo adicional. Nuestros técnicos cuentan con scanner automotriz profesional para diagnóstico computarizado.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- MANTENCION POR KILOMETRAJE -->
<!-- ======================================================================= -->
<section class="py-5" style="background:#fff;" id="mantencion-kilometraje">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="section-title">Mantención por Kilometraje en {html.escape(comuna_display)}</h2>
      <p class="section-subtitle">Revisamos todos los puntos indicados en la pauta de mantención de su vehículo según su kilometraje, directamente en {html.escape(comuna_display)}.</p>
    </div>
    <div class="row g-4 justify-content-center">
      <div class="col-lg-8">
        <div class="row g-3">
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Cambio de Filtro y Aceite</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Cambio de Filtro de Aire</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Revisión de Correas</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Cambio de Filtro de Polen</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Revisión de Frenos</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Revisión de Luces</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Revisión de fluidos</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Rotación de Neumáticos</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Scanner Automotriz</span></div></div>
          <div class="col-md-6"><div class="d-flex align-items-start"><i class="fas fa-check-circle text-success me-2 mt-1"></i><span>Asesoramos en Aceite y Filtros</span></div></div>
        </div>
        <div class="mt-4 p-3" style="background:#f8f9fa; border-radius:10px; border-left:4px solid #a80000;">
          <p class="mb-0" style="color:#555;"><strong>Cambio de Aceite y Filtro:</strong> Utilizamos el Aceite indicado por el fabricante o el indicado por el cliente. Usamos el Filtro de Aceite de la Marca o el Alternativo de mejor calidad.</p>
        </div>
        <div class="text-center mt-4">
          <a href="https://wa.me/{PHONE_CLEAN}?text=Hola%20quiero%20cotizar%20una%20mantencion%20por%20kilometraje%20en%20{html.escape(comuna_display)}" target="_blank" class="btn btn-primary btn-lg"><i class="fab fa-whatsapp me-2"></i> Cotizar Mantención</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- MANTENIMIENTO PREVENTIVO -->
<!-- ======================================================================= -->
<section class="py-5" style="background:#fff;" id="mantenimiento-preventivo">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="section-title">Mantenimiento Preventivo: Cuida tu Auto y Ahorra Dinero en {html.escape(comuna_display)}</h2>
      <p class="section-subtitle">La mejor reparación es la que no se necesita. Con un mantenimiento preventivo regular en {html.escape(comuna_display)} evitas fallas costosas y prolongas la vida útil de tu vehículo.</p>
    </div>
    <div class="row g-4">
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-oil-can"></i></div>
            <h3 class="service-title">Cambio de Aceite y Filtro</h3>
            <p>El cambio periódico de aceite es fundamental para proteger el motor. Utilizamos aceites recomendados por el fabricante.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-compact-disc"></i></div>
            <h3 class="service-title">Frenos y Seguridad</h3>
            <p>Revisión completa del sistema de frenos: pastillas, discos, líquido y ABS. Tu seguridad es nuestra prioridad.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-bolt"></i></div>
            <h3 class="service-title">Sistema Eléctrico</h3>
            <p>Revisión de batería, alternador, luces y sistema de arranque. Evita quedarte varado por una falla eléctrica.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-snowflake"></i></div>
            <h3 class="service-title">Aire Acondicionado</h3>
            <p>Recarga de gas, revisión de compresor y climatización. Mantén el confort en tu vehículo en cualquier temporada.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-microchip"></i></div>
            <h3 class="service-title">Scanner Diagnóstico</h3>
            <p>Diagnóstico computarizado completo para detectar fallas antes de que se conviertan en problemas mayores.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-md-6">
        <div class="card service-card">
          <div class="card-body text-center p-4">
            <div class="service-icon"><i class="fas fa-car"></i></div>
            <h3 class="service-title">Preparación Revisión Técnica</h3>
            <p>Revisamos todos los puntos críticos para que tu vehículo apruebe la revisión técnica sin rechazos.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================================= -->
<!-- MARCAS -->
<!-- ======================================================================= -->
<section class="py-5" style="background: #fff;" id="marcas">
  <div class="container text-center mb-4">
    <h2 class="text-uppercase fw-bold" style="color: #a80000; font-size: 1.8rem;">Trabajamos con las Mejores Marcas</h2>
    <p class="text-muted">Repuestos y accesorios de marcas reconocidas a nivel mundial</p>
  </div>
  <div class="container">
    <div class="swiper logo-swiper">
      <div class="swiper-wrapper">
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33795.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33793.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33792.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33791.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33790.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-39.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-36.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-35.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-33789.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
        <div class="swiper-slide"><img src="../images/imagen/wp-content/uploads/2024/10/Group-44.svg" alt="Marca automotriz" class="img-fluid" style="max-height: 70px; filter: grayscale(100%); opacity: 0.7;"></div>
      </div>
    </div>
  </div>
</section>

<!-- LISTADO DE MARCAS -->
<div class="py-4" style="background:#f9fafb;">
  <div class="container text-center">
    <p class="fw-bold text-uppercase" style="color:#a80000; font-size:1.1rem; margin-bottom:15px;">Trabajamos con todas las marcas</p>
    <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:10px 20px; font-size:0.9rem; color:#555;">
      <span>Toyota</span><span>Hyundai</span><span>Kia</span><span>Chevrolet</span><span>Nissan</span>
      <span>Renault</span><span>Peugeot</span><span>Ford</span><span>Volkswagen</span><span>Honda</span>
      <span>Mazda</span><span>Mitsubishi</span><span>Suzuki</span><span>Subaru</span><span>Fiat</span>
      <span>MG</span><span>Chery</span><span>Geely</span><span>BYD</span><span>JAC</span>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- CONTACTO -->
<!-- ======================================================================= -->
<section class="py-5" style="background: linear-gradient(135deg, #a80000 0%, #d32f2f 100%); color: white;" id="contacto">
  <div class="container text-center">
    <h2 class="text-uppercase fw-bold mb-3" style="font-size: 2.5rem;">¿Necesitas un Mecánico a Domicilio en {html.escape(comuna_display)}?</h2>
    <p class="lead mb-4" style="max-width: 700px; margin: 0 auto;">No esperes más. Contáctanos ahora por WhatsApp y agenda tu cita en {html.escape(comuna_display)}. Atención 24/7, emergencias incluidas.</p>
    <div class="d-flex flex-wrap justify-content-center gap-3">
      <a href="https://wa.me/{PHONE_CLEAN}?text={wa_text}" target="_blank" class="btn btn-lg fw-bold text-dark" style="background: #25D366; border: none; border-radius: 50px; padding: 15px 40px; font-size: 1.2rem;">
        <i class="fab fa-whatsapp me-2"></i> WhatsApp: {PHONE}
      </a>
      <a href="tel:{PHONE_CLEAN}" class="btn btn-lg fw-bold text-white" style="background: rgba(255,255,255,0.2); border: 2px solid white; border-radius: 50px; padding: 15px 40px; font-size: 1.2rem;">
        <i class="fas fa-phone-alt me-2"></i> Llamar Ahora
      </a>
    </div>
    <p class="mt-4 mb-0" style="opacity: 0.9;">
      <i class="fas fa-map-marker-alt me-1"></i> Servicio a domicilio en {html.escape(comuna_display)} y toda la Región Metropolitana
      &nbsp;|&nbsp; <i class="fas fa-clock me-1"></i> Disponibles 24/7
      &nbsp;|&nbsp; <i class="fas fa-star me-1"></i> 4.9/5 en Google
    </p>
  </div>
</section>

<!-- ======================================================================= -->
<!-- FOOTER -->
<!-- ======================================================================= -->
<footer class="main-footer">
  <div class="container">
    <div class="row">
      <div class="col-lg-4 col-md-6 mb-4">
        <div class="footer-logo-box"><i class="fas fa-wrench"></i></div>
        <h5 class="footer-title">GlobalPro</h5>
        <p class="text-justify">
          Somos líderes en <strong>Mecánico a Domicilio</strong> en Santiago. Ofrecemos servicio automotriz integral con tecnología de punta y profesionales certificados. Tu vehículo en las mejores manos, donde tú estés.
        </p>
        <div class="social-icons mt-3">
          <a href="#"><i class="fab fa-facebook-f"></i></a>
          <a href="#"><i class="fab fa-instagram"></i></a>
          <a href="#"><i class="fab fa-whatsapp"></i></a>
        </div>
      </div>
      <div class="col-lg-4 col-md-6 mb-4">
        <h5 class="footer-title">Enlaces Rápidos</h5>
        <div class="footer-links">
          <ul>
            <li><a href="../index.html">Inicio</a></li>
            <li><a href="#mecanico-domicilio-seo">Mecánico a Domicilio</a></li>
            <li><a href="#servicios">Nuestros Servicios</a></li>
            <li><a href="#faq">Preguntas Frecuentes</a></li>
            <li><a href="../blog/index.html">Blog</a></li>
            <li><a href="../contacto.html">Contacto</a></li>
          </ul>
        </div>
      </div>
      <div class="col-lg-4 col-md-12 mb-4">
        <h5 class="footer-title">Información de Contacto</h5>
        <div class="contact-info-item">
          <i class="fas fa-map-marker-alt"></i>
          <div>
            <strong>Ubicación:</strong><br>
            Servicio a Domicilio en todo Santiago<br>
            Base: Pedro Aguirre Cerda, RM
          </div>
        </div>
        <div class="contact-info-item">
          <i class="fas fa-phone-alt"></i>
          <div>
            <strong>Teléfono:</strong><br>
            <a href="tel:{PHONE_CLEAN}" style="color:#bbb; text-decoration:none;">{PHONE}</a>
          </div>
        </div>
        <div class="contact-info-item">
          <i class="fas fa-envelope"></i>
          <div>
            <strong>Email:</strong><br>
            <a href="mailto:{EMAIL}" style="color:#bbb; text-decoration:none;">{EMAIL}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="copyright-bar">
    <div class="container">
      <div class="row">
        <div class="col-md-6 text-center text-md-start">
          &copy; 2024 GlobalPro. Todos los derechos reservados.
        </div>
        <div class="col-md-6 text-center text-md-end">
          Especialistas en <strong>Mecánico a Domicilio</strong> | Servicio Automotriz Integral
        </div>
      </div>
    </div>
  </div>
</footer>

<!-- ======================================================================= -->
<!-- MODAL CHAT IA -->
<!-- ======================================================================= -->
<div id="modal-chat-ia" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.7); z-index:10000; align-items:center; justify-content:center; padding:20px;">
  <div style="background:#fff; border-radius:16px; max-width:480px; width:100%; padding:30px; position:relative; animation: modalSlideIn 0.3s ease-out;">
    <button onclick="document.getElementById('modal-chat-ia').style.display='none'" style="position:absolute; top:12px; right:16px; background:none; border:none; font-size:1.5rem; cursor:pointer; color:#999;">&times;</button>
    <div style="text-align:center; margin-bottom:20px;">
      <div style="width:70px; height:70px; background:linear-gradient(135deg,#FFC107,#FF9800); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 12px; box-shadow:0 4px 15px rgba(255,152,0,0.4);">
        <i class="fas fa-robot" style="font-size:2rem; color:#fff;"></i>
      </div>
      <h3 style="color:#a80000; font-weight:700; margin-bottom:6px;">Consulta tu Vehículo</h3>
      <p style="color:#666; font-size:0.9rem;">Ingresa tu patente y revisa el historial completo de trabajos, notas del técnico, fechas y más.</p>
    </div>
    <form id="form-patente-ia" onsubmit="buscarPatenteIA(event)" style="display:flex; gap:10px;">
      <input type="text" id="input-patente-ia" placeholder="Ej: ABCD12" required maxlength="10" style="flex:1; padding:14px 18px; border:2px solid #e5e7eb; border-radius:12px; font-size:1.1rem; text-transform:uppercase; outline:none; font-family:inherit;" onfocus="this.style.borderColor='#a80000'" onblur="this.style.borderColor='#e5e7eb'">
      <button type="submit" style="padding:14px 24px; background:#a80000; color:#fff; border:none; border-radius:12px; font-weight:700; cursor:pointer; font-size:1rem; white-space:nowrap; transition:background 0.2s;" onmouseover="this.style.background='#8b0000'" onmouseout="this.style.background='#a80000'">BUSCAR</button>
    </form>
    <div id="resultado-patente-ia" style="margin-top:16px; display:none;"></div>
    <div style="text-align:center; margin-top:16px;">
      <a href="https://llm-chat-app-template.estilosgrado33.workers.dev" target="_blank" style="color:#a80000; text-decoration:none; font-size:0.85rem; font-weight:600;">
        <i class="fas fa-comments"></i> Abrir chat completo con IA
      </a>
    </div>
  </div>
</div>

<!-- ======================================================================= -->
<!-- STICKY BOTTOM BAR -->
<!-- ======================================================================= -->
<div class="sticky-bottom-bar">
  <div class="big-buttons-container">
    <a href="tel:{PHONE_CLEAN}" class="btn-massive-call">
      <i class="fas fa-phone-alt"></i> LLAMAR
    </a>
    <a href="https://wa.me/{PHONE_CLEAN}?text={wa_text}" class="btn-massive-wa" target="_blank">
      <i class="fab fa-whatsapp"></i> WHATSAPP
    </a>
    <a href="#" class="btn-small-chat" title="Consulta tu vehículo por patente" onclick="document.getElementById('modal-chat-ia').style.display='flex'; return false;">
      <i class="fas fa-robot"></i>
    </a>
  </div>
</div>

<!-- ======================================================================= -->
<!-- SCRIPTS -->
<!-- ======================================================================= -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/ScrollTrigger.min.js"></script>

<script>
// Swiper initialization
var swiper = new Swiper(".logo-swiper", {{
  slidesPerView: 5,
  spaceBetween: 30,
  loop: true,
  autoplay: {{ delay: 2000, disableOnInteraction: false }},
  breakpoints: {{
    0: {{ slidesPerView: 2, spaceBetween: 15 }},
    576: {{ slidesPerView: 3, spaceBetween: 20 }},
    992: {{ slidesPerView: 5, spaceBetween: 30 }}
  }}
}});

// GSAP animations
gsap.registerPlugin(ScrollTrigger);
gsap.from(".service-card", {{
  scrollTrigger: {{ trigger: ".services-section", start: "top 80%" }},
  opacity: 0, y: 50, duration: 0.6, stagger: 0.15
}});
gsap.from(".section-title", {{
  scrollTrigger: {{ trigger: ".services-section", start: "top 85%" }},
  opacity: 0, y: 30, duration: 0.8
}});
</script>

<script>
// Modal Chat IA
function buscarPatenteIA(e) {{
  e.preventDefault();
  var pat = document.getElementById('input-patente-ia').value.trim().toUpperCase();
  if (!pat) return;
  var res = document.getElementById('resultado-patente-ia');
  res.style.display = 'block';
  res.innerHTML = '<div style="text-align:center; padding:20px; color:#999;"><i class="fas fa-spinner fa-spin"></i> Buscando...</div>';
  fetch('https://llm-chat-app-template.estilosgrado33.workers.dev/api/consultar', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ patente: pat }})
  }})
  .then(function(r) {{ return r.json(); }})
  .then(function(data) {{
    if (data.success && data.vehiculo) {{
      var v = data.vehiculo;
      var html = '<div style="background:#f0f7ff; border-radius:8px; padding:10px; margin-bottom:10px; border-left:3px solid #2563eb;">';
      html += '<strong style="color:#1e3a8a;">' + v.marca + ' ' + v.modelo + ' (' + (v.anio||'N/A') + ')</strong>';
      html += '<div style="font-size:0.83rem; color:#1e40af;">Patente: ' + v.patente_placa + ' | Propietario: ' + (v.cliente?.nombre || 'N/A') + '</div>';
      html += '<div style="font-size:0.83rem; color:#1e40af;">' + v.total_ordenes + ' orden(es) encontrada(s)</div></div>';
      for (var i = 0; i < v.ordenes.length; i++) {{
        var o = v.ordenes[i];
        var estadoClass = (o.estado==='Cerrada'||o.estado_trabajo==='Cerrada') ? 'badge-ok' : 'badge-pend';
        var num = String(o.numero_orden||0).padStart(6,'0');
        html += '<div class="ot-card">';
        html += '<div class="ot-num">OT #' + num + ' <span class="ot-estado ' + estadoClass + '">' + (o.estado_trabajo||o.estado||'N/A') + '</span></div>';
        html += '<div class="dato">Ingreso: ' + (o.fecha_ingreso||'N/A') + '</div>';
        if (o.fecha_completado) html += '<div class="dato">Cierre: ' + o.fecha_completado + '</div>';
        html += '</div>';
      }}
      res.innerHTML = html;
    }} else {{
      res.innerHTML = '<div style="text-align:center; padding:20px; color:#999;">No se encontró información para la patente ' + pat + '</div>';
    }}
  }})
  .catch(function() {{
    res.innerHTML = '<div style="text-align:center; padding:20px; color:#d32f2f;">Error al consultar. Intenta nuevamente.</div>';
  }});
}}

// Close modal on outside click
document.getElementById('modal-chat-ia').addEventListener('click', function(e) {{
  if (e.target === this) this.style.display = 'none';
}});
</script>

</body>
</html>'''

    return page


# ============================================================
# MAIN
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated = []
    for comuna_key in comunas:
        comuna_display = display_names[comuna_key]
        slug = slugify(comuna_key)
        filepath = os.path.join(OUTPUT_DIR, f"{slug}.html")

        page_html = generate_page(comuna_key, comuna_display, slug)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_html)

        generated.append(filepath)
        print(f"  ✓ {comuna_display} → comunas/{slug}.html")

    print(f"\n{'='*60}")
    print(f"Total: {len(generated)} archivos generados exitosamente.")
    print(f"Directorio: {OUTPUT_DIR}")
    print(f"{'='*60}")

    # Show a few examples
    print("\nEjemplos:")
    for g in generated[:5]:
        print(f"  - {g}")
    print("  ...")
    for g in generated[-3:]:
        print(f"  - {g}")


if __name__ == "__main__":
    main()
