#!/usr/bin/env python3
"""
Script para actualizar todas las paginas de vehiculos con:
1. 4 tarjetas de servicios destacados (Cambio de Aceite, Frenos, Electricidad, Scanner) personalizadas por vehiculo
2. Seccion de Vehiculos con modal lightbox (fotos miniatura que se abren en grande)

Estructura de cada pagina de vehiculo:
  - Hero
  - Info del vehiculo
  - Descripcion de servicios
  - Lista de servicios (8 items)
  - CTA (red gradient)
  - SEO Vitaminized Content (10 blocks)
  - "Otros Vehiculos que Atendemos" (text links)
  - "Listado de Marcas" div
  - Footer
  - Sticky bottom bar

Insercion: Ambas secciones se insertan ANTES del footer (despues del listado de marcas).
"""

import os
import re
import glob

VEHICULOS_DIR = "/home/z/my-project/Globalpro/vehiculos"

# Vehicle data - same as update_comunas.py
VEHICLES = [
    {"name": "Renault Logan", "thumb": "Renault-logan-300x225.png", "full": "Renault-logan.png", "alt": "Renault Logan"},
    {"name": "Hyundai Grand i10", "thumb": "hyundai-grandi10-300x137.png", "full": "hyundai-grandi10.png", "alt": "Hyundai Grand i10"},
    {"name": "Honda City", "thumb": "honda-city-300x225.png", "full": "honda-city.png", "alt": "Honda City"},
    {"name": "Chevrolet Sonic", "thumb": "chevrolet-sonic-300x198.png", "full": "chevrolet-sonic-1024x676.png", "alt": "Chevrolet Sonic"},
    {"name": "Ford Fiesta", "thumb": "ford-fiesta-300x199.png", "full": "ford-fiesta-1024x680.png", "alt": "Ford Fiesta"},
    {"name": "Suzuki Celerio", "thumb": "suzuki-celerio-300x225.png", "full": "suzuki-celerio.png", "alt": "Suzuki Celerio"},
    {"name": "Subaru XV", "thumb": "subaru-xv-300x225.png", "full": "subaru-xv.png", "alt": "Subaru XV"},
    {"name": "Subaru Forester", "thumb": "subaru-forester-300x172.png", "full": "subaru-forester-1024x587.png", "alt": "Subaru Forester"},
    {"name": "Renault Duster", "thumb": "renault-duster-300x158.png", "full": "renault-duster.png", "alt": "Renault Duster"},
    {"name": "Honda CR-V", "thumb": "honda-crv-300x225.png", "full": "honda-crv.png", "alt": "Honda CR-V"},
    {"name": "Honda Civic", "thumb": "honda-civic-300x300.png", "full": "honda-civic.png", "alt": "Honda Civic"},
    {"name": "Mazda CX-5", "thumb": "mazda-cx-5-300x199.png", "full": "mazda-cx-5-1024x680.png", "alt": "Mazda CX-5"},
    {"name": "Mazda 3", "thumb": "mazda-3-300x158.png", "full": "mazda-3.png", "alt": "Mazda 3"},
    {"name": "Volkswagen Gol", "thumb": "volkswagen-gol-300x177.png", "full": "volkswagen-gol.png", "alt": "Volkswagen Gol"},
    {"name": "Ford EcoSport", "thumb": "ford-ecosport-300x184.png", "full": "ford-ecosport.png", "alt": "Ford EcoSport"},
    {"name": "MG 3", "thumb": "mg-3-300x216.png", "full": "mg-3.png", "alt": "MG 3"},
    {"name": "MG ZS", "thumb": "mg-zs-300x106.png", "full": "mg-zs-1024x363.png", "alt": "MG ZS"},
    {"name": "Suzuki Baleno", "thumb": "suzuki-baleno-300x196.png", "full": "suzuki-baleno.png", "alt": "Suzuki Baleno"},
    {"name": "Hyundai Tucson", "thumb": "hyundai-tucson-300x184.png", "full": "hyundai-tucson.png", "alt": "Hyundai Tucson"},
    {"name": "Hyundai Accent", "thumb": "hyundai-accent-300x199.png", "full": "hyundai-accent-1024x680.png", "alt": "Hyundai Accent"},
    {"name": "Peugeot 3008", "thumb": "peugeot-3008-300x199.png", "full": "peugeot-3008.png", "alt": "Peugeot 3008"},
    {"name": "Peugeot 208", "thumb": "peugeot-208-300x197.png", "full": "peugeot-208.png", "alt": "Peugeot 208"},
    {"name": "Nissan Kicks", "thumb": "nissan-kicks-300x147.png", "full": "nissan-kicks-1024x502.png", "alt": "Nissan Kicks"},
    {"name": "Nissan Versa", "thumb": "nissan-versa-300x200.png", "full": "nissan-versa.png", "alt": "Nissan Versa"},
    {"name": "Kia Rio", "thumb": "kia-rio-300x180.png", "full": "kia-rio.png", "alt": "Kia Rio"},
    {"name": "Toyota Corolla", "thumb": "toyota-corolla-300x225.png", "full": "toyota-corolla.png", "alt": "Toyota Corolla"},
    {"name": "Toyota Yaris", "thumb": "toyota-yaris-300x200.png", "full": "toyota-yaris-1024x683.png", "alt": "Toyota Yaris"},
    {"name": "Chevrolet Spark", "thumb": "chevrolet-spark-300x225.png", "full": "chevrolet-spark-1024x768.png", "alt": "Chevrolet Spark"},
    {"name": "Chevrolet Sail", "thumb": "chevrolet-sail.png", "full": "chevrolet-sail.png", "alt": "Chevrolet Sail"},
    {"name": "Kia Morning", "thumb": "33678-MORNING-300x225.jpg", "full": "33678-MORNING-1024x768.jpg", "alt": "Kia Morning"},
    {"name": "Fiat Bravo tjet", "thumb": "Fiat-Bravo-2016-300x173.jpg", "full": "Fiat-Bravo-2016-1024x591.jpg", "alt": "Fiat Bravo tjet"},
    {"name": "Suzuki Swift", "thumb": "pngegg-1-300x200.png", "full": "pngegg-1-1024x683.png", "alt": "Suzuki Swift"},
]


def get_vehicle_img_path(filename):
    """Determine the correct image path based on the filename."""
    if filename.startswith('Fiat') or filename.startswith('pngegg'):
        return f"../images/wp-content/uploads/2024/08/{filename}"
    elif filename.startswith('33678'):
        return f"../images/wp-content/uploads/2024/10/{filename}"
    else:
        return f"../images/wp-content/uploads/2024/10/{filename}"


def generate_featured_services_section(vehicle_name, vehicle_slug):
    """Generate the 4 featured service cards HTML for a vehicle page."""
    wa_base = "https://wa.me/56939026185"
    vehicle_name_encoded = vehicle_name.replace(' ', '%20')
    return f'''
<!-- ======================================================================= -->
<!-- SERVICIOS DESTACADOS - ACEITE, FRENOS, ELECTRICIDAD, SCANNER -->
<!-- ======================================================================= -->
<section class="py-5" id="servicios-destacados" style="background: linear-gradient(135deg, #1a1a2e 0%, #121212 100%); color: white;">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="fw-bold" style="font-size: 2.2rem; color: #FFC107;">
        <i class="fas fa-star me-2"></i>Servicios Mas Solicitados para {vehicle_name}
      </h2>
      <p style="color: #ccc; max-width: 700px; margin: 0 auto;">Los servicios que mas necesitan los propietarios de {vehicle_name}. Agenda rapido por WhatsApp.</p>
    </div>
    <div class="row g-4 justify-content-center">
      <div class="col-lg-3 col-md-6">
        <div class="p-4 rounded text-center h-100" style="background: rgba(255,255,255,0.07); border: 2px solid #FFC107; border-radius: 16px !important; transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-8px)';this.style.boxShadow='0 10px 30px rgba(255,193,7,0.3)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
          <div style="width:80px; height:80px; background:linear-gradient(135deg,#FFC107,#FF9800); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; box-shadow:0 4px 15px rgba(255,193,7,0.4);">
            <i class="fas fa-oil-can" style="font-size:2rem; color:#000;"></i>
          </div>
          <h3 style="font-weight:700; font-size:1.2rem; color:#FFC107; margin-bottom:10px;">Cambio de Aceite</h3>
          <p style="font-size:0.9rem; color:#ccc; line-height:1.7;">Aceites sinteticos y semi-sinteticos premium. Incluye filtro y revision de niveles para tu {vehicle_name}.</p>
          <a href="{wa_base}?text=Hola%20necesito%20un%20cambio%20de%20aceite%20para%20mi%20{vehicle_name_encoded}" class="btn btn-sm fw-bold mt-2" target="_blank" style="background:#FFC107; color:#000; border-radius:50px; padding:8px 20px;">
            <i class="fab fa-whatsapp me-1"></i> Cotizar
          </a>
        </div>
      </div>
      <div class="col-lg-3 col-md-6">
        <div class="p-4 rounded text-center h-100" style="background: rgba(255,255,255,0.07); border: 2px solid #D32F2F; border-radius: 16px !important; transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-8px)';this.style.boxShadow='0 10px 30px rgba(211,47,47,0.3)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
          <div style="width:80px; height:80px; background:linear-gradient(135deg,#D32F2F,#a80000); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; box-shadow:0 4px 15px rgba(211,47,47,0.4);">
            <i class="fas fa-compact-disc" style="font-size:2rem; color:#fff;"></i>
          </div>
          <h3 style="font-weight:700; font-size:1.2rem; color:#D32F2F; margin-bottom:10px;">Frenos</h3>
          <p style="font-size:0.9rem; color:#ccc; line-height:1.7;">Pastillas, discos, liquido y ABS. Medicion digital del espesor. Tu seguridad es primero en tu {vehicle_name}.</p>
          <a href="{wa_base}?text=Hola%20necesito%20reparacion%20de%20frenos%20para%20mi%20{vehicle_name_encoded}" class="btn btn-sm fw-bold mt-2" target="_blank" style="background:#D32F2F; color:#fff; border-radius:50px; padding:8px 20px;">
            <i class="fab fa-whatsapp me-1"></i> Cotizar
          </a>
        </div>
      </div>
      <div class="col-lg-3 col-md-6">
        <div class="p-4 rounded text-center h-100" style="background: rgba(255,255,255,0.07); border: 2px solid #2196F3; border-radius: 16px !important; transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-8px)';this.style.boxShadow='0 10px 30px rgba(33,150,243,0.3)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
          <div style="width:80px; height:80px; background:linear-gradient(135deg,#2196F3,#1565C0); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; box-shadow:0 4px 15px rgba(33,150,243,0.4);">
            <i class="fas fa-bolt" style="font-size:2rem; color:#fff;"></i>
          </div>
          <h3 style="font-weight:700; font-size:1.2rem; color:#2196F3; margin-bottom:10px;">Electricidad</h3>
          <p style="font-size:0.9rem; color:#ccc; line-height:1.7;">Diagnostico electrico completo. Bateria, alternador, motor de arranque y cableado para tu {vehicle_name}.</p>
          <a href="{wa_base}?text=Hola%20necesito%20electricidad%20automotriz%20para%20mi%20{vehicle_name_encoded}" class="btn btn-sm fw-bold mt-2" target="_blank" style="background:#2196F3; color:#fff; border-radius:50px; padding:8px 20px;">
            <i class="fab fa-whatsapp me-1"></i> Cotizar
          </a>
        </div>
      </div>
      <div class="col-lg-3 col-md-6">
        <div class="p-4 rounded text-center h-100" style="background: rgba(255,255,255,0.07); border: 2px solid #4CAF50; border-radius: 16px !important; transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-8px)';this.style.boxShadow='0 10px 30px rgba(76,175,80,0.3)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
          <div style="width:80px; height:80px; background:linear-gradient(135deg,#4CAF50,#2E7D32); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; box-shadow:0 4px 15px rgba(76,175,80,0.4);">
            <i class="fas fa-barcode" style="font-size:2rem; color:#fff;"></i>
          </div>
          <h3 style="font-weight:700; font-size:1.2rem; color:#4CAF50; margin-bottom:10px;">Escanner</h3>
          <p style="font-size:0.9rem; color:#ccc; line-height:1.7;">Diagnostico computarizado sin adivinanzas. Interpretacion de codigos y soluciones reales para tu {vehicle_name}.</p>
          <a href="{wa_base}?text=Hola%20necesito%20scanner%20automotriz%20para%20mi%20{vehicle_name_encoded}" class="btn btn-sm fw-bold mt-2" target="_blank" style="background:#4CAF50; color:#fff; border-radius:50px; padding:8px 20px;">
            <i class="fab fa-whatsapp me-1"></i> Cotizar
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
'''


def generate_vehicles_section(vehicle_name, vehicle_slug):
    """Generate the vehicles section with thumbnail grid and lightbox modal."""
    # Generate vehicle thumbnails - show first 9 visible, rest hidden
    vehicle_cards = []
    for i, v in enumerate(VEHICLES):
        display = 'none' if i >= 9 else 'block'
        img_path = get_vehicle_img_path(v['thumb'])
        vehicle_cards.append(f'''
        <div class="col-4 col-md-3 col-lg-2 veh-thumb-col" style="display:{display};">
          <div class="veh-thumb" onclick="openVehicleLightbox({i})">
            <img src="{img_path}" alt="{v['alt']} - Mecanico a Domicilio" loading="lazy">
            <p class="veh-thumb-name">{v['name']}</p>
          </div>
        </div>''')

    # Generate lightbox slides data
    slides_js = "[\n"
    for i, v in enumerate(VEHICLES):
        full_path = get_vehicle_img_path(v['full'])
        slides_js += f'    {{src: "{full_path}", title: "{v["name"]}"}},\n'
    slides_js += "  ]"

    return f'''
<!-- ======================================================================= -->
<!-- VEHICULOS QUE ATENDEMOS -->
<!-- ======================================================================= -->
<section class="py-5" id="vehiculos-comuna" style="background:#f8f9fa; border-top:3px solid var(--gp-blood-red);">
  <div class="container">
    <div class="text-center mb-4">
      <h2 class="fw-bold" style="color:#a80000; font-size:2rem;">
        <i class="fas fa-car me-2"></i>Vehiculos que Atendemos
      </h2>
      <p style="color:#666; max-width:600px; margin:0 auto;">Selecciona tu vehiculo para ver los servicios disponibles. Haz clic en la foto para ampliarla.</p>
    </div>
    <div class="row g-3 justify-content-center">
      {''.join(vehicle_cards)}
    </div>
    <div class="text-center mt-4" id="veh-load-more-container-{vehicle_slug}">
      <button class="btn btn-outline-primary fw-bold" onclick="loadMoreVehicles('{vehicle_slug}')">
        <i class="fas fa-plus-circle me-1"></i> Ver Mas Vehiculos
      </button>
    </div>
    <div class="text-center mt-4">
      <a href="https://wa.me/56939026185?text=Hola%20necesito%20servicio%20para%20mi%20{vehicle_name.replace(' ', '%20')}" class="btn btn-primary btn-lg fw-bold" target="_blank">
        <i class="fab fa-whatsapp me-2"></i> Cotizar para mi Vehiculo
      </a>
    </div>
  </div>
</section>

<!-- LIGHTBOX MODAL VEHICULOS -->
<div id="vehicleLightbox" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.92); z-index:10001; align-items:center; justify-content:center; padding:15px;" onclick="if(event.target===this)closeVehicleLightbox()">
  <button onclick="closeVehicleLightbox()" style="position:absolute; top:15px; right:20px; background:none; border:none; color:#fff; font-size:2.5rem; cursor:pointer; z-index:10002; line-height:1;">&times;</button>
  <button onclick="prevVehicle()" style="position:absolute; left:15px; top:50%; transform:translateY(-50%); background:rgba(168,0,0,0.8); border:none; color:#fff; font-size:2rem; cursor:pointer; width:50px; height:50px; border-radius:50%; z-index:10002;">&#10094;</button>
  <button onclick="nextVehicle()" style="position:absolute; right:15px; top:50%; transform:translateY(-50%); background:rgba(168,0,0,0.8); border:none; color:#fff; font-size:2rem; cursor:pointer; width:50px; height:50px; border-radius:50%; z-index:10002;">&#10095;</button>
  <div style="text-align:center; max-width:90vw; max-height:85vh;">
    <img id="lightboxImg" src="" alt="Vehiculo" style="max-width:90vw; max-height:75vh; object-fit:contain; border-radius:12px; box-shadow:0 10px 40px rgba(0,0,0,0.5);">
    <p id="lightboxTitle" style="color:#fff; font-size:1.3rem; font-weight:700; margin-top:15px;"></p>
  </div>
</div>

<style>
  .veh-thumb {{
    background:#fff; border-radius:12px; overflow:hidden; cursor:pointer;
    box-shadow:0 3px 10px rgba(0,0,0,0.08); transition:transform 0.3s, box-shadow 0.3s;
    text-align:center; padding:8px;
  }}
  .veh-thumb:hover {{
    transform:translateY(-5px); box-shadow:0 8px 25px rgba(0,0,0,0.15);
  }}
  .veh-thumb img {{
    width:100%; height:80px; object-fit:contain; border-radius:8px; background:#f8f9fa;
  }}
  .veh-thumb-name {{
    font-size:0.75rem; font-weight:600; color:#333; margin:5px 0 0 0; white-space:nowrap;
    overflow:hidden; text-overflow:ellipsis;
  }}
</style>

<script>
(function(){{
  var slides = {slides_js};
  window._vehSlides = slides;
  window._vehIdx = 0;
}})();

function openVehicleLightbox(idx){{
  window._vehIdx = idx;
  var lb = document.getElementById('vehicleLightbox');
  lb.style.display = 'flex';
  document.getElementById('lightboxImg').src = window._vehSlides[idx].src;
  document.getElementById('lightboxTitle').textContent = window._vehSlides[idx].title;
  document.body.style.overflow = 'hidden';
}}
function closeVehicleLightbox(){{
  document.getElementById('vehicleLightbox').style.display = 'none';
  document.body.style.overflow = '';
}}
function nextVehicle(){{
  window._vehIdx = (window._vehIdx + 1) % window._vehSlides.length;
  document.getElementById('lightboxImg').src = window._vehSlides[window._vehIdx].src;
  document.getElementById('lightboxTitle').textContent = window._vehSlides[window._vehIdx].title;
}}
function prevVehicle(){{
  window._vehIdx = (window._vehIdx - 1 + window._vehSlides.length) % window._vehSlides.length;
  document.getElementById('lightboxImg').src = window._vehSlides[window._vehIdx].src;
  document.getElementById('lightboxTitle').textContent = window._vehSlides[window._vehIdx].title;
}}
document.addEventListener('keydown', function(e){{
  if(document.getElementById('vehicleLightbox').style.display==='flex'){{
    if(e.key==='Escape') closeVehicleLightbox();
    if(e.key==='ArrowRight') nextVehicle();
    if(e.key==='ArrowLeft') prevVehicle();
  }}
}});

function loadMoreVehicles(slug){{
  var cols = document.querySelectorAll('.veh-thumb-col');
  var shown = 0;
  cols.forEach(function(c){{
    if(c.style.display==='none'){{ c.style.display='block'; shown++; }}
  }});
  var btn = document.getElementById('veh-load-more-container-' + slug);
  if(shown === 0 && btn) btn.style.display = 'none';
}}
</script>
'''


def extract_vehicle_name(content, filepath):
    """Extract the vehicle name from the H1 tag or title tag."""
    # Try H1 first (most reliable)
    h1_match = re.search(r'<h1[^>]*class="fw-bold[^"]*"[^>]*>\s*(.+?)\s*</h1>', content)
    if h1_match:
        name = h1_match.group(1).strip()
        # Clean up any HTML tags inside
        name = re.sub(r'<[^>]+>', '', name)
        return name

    # Try any H1
    h1_match = re.search(r'<h1[^>]*>\s*(.+?)\s*</h1>', content)
    if h1_match:
        name = h1_match.group(1).strip()
        name = re.sub(r'<[^>]+>', '', name)
        return name

    # Try title tag
    title_match = re.search(r'<title>[^<]*?(?:Mecanico|Servicio)\s+\w+\s+(.+?)\s+Santiago', content, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()

    # Fallback: derive from filename
    basename = os.path.basename(filepath).replace('.html', '')
    return basename.replace('-', ' ').title()


def get_vehicle_slug(filepath):
    """Extract vehicle slug from filename."""
    basename = os.path.basename(filepath)
    return basename.replace('.html', '')


def update_vehicle_file(filepath):
    """Update a single vehicle HTML file with services + vehicles section."""
    slug = get_vehicle_slug(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'servicios-destacados' in content:
        print(f"  SKIP {slug} - already has featured services")
        return False

    if 'vehiculos-comuna' in content:
        print(f"  SKIP {slug} - already has vehicles section")
        return False

    # Extract vehicle name
    vehicle_name = extract_vehicle_name(content, filepath)
    print(f"  Vehicle name: {vehicle_name}")

    # Generate new sections
    services_html = generate_featured_services_section(vehicle_name, slug)
    vehicles_html = generate_vehicles_section(vehicle_name, slug)

    # Strategy: Insert both sections BEFORE the footer
    # Look for the footer tag
    combined_html = services_html + '\n' + vehicles_html

    # Try insertion points in order of preference
    insertion_points = [
        '<footer class="main-footer">',   # Most common - footer tag
        '<footer ',                         # Any footer tag
    ]

    inserted = False
    for point in insertion_points:
        idx = content.find(point)
        if idx != -1:
            content = content[:idx] + combined_html + '\n' + content[idx:]
            inserted = True
            print(f"  Inserted before: {point}")
            break

    if not inserted:
        print(f"  WARNING: Could not find insertion point for {slug}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    print("=" * 60)
    print("ACTUALIZACION MASIVA DE VEHICULOS")
    print("=" * 60)

    # Get all vehicle HTML files (EXCEPT index.html)
    vehicle_files = sorted(glob.glob(os.path.join(VEHICULOS_DIR, "*.html")))
    vehicle_files = [f for f in vehicle_files if os.path.basename(f) != 'index.html']

    print(f"\nFound {len(vehicle_files)} vehicle files (excluding index.html)")

    updated = 0
    skipped = 0
    errors = 0

    for filepath in vehicle_files:
        slug = get_vehicle_slug(filepath)
        print(f"\nProcessing: {slug}...")

        try:
            result = update_vehicle_file(filepath)
            if result:
                updated += 1
                print(f"  OK UPDATED {slug}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR {slug}: {e}")

    print("\n" + "=" * 60)
    print(f"RESUMEN:")
    print(f"  Vehiculos actualizados: {updated}")
    print(f"  Vehiculos saltados: {skipped}")
    print(f"  Errores: {errors}")
    print(f"  Total archivos: {len(vehicle_files)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
