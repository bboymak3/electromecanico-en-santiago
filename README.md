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
- Bootstrap 5 (grid, componentes, modales)
- CSS3 + JS Vanilla
- Skin visual tipo iPhone (iOS) en todo el sitio: `css/ios-skin.css`
- Font Awesome 6 (iconografía)
- Sin build step — todo es estático (los scripts de `scripts/` generan HTML y se versiona el resultado)

## 📁 Estructura del Proyecto

```
electromecanico-en-santiago/
├── index.html                  # Página principal (hero, valor estándar, instalaciones, servicios, galería, trabajos realizados, comunas, FAQ)
├── galeria.html                # Galería de trabajos realizados (fotos + fichas de vehículos)
├── quienes-somos.html          # Sobre la empresa
├── contacto.html               # Contacto
├── faq.html                    # Preguntas frecuentes
├── servicios-domicilio.html    # Listado de servicios
├── inspeccion-mecanica.html    # Inspección técnica vehicular
├── politica-privacidad.html    # Política de privacidad
├── 404.html                    # Página no encontrada
├── servicios/                  # 69 landings de servicios (incluye 6 de valor estándar, 18 instalaciones y el hub instalaciones-automotrices)
├── comunas/                    # 52 landings por comuna (SEO local)
├── blog/                       # 61 artículos de blog (SEO temático)
├── vehiculos/                  # 33 páginas por modelo de vehículo
├── marcas_automotrices/        # 10 páginas por marca/modelo
├── en/                         # 110 páginas en inglés
├── images/                     # Logo, banner, favicon, imágenes
│   └── galeria/                # Fotos de trabajos realizados (nombres SEO + comuna) y miniaturas
├── css/
│   ├── styles.css              # Estilos globales
│   ├── galeria.css             # Galería, fichas y lightbox
│   └── ios-skin.css            # Skin tipo iPhone
├── js/galeria.js               # Lightbox, filtros y botón "Ver más" de la galería
├── scripts/                    # Generadores (ver Mantenimiento)
├── sitemap.xml                 # 339 URLs indexables (+ imágenes de la galería)
├── robots.txt
├── _redirects                  # Redirecciones 301 (Cloudflare Pages)
├── _headers                    # Cabeceras HTTP
└── favicon.jpg
```

## 📊 Estadísticas del sitio

| Sección | Cantidad |
|---------|----------|
| Páginas raíz (incluye galería y 404) | 9 |
| Landings de servicios (`servicios/`) | 69 |
| Landings por comuna (`comunas/`) | 52 |
| Posts de blog (`blog/`) | 61 |
| Páginas de vehículos (`vehiculos/`) | 33 |
| Páginas de marcas (`marcas_automotrices/`) | 10 |
| **Total páginas en español** | **234** |
| Páginas en inglés (`en/`) | 110 |
| **Total páginas HTML** | **344** |
| URLs en `sitemap.xml` | 339 |

*No incluye `google7a5c4682e9b25d4f.html` (verificación de Google Search Console). Conteo al 2026-10-11.*

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

- `sitemap.xml` con 339 URLs (todas las páginas indexables, incluye vehículos, marcas e inglés) y fotos de la galería como `image:image`
- Al compartir cualquier enlace (WhatsApp, Facebook, X, LinkedIn) se muestra el logo: `images/electromecanico-a-domicilio-en-santiago-logo-og.jpg` (1200×630)
- Canónicas: cada página apunta a su propia URL limpia
- Robots.txt permite user-agents de IA (GPTBot, ClaudeBot, PerplexityBot, etc.)
- Redirecciones 301 de URLs con `.html` a URLs limpias
- Schema.org en todas las páginas: AutoRepair/LocalBusiness con logo, WebSite, WebPage y BreadcrumbList; FAQPage en el index; Service + FAQPage en las landings de servicios; ImageGallery en la galería
- 52 landings por comuna (SEO local) y 69 landings de servicios (SEO temático)
- 61 posts de blog (SEO de contenido)
- Fotos de la galería con nombres de palabras clave separadas por `-` y la comuna al final
- Versión en inglés

## 🔧 Mantenimiento

Todos los scripts son idempotentes (se pueden ejecutar varias veces sin duplicar nada):

| Script | Qué hace | Datos |
|--------|----------|-------|
| `python3 scripts/build_galeria.py` | Regenera `galeria.html`, la grilla de fotos, la sección "Trabajos Realizados" y las fichas modales del index | `scripts/galeria_data.json` |
| `python3 scripts/build_landings_servicios.py` | Regenera las landings de valor estándar e instalaciones, el hub, sus secciones/modales en el index y el sitemap | `scripts/landings_data.json` |
| `python3 scripts/fix_servicios_en_blanco.py` | Regenera el bloque de contexto (señales, FAQ, relacionados) de 24 páginas de servicios | `scripts/servicios_contexto.json` |
| `python3 scripts/add_ios_skin.py` | Enlaza `css/ios-skin.css` en páginas nuevas | — |
| `python3 scripts/seo_social_schema.py` | Imagen del logo al compartir, canónicas, datos estructurados (@graph) y `sitemap.xml` completo | — |

**Orden recomendado después de cambios:** ejecuta primero el script que corresponda (galería, landings, contexto) y al final `seo_social_schema.py`, para que las páginas regeneradas recuperen sus metadatos y el sitemap quede completo.

**Agregar un vehículo a la galería:** copia la foto a `images/galeria/` con nombre `palabras-clave-separadas-con-guion-comuna.jpg` (+ versión `-thumb.jpg`), agrega la entrada en `scripts/galeria_data.json` y ejecuta `build_galeria.py`.

> ⚠️ `scripts/regenerate_seo_electromecanico.py` reescribe `sitemap.xml`, `robots.txt`, `_redirects` **y este README** desde cero. Si lo ejecutas, revisa que el sitemap conserve `/galeria` y las landings nuevas, y vuelve a aplicar estos cambios al README.

---

© Electromecánico en Santiago — Grupo 360 Soluciones
