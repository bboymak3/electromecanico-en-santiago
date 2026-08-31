import re

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add .html extension to URLs that need it
# Pattern: /comunas/X, /vehiculos/X, /servicios/X, /marcas_automotrices/X
# But NOT /blog/ URLs (those don't use .html)
# Also NOT /en/ versions that already have the same pattern

# Fix comunas URLs without .html
# Match: https://mecanico247.com/comunas/WORD but NOT if already .html
content = re.sub(
    r'(https://mecanico247\.com/(?:en/)?comunas/([a-z-]+))(</loc>)',
    lambda m: m.group(1) + '.html' + m.group(3) if not m.group(2).endswith('.html') else m.group(0),
    content
)

# Fix vehiculos URLs
content = re.sub(
    r'(https://mecanico247\.com/(?:en/)?vehiculos/([a-z0-9-]+))(</loc>)',
    lambda m: m.group(1) + '.html' + m.group(3) if not m.group(2).endswith('.html') else m.group(0),
    content
)

# Fix servicios URLs
content = re.sub(
    r'(https://mecanico247\.com/(?:en/)?servicios/([a-z0-9-]+))(</loc>)',
    lambda m: m.group(1) + '.html' + m.group(3) if not m.group(2).endswith('.html') else m.group(0),
    content
)

# Fix marcas_automotrices URLs
content = re.sub(
    r'(https://mecanico247\.com/(?:en/)?marcas_automotrices/([a-z0-9-]+))(</loc>)',
    lambda m: m.group(1) + '.html' + m.group(3) if not m.group(2).endswith('.html') else m.group(0),
    content
)

# Fix hreflang URLs too (same patterns)
# For hreflang href attributes
content = re.sub(
    r'(href="https://mecanico247\.com/(?:en/)?comunas/([a-z-]+)")',
    lambda m: m.group(1) if m.group(2).endswith('.html') else m.group(1).replace(m.group(2), m.group(2) + '.html'),
    content
)
content = re.sub(
    r'(href="https://mecanico247\.com/(?:en/)?vehiculos/([a-z0-9-]+)")',
    lambda m: m.group(1) if m.group(2).endswith('.html') else m.group(1).replace(m.group(2), m.group(2) + '.html'),
    content
)
content = re.sub(
    r'(href="https://mecanico247\.com/(?:en/)?servicios/([a-z0-9-]+)")',
    lambda m: m.group(1) if m.group(2).endswith('.html') else m.group(1).replace(m.group(2), m.group(2) + '.html'),
    content
)
content = re.sub(
    r'(href="https://mecanico247\.com/(?:en/)?marcas_automotrices/([a-z0-9-]+)")',
    lambda m: m.group(1) if m.group(2).endswith('.html') else m.group(1).replace(m.group(2), m.group(2) + '.html'),
    content
)

# Fix 2: Fix priority floating point issues
content = re.sub(r'0\.7000000000000001', '0.7', content)
content = re.sub(r'0\.9000000000000001', '0.9', content)
content = re.sub(r'0\.8000000000000001', '0.8', content)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("Sitemap fixed!")

# Verify
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

import re as re2
missing_html = re2.findall(r'<loc>https://mecanico247\.com/(?:en/)?(?:comunas|vehiculos|servicios|marcas_automotrices)/[a-z0-9-]+</loc>', content)
bad = [x for x in missing_html if '.html' not in x]
print(f"URLs still missing .html: {len(bad)}")
for x in bad[:5]:
    print(f"  {x}")

float_issues = re2.findall(r'0\.\d{10,}', content)
print(f"Floating point issues remaining: {len(float_issues)}")
