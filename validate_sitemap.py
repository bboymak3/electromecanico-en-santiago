#!/usr/bin/env python3
"""
Valida el sitemap.xml contra:
1. El sitio en producción (HTTP status de cada URL)
2. Los archivos HTML reales del repo (descubre URLs faltantes)

Genera un nuevo sitemap limpio y ordenado con SOLO las URLs que existen realmente.
"""
import os
import re
import subprocess
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

REPO = Path(__file__).resolve().parent
SITEMAP = REPO / "sitemap.xml"
DOMAIN = "https://mecanico247.com"
TODAY = datetime.now().strftime("%Y-%m-%d")

# Máximo de hilos para validación HTTP (paralelo)
MAX_WORKERS = 20
# Timeout por request (segundos)
HTTP_TIMEOUT = 15


def extract_sitemap_urls():
    """Extrae todas las URLs del sitemap.xml actual."""
    content = SITEMAP.read_text(encoding="utf-8", errors="replace")
    urls = re.findall(r'<loc>([^<]+)</loc>', content)
    return urls


def get_real_html_files():
    """
    Descubre TODAS las URLs reales basándose en los HTML del repo.
    Mapea cada .html a su URL pública.
    """
    urls = set()
    
    # Buscar todos los .html del repo (excluyendo .git, scripts)
    html_files = []
    for ext in ["*.html"]:
        for p in REPO.rglob(ext):
            if ".git" in p.parts:
                continue
            html_files.append(p)
    
    for html_path in html_files:
        rel = html_path.relative_to(REPO).as_posix()
        
        # google verification file → skip
        if "google7a5c4682" in rel:
            continue
        
        # 404.html → skip (no indexable)
        if rel == "404.html":
            continue
        
        # Convertir path a URL
        # index.html → /
        if rel == "index.html":
            urls.add(f"{DOMAIN}/")
            continue
        
        # en/index.html → /en/
        if rel == "en/index.html":
            urls.add(f"{DOMAIN}/en/")
            continue
        
        # subcarpeta/index.html → /subcarpeta/
        if rel.endswith("/index.html"):
            path = rel.replace("/index.html", "/")
            urls.add(f"{DOMAIN}/{path}")
            continue
        
        # resto .html → URL sin extensión
        path = rel.replace(".html", "")
        urls.add(f"{DOMAIN}/{path}")
    
    return sorted(urls)


def check_url_status(url):
    """Verifica el status HTTP de una URL con curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(HTTP_TIMEOUT), "-L", url],
            capture_output=True, text=True, timeout=HTTP_TIMEOUT + 5
        )
        code = result.stdout.strip()
        return url, code
    except Exception as e:
        return url, "ERROR"


def validate_urls_parallel(urls):
    """Valida todas las URLs en paralelo."""
    results = {}
    print(f"Validando {len(urls)} URLs en paralelo ({MAX_WORKERS} hilos)...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_url_status, url): url for url in urls}
        
        completed = 0
        for future in as_completed(futures):
            url, code = future.result()
            results[url] = code
            completed += 1
            if completed % 50 == 0 or completed == len(urls):
                print(f"  [{completed}/{len(urls)}] procesadas")
    
    return results


def categorize_url(url):
    """Categoriza una URL para asignar prioridad."""
    # Raíz
    if url == f"{DOMAIN}/":
        return ("1.0", "weekly", "root")
    
    # EN root
    if url == f"{DOMAIN}/en/":
        return ("0.9", "weekly", "en-root")
    
    path = url.replace(DOMAIN, "").lstrip("/")
    
    # Páginas raíz importantes
    if "/" not in path:
        if path.startswith("en/"):
            return ("0.8", "monthly", "en-root-page")
        if path in ["contacto", "quienes-somos", "faq", "servicios-domicilio",
                    "inspeccion-mecanica", "politica-privacidad"]:
            return ("0.9", "monthly", "root-page")
        # Servicios en raíz
        return ("0.8", "monthly", "service")
    
    # Subcarpetas
    section = path.split("/")[0]
    if section == "en":
        if path.count("/") == 1:
            return ("0.7", "monthly", "en-root-page")
        en_section = path.split("/")[1]
        if en_section == "comunas":
            return ("0.8", "monthly", "en-comuna")
        elif en_section == "vehiculos":
            return ("0.7", "monthly", "en-vehiculo")
        elif en_section == "servicios":
            return ("0.8", "monthly", "en-servicio")
        elif en_section == "marcas_automotrices":
            return ("0.6", "monthly", "en-marca")
        return ("0.6", "monthly", "en-other")
    
    if section == "comunas":
        return ("0.9", "monthly", "comuna")
    elif section == "vehiculos":
        return ("0.8", "monthly", "vehiculo")
    elif section == "servicios":
        return ("0.8", "monthly", "servicio")
    elif section == "marcas_automotrices":
        return ("0.7", "monthly", "marca")
    elif section == "blog":
        return ("0.6", "monthly", "blog")
    
    return ("0.6", "monthly", "other")


def generate_sitemap(urls):
    """Genera el XML del sitemap ordenado por categoría."""
    # Ordenar URLs: raíz → en raíz → ES páginas → EN páginas → comunas → servicios → vehículos → marcas → blog
    def sort_key(url):
        path = url.replace(DOMAIN, "").lstrip("/")
        if url == f"{DOMAIN}/":
            return (0, path)
        if url == f"{DOMAIN}/en/":
            return (1, path)
        
        if "/" not in path:
            # Raíz
            if path.startswith("en/"):
                return (3, path)
            return (2, path)
        
        sections = path.split("/")
        if sections[0] == "en":
            en_sec = sections[1] if len(sections) > 1 else ""
            order = {"comunas": 5, "servicios": 6, "vehiculos": 7, "marcas_automotrices": 8, "blog": 9}
            return (order.get(en_sec, 10), path)
        
        order = {"comunas": 11, "servicios": 12, "vehiculos": 13, "marcas_automotrices": 14, "blog": 15}
        return (order.get(sections[0], 20), path)
    
    urls_sorted = sorted(urls, key=sort_key)
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls_sorted:
        priority, freq, category = categorize_url(url)
        xml += '  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{TODAY}</lastmod>\n'
        xml += f'    <changefreq>{freq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>\n'
    return xml, urls_sorted


def main():
    print("=" * 60)
    print("VALIDACIÓN Y REGENERACIÓN DE SITEMAP")
    print(f"Repo: {REPO}")
    print(f"Dominio: {DOMAIN}")
    print(f"Fecha: {TODAY}")
    print("=" * 60)
    
    # 1. Extraer URLs del sitemap actual
    print("\n1. Extrayendo URLs del sitemap actual...")
    sitemap_urls = extract_sitemap_urls()
    print(f"   URLs en sitemap: {len(sitemap_urls)}")
    
    # 2. Descubrir URLs reales del repo
    print("\n2. Descubriendo URLs reales del repo (HTML files)...")
    real_urls = get_real_html_files()
    print(f"   URLs reales en repo: {len(real_urls)}")
    
    # 3. Combinar: todas las URLs a validar
    all_urls = set(sitemap_urls) | set(real_urls)
    print(f"\n3. Total URLs a validar: {len(all_urls)}")
    
    # 4. URLs en sitemap pero NO en repo (huérfanas)
    orphan_urls = set(sitemap_urls) - set(real_urls)
    print(f"   URLs en sitemap pero NO en repo: {len(orphan_urls)}")
    
    # 5. URLs en repo pero NO en sitemap (faltantes)
    missing_urls = set(real_urls) - set(sitemap_urls)
    print(f"   URLs en repo pero NO en sitemap: {len(missing_urls)}")
    
    # 6. Validar HTTP status de todas las URLs
    print(f"\n4. Validando HTTP status de {len(all_urls)} URLs...")
    results = validate_urls_parallel(sorted(all_urls))
    
    # 7. Filtrar URLs válidas (200 o 301/308 redirect)
    valid_urls = []
    invalid_urls = []
    for url, code in results.items():
        if code in ["200", "301", "308"]:
            valid_urls.append(url)
        else:
            invalid_urls.append((url, code))
    
    print(f"\n5. Resultados de validación:")
    print(f"   URLs válidas (200/301/308): {len(valid_urls)}")
    print(f"   URLs inválidas (404/error): {len(invalid_urls)}")
    
    # Mostrar URLs inválidas
    if invalid_urls:
        print(f"\n   URLs inválidas (no se incluirán en sitemap nuevo):")
        for url, code in sorted(invalid_urls)[:20]:
            print(f"     [{code}] {url}")
        if len(invalid_urls) > 20:
            print(f"     ... y {len(invalid_urls) - 20} más")
    
    # 8. Generar nuevo sitemap
    print(f"\n6. Generando nuevo sitemap con {len(valid_urls)} URLs válidas...")
    xml, urls_sorted = generate_sitemap(valid_urls)
    
    # Guardar
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"   ✓ Sitemap guardado: {SITEMAP}")
    print(f"   Total URLs: {len(urls_sorted)}")
    
    # 9. Estadísticas por categoría
    print(f"\n7. Estadísticas por categoría:")
    cat_stats = {}
    for url in urls_sorted:
        _, _, cat = categorize_url(url)
        cat_stats[cat] = cat_stats.get(cat, 0) + 1
    for cat, count in sorted(cat_stats.items()):
        print(f"   - {cat}: {count}")
    
    # 10. Muestras
    print(f"\n8. Muestras del nuevo sitemap:")
    for url in urls_sorted[:5]:
        p, f, c = categorize_url(url)
        print(f"   [{p}] {url}")
    print("   ...")
    for url in urls_sorted[-5:]:
        p, f, c = categorize_url(url)
        print(f"   [{p}] {url}")
    
    print(f"\n{'=' * 60}")
    print(f"✓ SITEMAP REGENERADO")
    print(f"  Antes: {len(sitemap_urls)} URLs")
    print(f"  Ahora: {len(valid_urls)} URLs válidas")
    print(f"  Removidas: {len(sitemap_urls) - len(set(valid_urls) & set(sitemap_urls))} URLs inválidas")
    print(f"  Agregadas: {len(missing_urls & set(valid_urls))} URLs faltantes")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
