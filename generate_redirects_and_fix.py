import os
import re
import glob

# ============================================================
# 1. GENERATE _redirects FILE FOR CLOUDFLARE PAGES
# ============================================================
# Format: /old-path /new-path 301

redirect_lines = []

# Helper to get comuna names
comuna_files = sorted(glob.glob('comunas/*.html'))
vehiculo_files = sorted(glob.glob('vehiculos/*.html'))
servicio_files = sorted(glob.glob('servicios/*.html'))
marca_files = sorted(glob.glob('marcas_automotrices/*.html'))

en_comuna_files = sorted(glob.glob('en/comunas/*.html'))
en_vehiculo_files = sorted(glob.glob('en/vehiculos/*.html'))
en_servicio_files = sorted(glob.glob('en/servicios/*.html'))
en_marca_files = sorted(glob.glob('en/marcas_automotrices/*.html'))

# ES comunas
for f in comuna_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/comunas/{name}.html /comunas/{name} 301')

# ES vehiculos
for f in vehiculo_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/vehiculos/{name}.html /vehiculos/{name} 301')

# ES servicios
for f in servicio_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/servicios/{name}.html /servicios/{name} 301')

# ES marcas
for f in marca_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/marcas_automotrices/{name}.html /marcas_automotrices/{name} 301')

# EN comunas
for f in en_comuna_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/en/comunas/{name}.html /en/comunas/{name} 301')

# EN vehiculos
for f in en_vehiculo_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/en/vehiculos/{name}.html /en/vehiculos/{name} 301')

# EN servicios
for f in en_servicio_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/en/servicios/{name}.html /en/servicios/{name} 301')

# EN marcas
for f in en_marca_files:
    name = os.path.basename(f).replace('.html', '')
    redirect_lines.append(f'/en/marcas_automotrices/{name}.html /en/marcas_automotrices/{name} 301')

# Other ES pages
for page in ['contacto', 'faq', 'quienes-somos', 'politica-privacidad', 'inspeccion-mecanica', 'servicios-domicilio', '404']:
    redirect_lines.append(f'/{page}.html /{page} 301')

# Other EN pages
for page in ['contacto', 'faq', 'about-us', 'privacy-policy', 'mechanical-inspection', 'services-at-home', '404']:
    redirect_lines.append(f'/en/{page}.html /en/{page} 301')

# Root pages
redirect_lines.append('/index.html / 301')
redirect_lines.append('/en/index.html /en/ 301')
redirect_lines.append('/blog/index.html /blog/ 301')
redirect_lines.append('/en/blog/index.html /en/blog/ 301')

# Write _redirects
with open('_redirects', 'w', encoding='utf-8') as f:
    f.write('# Redirects for Cloudflare Pages\n')
    f.write('# All .html URLs redirect 301 to canonical (no .html) URLs\n')
    f.write('# This prevents duplicate content and consolidates authority\n\n')
    for line in redirect_lines:
        f.write(line + '\n')

print(f"Generated _redirects with {len(redirect_lines)} redirects")

# ============================================================
# 2. FIX SITEMAP - Only canonical URLs (no .html)
# ============================================================
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

# Remove .html from sitemap URLs
# Pattern: <loc>https://mecanico247.com/comunas/alhue.html</loc>
# Should be: <loc>https://mecanico247.com/comunas/alhue</loc>
sitemap = re.sub(r'\.html</loc>', '</loc>', sitemap)
sitemap = re.sub(r'\.html"', '"', sitemap)  # hreflang URLs too

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

# Verify
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()
html_in_loc = re.findall(r'<loc>[^<]*\.html[^<]*</loc>', content)
print(f"Sitemap URLs still with .html: {len(html_in_loc)}")
if html_in_loc:
    for h in html_in_loc[:5]:
        print(f"  {h}")

print("Sitemap fixed - canonical URLs only (no .html)")
