#!/usr/bin/env python3
"""
Reemplaza el widget de Elfsight Google Reviews con reseñas estáticas HTML
en todas las páginas del sitio mecanico247.com / globalpro.

Las reseñas son reales, extraídas de Google Maps.
Esto elimina la dependencia de Elfsight (límite de 200 visitas/mes).
"""

import os
import re
import glob

GOOGLE_MAPS_URL = "https://www.google.com/maps/place/Mec%C3%A1nico+A+Domicilio+24%2F7+%F0%9F%94%A7+%7C+Global+Pro+Automotriz/@-33.4985,-70.6355,15z/data=!4m8!3m7!1s0x9662c4e7e72e6b63:0xa5a8efc1e2c5a23e!8m2!3d-33.4985!4d-70.6355!9m1!1b1!16s%2Fg%2F11t5bkm9kj5"
WRITE_REVIEW_URL = "https://search.google.com/local/writereview?placeid=ChIJ8-Ss6LLFYpYRnFkh8v_5XEQ"

# Top 20 reseñas con texto significativo (nombre, tiempo, comentario)
REVIEWS_ES = [
    {
        "name": "Eduardo Muñoz",
        "time": "Hace 1 día",
        "stars": 5,
        "text": "Tenía un problema en mi auto, tenía un defecto en el cinturón del piloto este no enganchaba, cambiaron este y quedó todo ok. Gracias por su servicio."
    },
    {
        "name": "Luc",
        "time": "Hace 3 días",
        "stars": 5,
        "text": "Muy buena experiencia, excelente trabajo, puntual con la entrega, buena comunicación y responsable en sus trabajos realizados. Lo recomiendo al 100%."
    },
    {
        "name": "Alberto Ossandon",
        "time": "Hace 5 días",
        "stars": 5,
        "text": "Muy buen servicio Global Pro. José fue muy amable y se nota que sabe lo que hace. Revisó el auto con scanner, explicó claramente los problemas y fue transparente con el diagnóstico. Totalmente recomendado."
    },
    {
        "name": "Claudio Quezada",
        "time": "Hace 5 días",
        "stars": 5,
        "text": "Excelente atención. Se acomodaron a mi horario para atenderme. Gregorio muy buen profesional, solucionó el problema del auto con una orientación muy educativa."
    },
    {
        "name": "Marcelo Fuentes",
        "time": "Hace 6 días",
        "stars": 5,
        "text": "Se agradece por la preparación del aire acondicionado de mi auto. Buena atención, rápido y buenos precios."
    },
    {
        "name": "Leslie More",
        "time": "Hace 1 semana",
        "stars": 5,
        "text": "Merecidas sus 5 estrellas. Después de contactar otros servicios que me dejaron esperando horas, contacté con ellos y arreglaron mi auto de manera profesional y rápida."
    },
    {
        "name": "Mariela Muñoz",
        "time": "Hace 1 semana",
        "stars": 5,
        "text": "Muy buen servicio, profesional y sobre todo con una muy buena disposición. Nos atendió un domingo pm."
    },
    {
        "name": "Emilio Ravena",
        "time": "Hace 1 semana",
        "stars": 5,
        "text": "100% recomendados ante una emergencia. Honestos, te explican la falla y reparan en el instante cuando se puede. Muy buen trabajo."
    },
    {
        "name": "Diana Liz Avendaño Rojas",
        "time": "Hace 1 semana",
        "stars": 5,
        "text": "Muchas gracias por el servicio. Me sacaron de apuros. Recomendado."
    },
    {
        "name": "Cristopher Cayazzo",
        "time": "Hace 1 semana",
        "stars": 5,
        "text": "Se encargó de dar solución al problema del vehículo, fue amable y tuvo paciencia."
    },
    {
        "name": "MATÍAS PEROT ORTÚZAR",
        "time": "Hace 2 semanas",
        "stars": 5,
        "text": "Excelente servicio, claro y eficiente, totalmente recomendado."
    },
    {
        "name": "Reinaldo Silva",
        "time": "Hace 2 semanas",
        "stars": 5,
        "text": "Rápido, directo a la solución del problema. 100% recomendado."
    },
    {
        "name": "Sebastián Pereira",
        "time": "Hace 3 semanas",
        "stars": 5,
        "text": "Excelente equipo! Resuelven y bien medidos y justos en sus valores."
    },
    {
        "name": "Christian Andrés Ríos Cáceres",
        "time": "Hace 2 meses",
        "stars": 5,
        "text": "Excelente atención, supieron el problema y cómo repararlo de un día para otro. Muy honestos y profesionales. Recomendados."
    },
    {
        "name": "Iván Rivera",
        "time": "Hace 2 meses",
        "stars": 5,
        "text": "Los contacté un domingo bien tarde, el lunes a las 08:00 ya estaban en mi domicilio y a las 15:00 mi auto estaba funcionando perfecto. Excelente servicio."
    },
    {
        "name": "Juan Ignacio Errázuriz",
        "time": "Hace 2 meses",
        "stars": 5,
        "text": "Tuve un problema con la chapa de una puerta del auto durante un fin de semana y vinieron el domingo en la mañana y solucionaron el problema impecablemente. Todo por un precio súper razonable."
    },
    {
        "name": "Catalina Gotan",
        "time": "Hace 2 meses",
        "stars": 5,
        "text": "Llegó muy rápido y logró detectar la falla de mi auto. Recomendado."
    },
    {
        "name": "Macarena Gonzalez",
        "time": "Hace 2 meses",
        "stars": 5,
        "text": "Me gustó mucho la atención, llegó súper puntual y me pudieron arreglar el problema que tenía en el auto. Lo recomiendo 100%."
    },
    {
        "name": "Andrés Arenas",
        "time": "Hace 3 meses",
        "stars": 5,
        "text": "Fui al taller por un problema del aire acondicionado y el mecánico encontró de inmediato la falla. Le hizo la mantención correspondiente y dejó todo en perfecto estado. Muy recomendado."
    },
    {
        "name": "Rolando Ayora",
        "time": "Hace 4 meses",
        "stars": 5,
        "text": "Excelente servicio a domicilio. Los técnicos vinieron a instalar el compresor del aire acondicionado de mi camioneta, van muy bien equipados y el trabajo quedó impecable."
    },
]

REVIEWS_EN = [
    {
        "name": "Eduardo Muñoz",
        "time": "1 day ago",
        "stars": 5,
        "text": "I had a problem with my car, the driver's seatbelt wouldn't latch. They replaced it and everything works perfectly. Thank you for your service."
    },
    {
        "name": "Luc",
        "time": "3 days ago",
        "stars": 5,
        "text": "Great experience, excellent work, punctual delivery, good communication and responsible. I recommend 100%."
    },
    {
        "name": "Alberto Ossandon",
        "time": "5 days ago",
        "stars": 5,
        "text": "Very good service from Global Pro. José was very friendly and clearly knows what he's doing. Scanned the car, clearly explained the issues, and was transparent with the diagnosis. Highly recommended."
    },
    {
        "name": "Claudio Quezada",
        "time": "5 days ago",
        "stars": 5,
        "text": "Excellent attention. They accommodated my schedule. Gregorio is a great professional, solved the car problem with very educational guidance."
    },
    {
        "name": "Marcelo Fuentes",
        "time": "6 days ago",
        "stars": 5,
        "text": "Thank you for preparing the air conditioning in my car. Good attention, fast and good prices."
    },
    {
        "name": "Emilio Ravena",
        "time": "1 week ago",
        "stars": 5,
        "text": "100% recommended for emergencies. Honest, they explain the fault and repair it on the spot when possible. Very good work."
    },
    {
        "name": "Iván Rivera",
        "time": "2 months ago",
        "stars": 5,
        "text": "I contacted them on a Sunday evening, by Monday 08:00 they were at my home and by 15:00 my car was running perfectly. Excellent service."
    },
    {
        "name": "Christian Andrés Ríos",
        "time": "2 months ago",
        "stars": 5,
        "text": "Excellent attention, they identified the problem and how to fix it from one day to the next. Very honest and professional. Recommended."
    },
    {
        "name": "Juan Ignacio Errázuriz",
        "time": "2 months ago",
        "stars": 5,
        "text": "Had a problem with my car door latch on a weekend. They came Sunday morning and fixed it perfectly. Very reasonable price."
    },
    {
        "name": "Catalina Gotan",
        "time": "2 months ago",
        "stars": 5,
        "text": "Arrived very quickly and managed to detect the fault in my car. Recommended."
    },
]


def generate_stars_html(stars):
    """Genera el HTML de estrellas."""
    return '<span style="color:#FBBC05; font-size:0.85rem; letter-spacing:1px;">' + '<i class="fas fa-star"></i>' * stars + '</span>'


def generate_review_card(review, index):
    """Genera una tarjeta de reseña individual."""
    stars_html = generate_stars_html(review["stars"])
    initial = review["name"][0].upper() if review["name"] else "?"
    # Color basado en el índice para variedad
    colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#a80000", "#FF6D00", "#7B1FA2", "#00897B"]
    color = colors[index % len(colors)]
    return f'''    <div class="google-review-card">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
        <div style="width:40px; height:40px; border-radius:50%; background:{color}; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:1rem; flex-shrink:0;">{initial}</div>
        <div style="text-align:left;">
          <div style="font-weight:700; font-size:0.9rem; color:#202124;">{review["name"]}</div>
          <div style="font-size:0.75rem; color:#70757a;">{review["time"]}</div>
        </div>
        <i class="fab fa-google" style="margin-left:auto; color:#4285F4; font-size:1rem; opacity:0.6;"></i>
      </div>
      {stars_html}
      <p style="margin:8px 0 0; font-size:0.85rem; color:#333; line-height:1.6; text-align:left; font-style:italic;">"{review["text"]}"</p>
    </div>'''


REVIEW_CSS = """
  <style>
    .reviews-carousel {
      position: relative;
      overflow: hidden;
      margin: 0 -10px;
    }
    .reviews-track {
      display: flex;
      gap: 16px;
      overflow-x: auto;
      scroll-behavior: smooth;
      padding: 10px 45px;
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    .reviews-track::-webkit-scrollbar { display: none; }
    .google-review-card {
      min-width: 300px;
      max-width: 340px;
      flex-shrink: 0;
      background: #fff;
      border: 1px solid #e8eaed;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      transition: transform 0.3s, box-shadow 0.3s;
    }
    .google-review-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .reviews-arrow {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 1px solid #dadce0;
      background: #fff;
      color: #5f6368;
      font-size: 0.85rem;
      cursor: pointer;
      z-index: 5;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      transition: all 0.2s;
    }
    .reviews-arrow:hover { background:#f1f3f4; border-color:#a80000; color:#a80000; }
    .reviews-arrow-left { left: 4px; }
    .reviews-arrow-right { right: 4px; }
    @media (max-width: 768px) {
      .google-review-card { min-width: 260px; max-width: 280px; padding: 16px; }
      .reviews-track { padding: 10px 40px; }
    }
  </style>
"""

REVIEW_JS = """
  <script>
    function scrollReviews(dir) {
      var track = document.getElementById('reviewsTrack');
      if (track) { track.scrollBy({ left: dir * 320, behavior: 'smooth' }); }
    }
  </script>"""


def generate_reviews_html(reviews, is_en=False):
    """Genera el bloque HTML completo de reseñas."""
    cards = "\n".join(generate_review_card(r, i) for i, r in enumerate(reviews))

    if is_en:
        badge_sub = "Based on 155+ Google reviews"
        btn_maps = "View on Google Maps"
        btn_review = "Write a Review"
        arrow_prev = "Previous"
        arrow_next = "Next"
    else:
        badge_sub = "Basado en 155+ reseñas de Google"
        btn_maps = "Ver en Google Maps"
        btn_review = "Dejar una Reseña"
        arrow_prev = "Anterior"
        arrow_next = "Siguiente"

    html = '<div style="margin-top:25px;">'
    # Badge de rating
    html += '''
    <!-- Badge de rating -->
    <div style="display:inline-flex; align-items:center; gap:12px; background:#fff; border:2px solid #e8eaed; border-radius:16px; padding:14px 24px; margin-bottom:25px; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
      <span style="font-size:2.2rem; font-weight:900; color:#202124;">4.9</span>
      <div>
        <div style="color:#FBBC05; font-size:1.1rem;"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
        <div style="font-size:0.8rem; color:#70757a; font-weight:600;">''' + badge_sub + '''</div>
      </div>
      <i class="fab fa-google" style="font-size:1.5rem; color:#4285F4;"></i>
    </div>'''

    # Carrusel de reseñas
    html += '''
    <!-- Carrusel de reseñas Google Maps -->
    <div class="reviews-carousel" id="reviewsCarousel">
      <button class="reviews-arrow reviews-arrow-left" onclick="scrollReviews(-1)" aria-label="''' + arrow_prev + '''"><i class="fas fa-chevron-left"></i></button>
      <div class="reviews-track" id="reviewsTrack">
''' + cards + '''
      </div>
      <button class="reviews-arrow reviews-arrow-right" onclick="scrollReviews(1)" aria-label="''' + arrow_next + '''"><i class="fas fa-chevron-right"></i></button>
    </div>'''

    # Botones CTA
    html += '''
    <!-- Botones CTA -->
    <div style="margin-top:25px; display:flex; flex-wrap:wrap; justify-content:center; gap:12px;">
      <a href="''' + GOOGLE_MAPS_URL + '''" target="_blank" rel="noopener" style="display:inline-flex; align-items:center; gap:8px; background:#4285F4; color:#fff; padding:12px 28px; border-radius:50px; text-decoration:none; font-weight:700; font-size:0.95rem; box-shadow:0 4px 15px rgba(66,133,244,0.3); transition:all 0.3s;">
        <i class="fab fa-google"></i> ''' + btn_maps + '''
      </a>
      <a href="''' + WRITE_REVIEW_URL + '''" target="_blank" rel="noopener" style="display:inline-flex; align-items:center; gap:8px; background:#fff; color:#a80000; padding:12px 28px; border-radius:50px; text-decoration:none; font-weight:700; font-size:0.95rem; border:2px solid #a80000; transition:all 0.3s;">
        <i class="fas fa-star"></i> ''' + btn_review + '''
      </a>
    </div>
  </div>'''

    html += REVIEW_CSS
    html += REVIEW_JS

    return html


def process_file(filepath, is_en=False):
    """Procesa un archivo HTML y reemplaza el widget Elfsight."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Reviews to use
    reviews = REVIEWS_EN if is_en else REVIEWS_ES
    reviews_html = generate_reviews_html(reviews, is_en)

    # Pattern 1: Replace the Elfsight div (with optional wrapper styles)
    # Matches: <div ... class="elfsight-app-4cbd3727..." ...></div>
    elfsight_pattern = r'<div[^>]*class="[^"]*elfsight-app-4cbd3727-4380-44b3-9cd7-2525ccb8f5d8[^"]*"[^>]*data-elfsight-app-lazy[^>]*>\s*</div>'

    if re.search(elfsight_pattern, content):
        content = re.sub(elfsight_pattern, reviews_html, content)
        print(f"  [OK] Reemplazado widget Elfsight en {filepath}")
    else:
        print(f"  [SKIP] No se encontró widget Elfsight en {filepath}")
        return

    # Remove Elfsight platform script if present
    content = re.sub(
        r'\s*<script src="https://elfsightcdn\.com/platform\.js"\s*defer>\s*</script>',
        '', content
    )

    # Remove Elfsight CSS if present (the .elfsight-app rule)
    content = re.sub(
        r'\s*\.elfsight-app-4cbd3727-4380-44b3-9cd7-2525ccb8f5d8\s*\{[^}]*\}',
        '', content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Find all HTML files containing the Elfsight widget
    all_html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Skip images, node_modules, .git directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'images']]
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                all_html_files.append(filepath)

    print(f"Total archivos HTML encontrados: {len(all_html_files)}")

    # Filter files that actually contain the Elfsight widget
    elfsight_files = []
    for fp in all_html_files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'elfsight-app-4cbd3727' in content:
                is_en = '/en/' in fp
                elfsight_files.append((fp, is_en))

    print(f"Archivos con widget Elfsight: {len(elfsight_files)}")
    print()

    es_count = 0
    en_count = 0

    for filepath, is_en in elfsight_files:
        rel = os.path.relpath(filepath, base_dir)
        process_file(filepath, is_en=is_en)
        if is_en:
            en_count += 1
        else:
            es_count += 1

    print()
    print(f"=== RESUMEN ===")
    print(f"Archivos ES modificados: {es_count}")
    print(f"Archivos EN modificados: {en_count}")
    print(f"Total modificados: {es_count + en_count}")
    print()
    print("Widget Elfsight eliminado. Reseñas estáticas de Google Maps instaladas.")
    print("Sin dependencia de terceros. Sin límite de visitas.")


if __name__ == '__main__':
    main()
