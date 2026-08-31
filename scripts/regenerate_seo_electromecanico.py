#!/usr/bin/env python3
"""
Regenera sitemap.xml, robots.txt, _redirects y README.md del proyecto
Electromecánico en Santiago basándose en los archivos HTML reales que existen.
"""
import os
from datetime import date
from pathlib import Path

BASE_URL = "https://electromecanico-en-santiago.pages.dev"
TODAY = date.today().isoformat()
ROOT = Path("/home/z/my-project/repos/electromecanico-en-santiago")

# Recopilar todas las URLs reales del sitio
urls = []

# 1. Páginas raíz (sin .html en la URL)
root_html = [
    "index.html",
    "quienes-somos.html",
    "contacto.html",
    "faq.html",
    "servicios-domicilio.html",
    "inspeccion-mecanica.html",
    "politica-privacidad.html",
]
for f in root_html:
    slug = "" if f == "index.html" else f.replace(".html", "")
    priority = "1.0" if f == "index.html" else "0.7"
    freq = "monthly"
    urls.append((f"{BASE_URL}/{slug}", priority, freq))

# 2. Servicios (alta prioridad, ~30 archivos)
servicios_dir = ROOT / "servicios"
if servicios_dir.exists():
    for f in sorted(servicios_dir.glob("*.html")):
        slug = f.name.replace(".html", "")
        urls.append((f"{BASE_URL}/servicios/{slug}", "0.9", "monthly"))

# 3. Comunas (alta prioridad para SEO local, ~52 archivos)
comunas_dir = ROOT / "comunas"
if comunas_dir.exists():
    for f in sorted(comunas_dir.glob("*.html")):
        slug = f.name.replace(".html", "")
        urls.append((f"{BASE_URL}/comunas/{slug}", "0.8", "weekly"))

# 4. Blog (~61 archivos)
blog_dir = ROOT / "blog"
if blog_dir.exists():
    for f in sorted(blog_dir.glob("*.html")):
        slug = f.name.replace(".html", "")
        urls.append((f"{BASE_URL}/blog/{slug}", "0.6", "monthly"))

# 5. Versión inglesa
en_root_files = [
    "index.html", "about-us.html", "contacto.html", "faq.html",
    "mechanical-inspection.html", "privacy-policy.html", "services-at-home.html",
    "404.html"
]
for f in en_root_files:
    slug = "" if f == "index.html" else f.replace(".html", "")
    urls.append((f"{BASE_URL}/en/{slug}", "0.5", "monthly"))

# English comunas
en_comunas = ROOT / "en" / "comunas"
if en_comunas.exists():
    for f in sorted(en_comunas.glob("*.html")):
        slug = f.name.replace(".html", "")
        urls.append((f"{BASE_URL}/en/comunas/{slug}", "0.4", "monthly"))

# English marcas
en_marcas = ROOT / "en" / "marcas_automotrices"
if en_marcas.exists():
    for f in sorted(en_marcas.glob("*.html")):
        slug = f.name.replace(".html", "")
        urls.append((f"{BASE_URL}/en/marcas_automotrices/{slug}", "0.4", "monthly"))

# === SITEMAP.XML ===
sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, prio, freq in urls:
    # Excluir 404 del sitemap (no debe indexarse)
    if "/404" in loc:
        continue
    sitemap_lines.append(
        f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>"
        f"<priority>{prio}</priority><changefreq>{freq}</changefreq></url>"
    )
sitemap_lines.append('</urlset>')
(ROOT / "sitemap.xml").write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")
print(f"sitemap.xml: {len(urls)-1} URLs escritas")

# === ROBOTS.TXT (con 30 user-agents IA) ===
ai_bots = [
    "GPTBot", "ChatGPT-User", "Google-Extended", "PerplexityBot", "Perplexity-User",
    "ClaudeBot", "Claude-Web", "CCBot", "anthropic-ai", "Applebot-Extended",
    "cohere-ai", "Meta-ExternalAgent", "Meta-ExternalFetcher", "Bytespider",
    "Amazonbot", "YandexBot", "Diffbot", "FacebookBot", "Googlebot-Image",
    "Bingbot", "Applebot", "DuckDuckBot", "Slurp", "Baiduspider", "Sogou",
    "Discordbot", "LinkedInBot", "Twitterbot", "Pinterestbot", "WhatsApp"
]
robots_lines = [
    "# robots.txt - Electromecánico en Santiago",
    f"# {BASE_URL}",
    "",
]
for bot in ai_bots:
    robots_lines.append(f"User-agent: {bot}")
    robots_lines.append("Allow: /")
    robots_lines.append("")
robots_lines.extend([
    "User-agent: *",
    "Allow: /",
    "Disallow: /cdn-cgi/",
    "Disallow: /404.html",
    "Disallow: /en/404.html",
    "",
    f"Sitemap: {BASE_URL}/sitemap.xml",
    f"Host: {BASE_URL}",
])
(ROOT / "robots.txt").write_text("\n".join(robots_lines) + "\n", encoding="utf-8")
print(f"robots.txt: {len(ai_bots)} user-agents IA + universal")

# === _REDIRECTS (Cloudflare Pages) ===
redirects_lines = [
    "# Electromecánico en Santiago - Cloudflare Pages Redirects",
    "# Generado automáticamente - " + TODAY,
    "",
    "# Redirección raíz al blog index",
    "/blog /blog/index 301",
    "/blog/ /blog/index 301",
    "",
    "# Redirecciones de servicios antiguos con .html a sin .html",
]
# Servicios .html -> sin .html
for f in sorted(servicios_dir.glob("*.html")) if servicios_dir.exists() else []:
    slug = f.name.replace(".html", "")
    redirects_lines.append(f"/servicios/{slug}.html /servicios/{slug} 301")
redirects_lines.append("")
# Comunas .html -> sin .html
for f in sorted(comunas_dir.glob("*.html")) if comunas_dir.exists() else []:
    slug = f.name.replace(".html", "")
    redirects_lines.append(f"/comunas/{slug}.html /comunas/{slug} 301")
redirects_lines.append("")
# Blog .html -> sin .html
for f in sorted(blog_dir.glob("*.html")) if blog_dir.exists() else []:
    slug = f.name.replace(".html", "")
    redirects_lines.append(f"/blog/{slug}.html /blog/{slug} 301")
redirects_lines.append("")
# Páginas raíz .html -> sin .html (excepto index.html)
for f in root_html:
    if f == "index.html":
        continue
    slug = f.replace(".html", "")
    redirects_lines.append(f"/{slug}.html /{slug} 301")
redirects_lines.append("")
# Inglés
for f in en_root_files:
    if f == "index.html":
        redirects_lines.append("/en/index.html /en/ 301")
    elif f == "404.html":
        continue
    else:
        slug = f.replace(".html", "")
        redirects_lines.append(f"/en/{slug}.html /en/{slug} 301")
(ROOT / "_redirects").write_text("\n".join(redirects_lines) + "\n", encoding="utf-8")
print(f"_redirects: {len(redirects_lines)-3} redirecciones escritas")

# === README.MD ===
total_html = 0
for d, _ in [(ROOT, ""), (servicios_dir, "servicios"), (comunas_dir, "comunas"),
             (blog_dir, "blog")]:
    if d.exists():
        total_html += len(list(d.glob("*.html")))
total_html += len(list((ROOT/"en").glob("*.html"))) if (ROOT/"en").exists() else 0
total_html += len(list((ROOT/"en"/"comunas").glob("*.html"))) if (ROOT/"en"/"comunas").exists() else 0
total_html += len(list((ROOT/"en"/"marcas_automotrices").glob("*.html"))) if (ROOT/"en"/"marcas_automotrices").exists() else 0

# Conteos por sección para el README
total_servicios = len(list(servicios_dir.glob('*.html'))) if servicios_dir.exists() else 0
total_comunas = len(list(comunas_dir.glob('*.html'))) if comunas_dir.exists() else 0
total_blog = len(list(blog_dir.glob('*.html'))) if blog_dir.exists() else 0
total_en = (len(list((ROOT/'en').glob('*.html'))) +
            len(list((ROOT/'en'/'comunas').glob('*.html'))) +
            len(list((ROOT/'en'/'marcas_automotrices').glob('*.html')))) if (ROOT/'en').exists() else 0

readme = f"""# Electromecánico en Santiago

Sitio web oficial de **Electromecánico a Domicilio en Santiago** — servicio de mecánica automotriz, electromecánica y mantenimiento a domicilio en toda la Región Metropolitana.

## 🌐 Sitio en producción

- **URL**: https://electromecanico-en-santiago.pages.dev
- **Hosting**: Cloudflare Pages
- **Repositorio**: https://github.com/bboymak3/electromecanico-en-santiago

## 📞 Contacto

- **Teléfono / WhatsApp**: +56 9 7362 2291
- **WhatsApp directo**: https://wa.me/56973622291

## 🛠️ Stack Tecnológico

- HTML5 semántico
- Bootstrap 5 (grid, componentes, utilidades)
- CSS3 + JS Vanilla
- jQuery (carrusel y modales)
- Font Awesome 6 (iconografía)
- Sin build step — todo es estático

## 📁 Estructura del Proyecto

```
electromecanico-en-santiago/
├── index.html                  # Página principal (hero + servicios + comunas + FAQ + CTA)
├── quienes-somos.html          # Sobre la empresa
├── contacto.html               # Formulario de contacto
├── faq.html                    # Preguntas frecuentes
├── servicios-domicilio.html    # Listado de servicios
├── inspeccion-mecanica.html    # Inspección técnica vehicular
├── politica-privacidad.html    # Política de privacidad
├── 404.html                    # Página no encontrada
├── servicios/                  # {total_servicios} landings de servicios específicos
├── comunas/                    # {total_comunas} landings por comuna (SEO local)
├── blog/                       # {total_blog} artículos de blog (SEO temático)
├── en/                         # Versión en inglés (mirror del sitio)
│   ├── comunas/
│   └── marcas_automotrices/
├── images/                     # Logo, banner, favicon, imágenes
├── css/styles.css              # Estilos globales
├── js/                         # Scripts (carrusel, modales, SEO)
├── sitemap.xml                 # {len(urls)-1} URLs indexables
├── robots.txt                  # {len(ai_bots)} user-agents IA permitidos
├── _redirects                  # Redirecciones 301 (Cloudflare Pages)
├── _headers                    # Cabeceras HTTP
└── favicon.jpg
```

## 📊 Estadísticas del sitio

| Sección | Cantidad |
|---------|----------|
| Páginas raíz | {len(root_html)} |
| Landings de servicios | {len(list(servicios_dir.glob('*.html'))) if servicios_dir.exists() else 0} |
| Landings por comuna | {len(list(comunas_dir.glob('*.html'))) if comunas_dir.exists() else 0} |
| Posts de blog | {len(list(blog_dir.glob('*.html'))) if blog_dir.exists() else 0} |
| Páginas en inglés | {len(list((ROOT/'en').glob('*.html'))) + len(list((ROOT/'en'/'comunas').glob('*.html'))) + len(list((ROOT/'en'/'marcas_automotrices').glob('*.html')))} |
| **Total páginas HTML** | **{total_html}** |

## 🎨 Identidad visual

- **Logo**: `images/electromecanico-a-domicilio-en-santiago-logo.jpg`
- **Banner**: `images/electromecanico-a-domicilio-en-santiago-banner.jpg`
- **Favicon**: `favicon.jpg`
- **Colores**:
  - Primary: `#0d7377` (azul petróleo)
  - Secondary: `#14a098` (turquesa)
  - Accent: `#ff6b35` (naranja CTA)

## 🚀 Deploy manual (Cloudflare Pages)

> **Importante**: El webhook GitHub → Cloudflare Pages no está conectado.
> Los `git push` NO disparan deploy automático. Hay que subir manualmente:

```bash
CLOUDFLARE_API_TOKEN=<token> \\
CLOUDFLARE_ACCOUNT_ID=6fc12c9a89723c0039cf189380c0b02f \\
npx wrangler@latest pages deploy . --project-name=electromecanico-en-santiago --branch=main
```

## 📝 SEO

- Sitemap autogenerado con {len(urls)-1} URLs (excluye 404)
- Robots.txt permite {len(ai_bots)} user-agents de IA (GPTBot, ClaudeBot, PerplexityBot, etc.)
- Redirecciones 301 de URLs con `.html` a URLs limpias
- Schema.org LocalBusiness en index.html
- 52 landings por comuna (SEO local)
- 31 landings de servicios (SEO temático)
- 61 posts de blog (SEO de contenido)
- Versión en inglés mirror

## 🔧 Mantenimiento

Para regenerar `sitemap.xml`, `robots.txt`, `_redirects` y este `README.md`:

```bash
python3 scripts/regenerate_seo.py
```

---

© Electromecánico en Santiago — Grupo 360 Soluciones
"""

(ROOT / "README.md").write_text(readme, encoding="utf-8")
print(f"README.md: {len(readme)} caracteres escritos")

print("\n✅ Todos los archivos regenerados:")
print(f"   - sitemap.xml ({len(urls)-1} URLs)")
print(f"   - robots.txt ({len(ai_bots)} bots IA)")
print(f"   - _redirects ({sum(1 for l in redirects_lines if ' 301' in l)} redirecciones)")
print(f"   - README.md (nuevo)")
