import os
import re

# ============================================================
# 1. FIX LANGUAGE SWITCHER - Add animation and color change
# ============================================================

# CSS to add for the language switcher animation
lang_switcher_css = """
/* Language Switcher Styles */
#lang-switcher a, #lang-switcher span {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
#lang-switcher a:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
#lang-switcher a::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  transition: width 0.4s, height 0.4s, top 0.4s, left 0.4s;
}
#lang-switcher a:hover::after {
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
}
@keyframes langPulse {
  0% { box-shadow: 0 0 0 0 rgba(168, 0, 0, 0.4); }
  70% { box-shadow: 0 0 0 8px rgba(168, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(168, 0, 0, 0); }
}
@keyframes langPulseEN {
  0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.4); }
  70% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
}
#lang-switcher .lang-active-es {
  background: linear-gradient(135deg, #a80000 0%, #d32f2f 100%) !important;
  animation: langPulse 2s infinite;
  color: #fff !important;
}
#lang-switcher .lang-active-en {
  background: linear-gradient(135deg, #1a1a2e 0%, #2d2d5e 100%) !important;
  animation: langPulseEN 2s infinite;
  color: #FFC107 !important;
}
"""

# Process ALL HTML files
count_lang = 0
for root, dirs, files in os.walk('.'):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        
        # Skip /en/blog/ pages
        if '/en/blog/' in fpath or '/blog/' in fpath.replace('./blog/', ''):
            if fpath.startswith('./blog/'):
                continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'id="lang-switcher"' not in content:
            continue
        
        original = content
        
        # Add CSS if not already added
        if 'langPulse' not in content:
            # Insert CSS before </head>
            content = content.replace('</head>', '<style>' + lang_switcher_css + '</style>\n</head>')
        
        # Fix Spanish pages (ES is active = span, EN is link)
        # Pattern: <span style="background:#a80000...>🇪🇸 ES</span> <a href="/en/..." style="background:#1a1a2e...>🇬🇧 EN</a>
        if fpath.startswith('./en/'):
            # EN pages: EN is active, ES is link
            # Current after previous fix: <a href="..." style="background:#a80000...>🇪🇸 ES</a> <span style="background:#1a1a2e...>🇬🇧 EN</span>
            content = re.sub(
                r'<a href="([^"]*)" style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700; text-decoration:none;">🇪🇸 ES</a>',
                r'<a href="\1" class="" style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;" onmouseover="this.style.background=\'linear-gradient(135deg, #c62828, #e53935)\'" onmouseout="this.style.background=\'#a80000\'">🇪🇸 ES</a>',
                content
            )
            content = re.sub(
                r'<span style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700;">🇬🇧 EN</span>',
                '<span class="lang-active-en" style="background:linear-gradient(135deg, #1a1a2e, #2d2d5e); color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇬🇧 EN</span>',
                content
            )
        else:
            # ES pages: ES is active, EN is link
            content = re.sub(
                r'<span style="background:#a80000; color:#fff; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700;">🇪🇸 ES</span>',
                '<span class="lang-active-es" style="background:linear-gradient(135deg, #a80000, #d32f2f); color:#fff; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700;">🇪🇸 ES</span>',
                content
            )
            content = re.sub(
                r'<a href="([^"]*)" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0\.8rem; font-weight:700; text-decoration:none;">🇬🇧 EN</a>',
                r'<a href="\1" class="" style="background:#1a1a2e; color:#FFC107; padding:6px 12px; border-radius:6px; font-size:0.8rem; font-weight:700; text-decoration:none;" onmouseover="this.style.background=\'linear-gradient(135deg, #2d2d5e, #4a4a8a)\'" onmouseout="this.style.background=\'#1a1a2e\'">🇬🇧 EN</a>',
                content
            )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count_lang += 1

print(f"Language switcher animated: {count_lang} files")

# ============================================================
# 2. FIX TAPIZADO DE VOLANTES LINK on index.html
# ============================================================
index_path = './index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Change the link from tapizadodevolantes.pages.dev to tapizadodevolante.com
content = content.replace('https://tapizadodevolantes.pages.dev"', 'https://tapizadodevolante.com/"')
content = content.replace('https://tapizadodevolantes.pages.dev/', 'https://tapizadodevolante.com/')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed tapizado link in index.html")

# Fix EN index.html too
en_index_path = './en/index.html'
with open(en_index_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('https://tapizadodevolantes.pages.dev"', 'https://tapizadodevolante.com/"')
content = content.replace('https://tapizadodevolantes.pages.dev/', 'https://tapizadodevolante.com/')
with open(en_index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed tapizado link in en/index.html")

# Fix servicios-domicilio.html
for sf in ['./servicios-domicilio.html']:
    if os.path.exists(sf):
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('https://tapizadodevolantes.pages.dev"', 'https://tapizadodevolante.com/"')
        content = content.replace('https://tapizadodevolantes.pages.dev/', 'https://tapizadodevolante.com/')
        with open(sf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed tapizado link in {sf}")

# ============================================================
# 3. ADD TAPIZADO SECTION TO CERRILLOS PAGE
# ============================================================
cerrillos_path = './comunas/cerrillos.html'
with open(cerrillos_path, 'r', encoding='utf-8') as f:
    content = f.read()

tapizado_section = '''
<!-- NUEVA SECCIÓN: VÍNCULO A TAPIZADO DE VOLANTES -->
<section class="py-5 bg-white">
  <div class="container">
    <div class="alert alert-success border-2 border-success shadow-lg p-4" role="alert">
      <div class="row align-items-center justify-content-center">
        <div class="col-12 text-center mb-4">
             <img src="https://tapizadodevolante.com/images/forrar-un-volante-con-cuero-forrar-volante-coche-en-santiago-monocromatico.jpg" class="img-fluid rounded shadow border border-3 border-success mx-auto d-block" style="max-height: 400px; object-fit: contain;" alt="Tapizado de Volantes">
        </div>
        <div class="col-12 text-center">
          <h2 class="text-uppercase fw-bold text-dark mb-3" style="font-size: 2rem;">
           Tapizado de volantes A DOMICILIO en SANTIAGO
          </h2>
          <p class="text-justify mb-4" style="font-size: 1.1rem; line-height: 1.6;">
tapizado de volantes en Santiago para renovar la imagen de tu auto. Trabajamos cuero de alta calidad, mejorando el agarre y estética del volante. Solución rápida y cómoda sin salir de casa.
          </p>
          <p class="lead mb-4">
            Si quieres informacion para el tapizado de volantes en santiago a domicilio entra al siguiente enlace.
          </p>
          <a href="https://tapizadodevolante.com/" class="btn btn-success btn-lg fw-bold text-white">
            IR AL SITIO WEB <i class="fas fa-external-link-alt ms-2"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# Insert before the footer
if 'Tapizado de volantes' not in content:
    content = content.replace('<!-- FOOTER -->', tapizado_section + '\n<!-- FOOTER -->')
    with open(cerrillos_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added tapizado section to cerrillos.html")
else:
    print("Tapizado section already exists in cerrillos.html")

# Also update the tapizado link if it exists with old URL
content = content.replace('https://tapizadodevolantes.pages.dev"', 'https://tapizadodevolante.com/"')
content = content.replace('https://tapizadodevolantes.pages.dev/', 'https://tapizadodevolante.com/')
with open(cerrillos_path, 'w', encoding='utf-8') as f:
    f.write(content)

# ============================================================
# 4. UPDATE robots.txt - Add /en/ routes
# ============================================================
robots_path = './robots.txt'
with open(robots_path, 'r', encoding='utf-8') as f:
    robots = f.read()

if '/en/' not in robots:
    # Add /en/ routes to Allow section
    robots = robots.replace('Allow: /servicios-domicilio', 'Allow: /en/\nAllow: /en/comunas/\nAllow: /en/vehiculos/\nAllow: /en/servicios/\nAllow: /en/marcas_automotrices/\nAllow: /en/contacto\nAllow: /en/faq\nAllow: /en/about-us\nAllow: /en/privacy-policy\nAllow: /en/mechanical-inspection\nAllow: /en/services-at-home\nAllow: /en/404\nAllow: /servicios-domicilio')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots)
    print("Updated robots.txt with /en/ routes")
else:
    print("robots.txt already has /en/ routes")

print("\nAll fixes applied!")
