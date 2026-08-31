# Electromecánico en Santiago

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
├── servicios/                  # 31 landings de servicios específicos
├── comunas/                    # 52 landings por comuna (SEO local)
├── blog/                       # 61 artículos de blog (SEO temático)
├── en/                         # Versión en inglés (mirror del sitio)
│   ├── comunas/
│   └── marcas_automotrices/
├── images/                     # Logo, banner, favicon, imágenes
├── css/styles.css              # Estilos globales
├── js/                         # Scripts (carrusel, modales, SEO)
├── sitemap.xml                 # 220 URLs indexables
├── robots.txt                  # 30 user-agents IA permitidos
├── _redirects                  # Redirecciones 301 (Cloudflare Pages)
├── _headers                    # Cabeceras HTTP
└── favicon.jpg
```

## 📊 Estadísticas del sitio

| Sección | Cantidad |
|---------|----------|
| Páginas raíz | 7 |
| Landings de servicios | 31 |
| Landings por comuna | 52 |
| Posts de blog | 61 |
| Páginas en inglés | 70 |
| **Total páginas HTML** | **223** |

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
CLOUDFLARE_API_TOKEN=<token> \
CLOUDFLARE_ACCOUNT_ID=6fc12c9a89723c0039cf189380c0b02f \
npx wrangler@latest pages deploy . --project-name=electromecanico-en-santiago --branch=main
```

## 📝 SEO

- Sitemap autogenerado con 220 URLs (excluye 404)
- Robots.txt permite 30 user-agents de IA (GPTBot, ClaudeBot, PerplexityBot, etc.)
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
