import os
import re

"""
Fix language switcher on ALL /en/ pages:
- ES should be an <a> link pointing to the Spanish equivalent page
- EN should be a <span> (you're already here)

For /en/index.html → ES links to /
For /en/comunas/X.html → ES links to /comunas/X.html  
For /en/vehiculos/X.html → ES links to /vehiculos/X.html
For /en/servicios/X.html → ES links to /servicios/X.html (need mapping)
For /en/marcas_automotrices/X.html → ES links to /marcas_automotrices/X.html
For /en/contacto.html → ES links to /contacto.html
For /en/faq.html → ES links to /faq.html
For /en/about-us.html → ES links to /quienes-somos.html
For /en/privacy-policy.html → ES links to /politica-privacidad.html
For /en/404.html → ES links to /404.html
For /en/mechanical-inspection.html → ES links to /inspeccion-mecanica.html
For /en/services-at-home.html → ES links to /servicios-domicilio.html
"""

# Service name mappings (EN slug → ES slug)
service_map = {
    '24-hour-mechanic': 'mecanico-24-horas',
    'oil-change-at-home': 'cambio-de-aceite-a-domicilio',
    'brake-repair-at-home': 'cambio-de-frenos-a-domicilio',
    'air-conditioning': 'aire-acondicionado-automotriz',
    'diagnostic-scan-at-home': 'diagnostico-con-scanner-a-domicilio',
    'auto-electrical-at-home': 'electricidad-automotriz-a-domicilio',
    'emergency-mechanic': 'mecanico-de-emergencia',
}

# Special page mappings
special_map = {
    'about-us': 'quienes-somos',
    'privacy-policy': 'politica-privacidad',
    'mechanical-inspection': 'inspeccion-mecanica',
    'services-at-home': 'servicios-domicilio',
}

count = 0
errors = []

for root, dirs, files in os.walk('./en'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the lang-switcher div
        if 'id="lang-switcher"' not in content:
            continue
        
        # Determine the Spanish URL from the file path
        rel_path = fpath.replace('./en/', '')  # e.g. "index.html", "comunas/santiago.html"
        
        if rel_path == 'index.html':
            es_url = '/'
        elif rel_path.startswith('comunas/'):
            # /en/comunas/santiago.html → /comunas/santiago.html
            es_url = '/' + rel_path
        elif rel_path.startswith('vehiculos/'):
            es_url = '/' + rel_path
        elif rel_path.startswith('marcas_automotrices/'):
            es_url = '/' + rel_path
        elif rel_path.startswith('servicios/'):
            en_slug = rel_path.replace('servicios/', '').replace('.html', '')
            es_slug = service_map.get(en_slug, en_slug)
            es_url = f'/servicios/{es_slug}.html'
        else:
            # Special pages
            en_slug = rel_path.replace('.html', '')
            es_slug = special_map.get(en_slug, en_slug)
            es_url = f'/{es_slug}.html'
        
        # Replace the lang-switcher content
        # Old pattern: <span ...>🇪🇸 ES</span> <a href="/en/..." ...>🇬🇧 EN</a>
        # New pattern: <a href="ES_URL" ...>🇪🇸 ES</a> <span ...>🇬🇧 EN</span>
        
        old_pattern = r'<div id="lang-switcher" style="position:fixed; top:150px; right:15px; z-index:10002; display:flex; gap:4px;">\s*<span style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700;">🇪🇸 ES</span>\s*<a href="[^"]*" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700; text-decoration:none;">🇬🇧 EN</a>\s*</div>'
        
        new_content_str = f'''<div id="lang-switcher" style="position:fixed; top:150px; right:15px; z-index:10002; display:flex; gap:4px;">
  <a href="{es_url}" style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;">🇪🇸 ES</a>
  <span style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇬🇧 EN</span>
</div>'''
        
        new_content = re.sub(old_pattern, new_content_str, content)
        
        if new_content == content:
            # Try a more flexible pattern
            old_pattern2 = r'<span style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700;">🇪🇸 ES</span>'
            old_pattern2b = r'<a href="[^"]*" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700; text-decoration:none;">🇬🇧 EN</a>'
            
            new_content = re.sub(old_pattern2, f'<a href="{es_url}" style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;">🇪🇸 ES</a>', content)
            new_content = re.sub(old_pattern2b, '<span style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇬🇧 EN</span>', new_content)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed: {fpath} → ES link: {es_url}")
        else:
            errors.append(fpath)
            print(f"ERROR - couldn't match pattern: {fpath}")

print(f"\nTotal files fixed: {count}")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
