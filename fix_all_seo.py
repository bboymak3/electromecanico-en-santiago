#!/usr/bin/env python3
"""
FIX COMPLETO SEO - mecanico247.com
Corrige TODOS los problemas de indexación encontrados:

1. Crea _headers con X-Robots-Tag: noindex para rutas basura
2. Corrige dropdown comunas en 52 páginas (/#contacto → URLs reales)
3. Elimina .html de TODOS los enlaces internos
4. Corrige dropdown comunas en servicios-domicilio.html (#contacto → URLs reales)
5. Corrige breadcrumb schema en páginas comuna
6. Actualiza robots.txt con más patrones basura
7. Actualiza _redirects con más patrones basura
"""

import os
import re
import glob

BASE = '/home/z/my-project/Globalpro'

# Lista completa de comunas con slugs
COMUNAS = [
    ("Alhué", "alhue"),
    ("Buín", "buin"),
    ("Calera de Tango", "calera-de-tango"),
    ("Cerrillos", "cerrillos"),
    ("Cerro Navia", "cerro-navia"),
    ("Colina", "colina"),
    ("Conchalí", "conchali"),
    ("Curacaví", "curacavi"),
    ("El Bosque", "el-bosque"),
    ("El Monte", "el-monte"),
    ("Estación Central", "estacion-central"),
    ("Huechuraba", "huechuraba"),
    ("Independencia", "independencia"),
    ("Isla de Maipo", "isla-de-maipo"),
    ("La Cisterna", "la-cisterna"),
    ("La Florida", "la-florida"),
    ("La Granja", "la-granja"),
    ("La Pintana", "la-pintana"),
    ("La Reina", "la-reina"),
    ("Lampa", "lampa"),
    ("Las Condes", "las-condes"),
    ("Lo Barnechea", "lo-barnechea"),
    ("Lo Espejo", "lo-espejo"),
    ("Lo Prado", "lo-prado"),
    ("Macul", "macul"),
    ("Maipú", "maipu"),
    ("María Pinto", "maria-pinto"),
    ("Melipilla", "melipilla"),
    ("Ñuñoa", "nunoa"),
    ("Padre Hurtado", "padre-hurtado"),
    ("Paine", "paine"),
    ("Pedro Aguirre Cerda", "pedro-aguirre-cerda"),
    ("Peñaflor", "penaflor"),
    ("Peñalolén", "penalolen"),
    ("Pirque", "pirque"),
    ("Providencia", "providencia"),
    ("Pudahuel", "pudahuel"),
    ("Puente Alto", "puente-alto"),
    ("Quilicura", "quilicura"),
    ("Quinta Normal", "quinta-normal"),
    ("Recoleta", "recoleta"),
    ("Renca", "renca"),
    ("San Bernardo", "san-bernardo"),
    ("San Joaquín", "san-joaquin"),
    ("San José de Maipo", "san-jose-de-maipo"),
    ("San Miguel", "san-miguel"),
    ("San Pedro", "san-pedro"),
    ("San Ramón", "san-ramon"),
    ("Santiago", "santiago"),
    ("Talagante", "talagante"),
    ("Tiltil", "tiltil"),
    ("Vitacura", "vitacura"),
]

# Generar el HTML del dropdown de comunas con URLs correctas
def generate_comuna_dropdown_items(active_slug=None):
    """Genera los <li> items del dropdown de comunas con enlaces correctos"""
    items = []
    for name, slug in COMUNAS:
        if slug == active_slug:
            items.append(f'<li><a class="dropdown-item active" href="#" aria-current="page">{name}</a></li>')
        else:
            items.append(f'<li><a class="dropdown-item" href="/comunas/{slug}">{name}</a></li>')
    return ''.join(items)

def fix_comuna_dropdown_in_html(content, active_slug=None):
    """Reemplaza el dropdown de comunas en el HTML con enlaces correctos"""
    # Buscar el dropdown de comunas - patrón: <ul class="dropdown-menu...> ... </ul>
    # dentro del dropdown de Comunas
    
    # Patrón para encontrar el contenido del dropdown de comunas
    # Busca desde el <ul del dropdown-menu hasta el </ul> que le sigue
    pattern = r'(<a[^>]*id="comunasDropdown"[^>]*>.*?</a>\s*<ul\s+class="dropdown-menu[^"]*"[^>]*>)(.*?)(</ul>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_items = generate_comuna_dropdown_items(active_slug)
        new_dropdown = match.group(1) + new_items + match.group(3)
        content = content[:match.start()] + new_dropdown + content[match.end():]
    
    return content

def fix_html_links(content):
    """Elimina .html de todos los enlaces internos"""
    # Fix: /contacto.html → /contacto
    # Fix: /faq.html → /faq
    # Fix: /quienes-somos.html → /quienes-somos
    # Fix: /politica-privacidad.html → /politica-privacidad
    # Fix: /servicios-domicilio.html → /servicios-domicilio
    # Fix: /inspeccion-mecanica.html → /inspeccion-mecanica
    # Fix: /comunas/xxx.html → /comunas/xxx
    # Fix: /vehiculos/xxx.html → /vehiculos/xxx
    # Fix: /servicios/xxx.html → /servicios/xxx
    # Fix: /marcas_automotrices/xxx.html → /marcas_automotrices/xxx
    # Fix: /blog/xxx.html → /blog/xxx
    
    replacements = [
        (r'href="/contacto\.html"', 'href="/contacto"'),
        (r'href="/faq\.html"', 'href="/faq"'),
        (r'href="/quienes-somos\.html"', 'href="/quienes-somos"'),
        (r'href="/politica-privacidad\.html"', 'href="/politica-privacidad"'),
        (r'href="/servicios-domicilio\.html"', 'href="/servicios-domicilio"'),
        (r'href="/inspeccion-mecanica\.html"', 'href="/inspeccion-mecanica"'),
        (r'href="/comunas/([a-z0-9-]+)\.html"', r'href="/comunas/\1"'),
        (r'href="/vehiculos/([a-z0-9-]+)\.html"', r'href="/vehiculos/\1"'),
        (r'href="/servicios/([a-z0-9-]+)\.html"', r'href="/servicios/\1"'),
        (r'href="/marcas_automotrices/([a-z0-9-]+)\.html"', r'href="/marcas_automotrices/\1"'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    return content

def fix_breadcrumb_schema(content, correct_slug):
    """Corrige el BreadcrumbList schema para usar la URL correcta sin .html"""
    # Buscar URLs incorrectas en breadcrumb: santiago-centro.html → santiago
    # Patrón general: item": "https://mecanico247.com/comunas/XXX.html"
    # Debe ser: item": "https://mecanico247.com/comunas/XXX"
    
    pattern = r'"item":\s*"https://mecanico247\.com/comunas/[^"]*\.html"'
    replacement = lambda m: m.group(0).replace('.html', '')
    content = re.sub(pattern, replacement, content)
    
    # También corregir específicamente santiago-centro → santiago
    content = content.replace(
        '"item": "https://mecanico247.com/comunas/santiago-centro"',
        '"item": "https://mecanico247.com/comunas/santiago"'
    )
    
    return content

def fix_service_schema_url(content):
    """Corrige URLs en Service schema que apuntan a santiago-centro"""
    content = content.replace(
        '"url": "https://mecanico247.com/comunas/santiago-centro"',
        '"url": "https://mecanico247.com/comunas/santiago"'
    )
    return content

# ============================================================
# FIX 1: Crear _headers para X-Robots-Tag
# ============================================================
def create_headers_file():
    print("Creating _headers file...")
    
    # Patrones basura que Google indexó - deben ser noindex
    ghost_prefixes = [
        "taxis", "aire-acondicionado", "frenos", "marcas", "diagnostico",
        "emergencias", "mecanica", "aceite", "electricidad", "scanner",
        "mecanico", "servicio", "autos", "reparacion", "auxilio",
        "24horas", "urgencia", "blog/comunas", "comunas/comunas",
        "vehiculos/comunas", "vehiculos/vehiculos", "comunas/vehiculos",
        "servicios/comunas", "servicios/vehiculos", "marcas/comunas",
        "marcas/vehiculos", "blog/vehiculos"
    ]
    
    headers_content = "# ===================================================\n"
    headers_content += "# _headers - mecanico247.com\n"
    headers_content += "# Bloquea indexación de rutas basura/fantasma\n"
    headers_content += "# Cloudflare Pages sirve estas URLs con 200 porque\n"
    headers_content += "# hace suffix-matching. Este header dice a Google\n"
    headers_content += "# que NO indexe estas páginas.\n"
    headers_content += "# ===================================================\n\n"
    
    for prefix in ghost_prefixes:
        headers_content += f"/{prefix}/*\n"
        headers_content += f"  X-Robots-Tag: noindex, nofollow\n\n"
    
    # También agregar 404 status para rutas que definitivamente no existen
    # Cloudflare Pages _headers soporta X-Robots-Tag
    
    headers_path = os.path.join(BASE, "_headers")
    with open(headers_path, 'w', encoding='utf-8') as f:
        f.write(headers_content)
    print(f"  Created: {headers_path}")

# ============================================================
# FIX 2: Corregir TODAS las páginas comuna
# ============================================================
def fix_all_comuna_pages():
    print("Fixing all comuna pages...")
    
    comuna_dir = os.path.join(BASE, "comunas")
    comuna_files = glob.glob(os.path.join(comuna_dir, "*.html"))
    
    for filepath in comuna_files:
        filename = os.path.basename(filepath)
        slug = filename.replace('.html', '')
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix dropdown de comunas (/#contacto → URLs reales)
        content = fix_comuna_dropdown_in_html(content, active_slug=slug)
        
        # 2. Fix enlaces con .html
        content = fix_html_links(content)
        
        # 3. Fix breadcrumb schema
        content = fix_breadcrumb_schema(content, slug)
        
        # 4. Fix service schema URL
        content = fix_service_schema_url(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: comunas/{filename}")
        else:
            print(f"  No changes: comunas/{filename}")

# ============================================================
# FIX 3: Corregir servicios-domicilio.html
# ============================================================
def fix_servicios_domicilio():
    print("Fixing servicios-domicilio.html...")
    
    filepath = os.path.join(BASE, "servicios-domicilio.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Fix dropdown comunas (#contacto → URLs reales)
    content = fix_comuna_dropdown_in_html(content, active_slug=None)
    
    # 2. Fix enlaces con .html
    content = fix_html_links(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Fixed: servicios-domicilio.html")
    else:
        print("  No changes: servicios-domicilio.html")

# ============================================================
# FIX 4: Corregir páginas de servicios
# ============================================================
def fix_service_pages():
    print("Fixing service pages...")
    
    service_dir = os.path.join(BASE, "servicios")
    service_files = glob.glob(os.path.join(service_dir, "*.html"))
    
    for filepath in service_files:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix enlaces con .html
        content = fix_html_links(content)
        
        # 2. Fix comuna links in service pages (tienen solo 5 comunas)
        # Replace /comunas/xxx.html with /comunas/xxx
        content = re.sub(r'href="/comunas/([a-z0-9-]+)\.html"', r'href="/comunas/\1"', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: servicios/{filename}")
        else:
            print(f"  No changes: servicios/{filename}")

# ============================================================
# FIX 5: Corregir páginas de vehículos
# ============================================================
def fix_vehicle_pages():
    print("Fixing vehicle pages...")
    
    vehicle_dir = os.path.join(BASE, "vehiculos")
    vehicle_files = glob.glob(os.path.join(vehicle_dir, "*.html"))
    
    for filepath in vehicle_files:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix enlaces con .html
        content = fix_html_links(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: vehiculos/{filename}")
        else:
            print(f"  No changes: vehiculos/{filename}")

# ============================================================
# FIX 6: Corregir páginas raíz
# ============================================================
def fix_root_pages():
    print("Fixing root pages...")
    
    root_files = [
        "index.html", "contacto.html", "faq.html", 
        "quienes-somos.html", "politica-privacidad.html",
        "inspeccion-mecanica.html"
    ]
    
    for filename in root_files:
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix enlaces con .html
        content = fix_html_links(content)
        
        # 2. Fix comuna links
        content = re.sub(r'href="/comunas/([a-z0-9-]+)\.html"', r'href="/comunas/\1"', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: {filename}")
        else:
            print(f"  No changes: {filename}")

# ============================================================
# FIX 7: Corregir páginas de marcas
# ============================================================
def fix_marcas_pages():
    print("Fixing marcas_automotrices pages...")
    
    marcas_dir = os.path.join(BASE, "marcas_automotrices")
    marcas_files = glob.glob(os.path.join(marcas_dir, "*.html"))
    
    for filepath in marcas_files:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix enlaces con .html
        content = fix_html_links(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: marcas_automotrices/{filename}")
        else:
            print(f"  No changes: marcas_automotrices/{filename}")

# ============================================================
# FIX 8: Corregir blog pages
# ============================================================
def fix_blog_pages():
    print("Fixing blog pages...")
    
    blog_dir = os.path.join(BASE, "blog")
    blog_files = glob.glob(os.path.join(blog_dir, "*.html"))
    
    for filepath in blog_files:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. Fix enlaces con .html
        content = fix_html_links(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: blog/{filename}")
        else:
            print(f"  No changes: blog/{filename}")

# ============================================================
# FIX 9: Actualizar robots.txt
# ============================================================
def update_robots_txt():
    print("Updating robots.txt...")
    
    robots_content = """# ===================================================
# robots.txt - GlobalPro Automotriz
# https://mecanico247.com
# ===================================================

# Sitemaps
Sitemap: https://mecanico247.com/sitemap.xml

# ===================================================
# REGLAS PARA TODOS LOS CRAWLERS (incluido Googlebot)
# Permitir solo las rutas válidas del sitio
# Bloquear prefijos inexistentes que generaron URLs basura
# ===================================================
User-agent: *
Allow: /$
Allow: /comunas/
Allow: /vehiculos/
Allow: /servicios/
Allow: /blog/
Allow: /marcas_automotrices/
Allow: /contacto
Allow: /faq
Allow: /quienes-somos
Allow: /politica-privacidad
Allow: /inspeccion-mecanica
Allow: /servicios-domicilio
Allow: /sitemap.xml
Allow: /robots.txt

# Archivos y carpetas que NO se deben rastrear
Disallow: /css/
Disallow: /js/
Disallow: /images/
Disallow: /assets/
Disallow: /images/imagen/

# ===================================================
# URLS FANTASMA - prefijos inexistentes que Google indexó
# por enlaces relativos. Bloquear para que se desindexen.
# IMPORTANTE: Estas reglas aplican a TODOS los crawlers
# incluyendo Googlebot
# ===================================================
Disallow: /taxis/
Disallow: /aire-acondicionado/
Disallow: /frenos/
Disallow: /marcas/
Disallow: /diagnostico/
Disallow: /emergencias/
Disallow: /mecanica/
Disallow: /aceite/
Disallow: /electricidad/
Disallow: /scanner/
Disallow: /mecanico/
Disallow: /servicio/
Disallow: /autos/
Disallow: /reparacion/
Disallow: /auxilio/
Disallow: /24horas/
Disallow: /urgencia/

# Patrones adicionales de URLs basura (combinaciones)
Disallow: /comunas/comunas/
Disallow: /vehiculos/comunas/
Disallow: /vehiculos/vehiculos/
Disallow: /comunas/vehiculos/
Disallow: /servicios/comunas/
Disallow: /servicios/vehiculos/
Disallow: /blog/comunas/
Disallow: /blog/vehiculos/
Disallow: /marcas/vehiculos/

# Bloquear bots maliciosos o innecesarios
User-agent: AhrefsBot
Crawl-delay: 10

User-agent: SemrushBot
Crawl-delay: 10

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: Baiduspider
Disallow: /

User-agent: Sogou
Disallow: /

User-agent: YandexBot
Crawl-delay: 10
"""
    
    robots_path = os.path.join(BASE, "robots.txt")
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print(f"  Updated: {robots_path}")

# ============================================================
# FIX 10: Actualizar _redirects con más patrones
# ============================================================
def update_redirects():
    print("Updating _redirects with additional patterns...")
    
    filepath = os.path.join(BASE, "_redirects")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add additional ghost URL patterns at the top of the redirects section
    additional_patterns = """
# ===================================================
# PATRONES ADICIONALES DE URLs BASURA (combinaciones)
# Estas rutas nunca existieron en el sitio
# ===================================================
/comunas/comunas/*  /  301
/vehiculos/comunas/*  /  301
/vehiculos/vehiculos/*  /  301
/comunas/vehiculos/*  /  301
/servicios/comunas/*  /  301
/servicios/vehiculos/*  /  301
/blog/comunas/*  /  301
/blog/vehiculos/*  /  301
/marcas/vehiculos/*  /  301
"""
    
    # Insert after the existing ghost URL patterns section
    insert_marker = "/urgencia/*  /  301"
    if insert_marker in content and "/comunas/comunas/*" not in content:
        content = content.replace(
            insert_marker,
            insert_marker + "\n" + additional_patterns
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filepath}")
    else:
        print(f"  Already updated or marker not found: {filepath}")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("FIX COMPLETO SEO - mecanico247.com")
    print("=" * 60)
    
    # 1. Create _headers
    create_headers_file()
    
    # 2. Fix all comuna pages
    fix_all_comuna_pages()
    
    # 3. Fix servicios-domicilio.html
    fix_servicios_domicilio()
    
    # 4. Fix service pages
    fix_service_pages()
    
    # 5. Fix vehicle pages
    fix_vehicle_pages()
    
    # 6. Fix root pages
    fix_root_pages()
    
    # 7. Fix marcas pages
    fix_marcas_pages()
    
    # 8. Fix blog pages
    fix_blog_pages()
    
    # 9. Update robots.txt
    update_robots_txt()
    
    # 10. Update _redirects
    update_redirects()
    
    print("=" * 60)
    print("ALL FIXES COMPLETED!")
    print("=" * 60)
