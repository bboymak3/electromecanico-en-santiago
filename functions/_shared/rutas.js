// Manejadores reutilizables de las Pages Functions de "Trabajos Realizados".
import { CONFIG } from './config.js';
import {
  URL_ES, URL_EN, API_FOTO, obtenerPosts, tarjetas, seccion, headExtra, ldScript, itemListLD, esHTML,
  textos, esc, slug, vehiculo, postSlug, urlDetalle, urlComuna, urlFoto, numFotos, altFoto, fechaBonita, fechaISO, absoluta,
} from './trabajos.js';

const quitarHtml = (request, sufijo = '.html') => {
  const u = new URL(request.url);
  if (u.pathname.endsWith(sufijo) || (u.pathname.length > 1 && u.pathname.endsWith('/') && sufijo === '/')) {
    u.pathname = u.pathname.slice(0, -sufijo.length) || '/';
    return Response.redirect(u.toString(), 301);
  }
  return null;
};

async function noEncontrado(context) {
  const r = await context.env.ASSETS.fetch(new URL('/404', context.request.url));
  return new Response(r.body, { status: 404, headers: r.headers });
}

// /comunas/maipu.html -> /comunas/maipu (las Functions no aplican _redirects)
export function redirigirHtml(context) {
  return quitarHtml(context.request);
}

async function postsOVacio() {
  try { return await obtenerPosts(); } catch (e) { return null; }
}

// ---------------------------------------------------------------- landing
export async function landing(context, lang) {
  const red = quitarHtml(context.request);
  if (red) return red;
  const res = await context.next();
  if (!esHTML(res)) return res;
  const posts = await postsOVacio();
  if (!posts || !posts.length) return res;
  return new HTMLRewriter()
    .on('head', { element(el) { el.append(headExtra() + ldScript(itemListLD(posts, lang)), { html: true }); } })
    .on('#trabajos-dinamicos', {
      element(el) {
        el.setAttribute('data-ssr', '1');
        el.setInnerContent(`<div class="row g-4">${tarjetas(posts, lang, 'col-12 col-sm-6 col-lg-4 col-xl-3')}</div>`, { html: true });
      },
    })
    .transform(res);
}

// ---------------------------------------------------------------- páginas con sección (home, galería, comunas)
// opts: { lang, modo: 'home'|'galeria'|'comuna', comuna (slug), grid (selector del grid estático), limite }
export async function conSeccion(context, opts) {
  const res = await context.next();
  if (!esHTML(res)) return res;
  let posts = await postsOVacio();
  if (!posts) return res;
  const lang = opts.lang || 'es';
  if (opts.modo === 'comuna') posts = posts.filter(p => slug(p.comuna) === opts.comuna);
  if (opts.limite) posts = posts.slice(0, opts.limite);
  if (!posts.length) return res;

  let gridHecho = false;
  const rw = new HTMLRewriter()
    .on('head', { element(el) { el.append(headExtra(), { html: true }); } });
  if (opts.grid) {
    rw.on(opts.grid, {
      element(el) {
        if (gridHecho) return;
        gridHecho = true;
        const col = opts.modo === 'comuna' ? 'col-12 col-sm-6 col-lg-4' : 'col-12 col-sm-6 col-lg-3';
        el.prepend(tarjetas(posts, lang, col), { html: true });
      },
    });
  }
  rw.on('#trabajos-dinamicos', {
    element(el) {
      el.setAttribute('data-ssr', '1');
      // En home/galería el grid estático viene DESPUÉS del contenedor: las tarjetas van ahí.
      const gridDespues = opts.grid && (opts.modo === 'home' || opts.modo === 'galeria');
      if (gridHecho || gridDespues) return;
      el.setInnerContent(seccion(posts, lang, opts.modo === 'comuna' ? posts[0].comuna : ''), { html: true });
    },
  });
  if (opts.globalproGrid) {
    // Globalpro: sección "Trabajos Realizados en <comuna>" con su propio grid
    rw.on('#trabajos-realizados-comuna', { element(el) { el.setAttribute('style', (el.getAttribute('style') || '').replace(/display\s*:\s*none;?/i, '')); } })
      .on('#grid-trabajos-comuna', {
        element(el) {
          el.setAttribute('data-ssr', '1');
          el.setInnerContent(tarjetas(posts, lang, 'col-12 col-sm-6 col-lg-4'), { html: true });
        },
      });
  }
  return rw.transform(res);
}

// ---------------------------------------------------------------- ficha de un trabajo
export async function detalle(context, lang) {
  const { request, params, env } = context;
  const t = textos(lang);
  const base = lang === 'en' ? URL_EN : URL_ES;
  const s = String(params.slug || '').replace(/\.html$/, '');
  const m = /-(\d+)$/.exec(s) || /^(\d+)$/.exec(s);
  if (!m) return context.next();
  const id = Number(m[1]);

  const posts = await postsOVacio();
  if (!posts) return new Response('Servicio no disponible, intenta en unos minutos.', { status: 503, headers: { 'Retry-After': '120' } });
  const p = posts.find(x => Number(x.id) === id);
  if (!p) return noEncontrado(context);

  const canon = postSlug(p);
  if (s !== canon) return Response.redirect(new URL(`${base}/${canon}`, request.url).toString(), 301);

  const shell = await env.ASSETS.fetch(new URL(base, request.url));
  if (!esHTML(shell)) return shell;

  const url = CONFIG.site + urlDetalle(p, lang);
  const urlOtro = CONFIG.site + urlDetalle(p, lang === 'en' ? 'es' : 'en');
  const urlEs = CONFIG.site + urlDetalle(p, 'es');
  const veh = vehiculo(p);
  const titulo = p.titulo || veh || t.titulo;
  const title = `${titulo} | ${t.titulo} – ${CONFIG.marca}`;
  let desc = (p.descripcion || p.trabajo_realizado || `${veh} ${t.aDomicilio}${p.comuna || 'Santiago'}`).replace(/\s+/g, ' ').trim();
  if (desc.length > 158) desc = desc.slice(0, 155).replace(/\s+\S*$/, '') + '…';
  const n = numFotos(p);
  const fotos = Array.from({ length: n }, (_, i) => urlFoto(p, i));
  const fotosAbs = fotos.filter(Boolean).map(absoluta);
  const comunaUrl = p.comuna ? urlComuna(p.comuna, lang) : '';

  // ---- contenido
  let h = '<div class="container" style="max-width:980px;"><article class="td-detalle">';
  h += '<div class="text-center mb-3">';
  if (p.marca) h += `<span class="td-chip">${esc(p.marca)}</span>`;
  if (p.modelo) h += `<span class="td-chip">${esc(p.modelo)}</span>`;
  if (p.anio) h += `<span class="td-chip">${esc(p.anio)}</span>`;
  if (p.comuna) h += comunaUrl ? `<a class="td-chip" href="${comunaUrl}"><i class="fas fa-map-marker-alt me-1"></i>${esc(p.comuna)}</a>` : `<span class="td-chip"><i class="fas fa-map-marker-alt me-1"></i>${esc(p.comuna)}</span>`;
  h += '</div>';
  if (p.descripcion) h += `<p class="lead text-center" style="color:#444;">${esc(p.descripcion)}</p>`;
  if (n) {
    h += `<h2 class="h5 fw-bold mt-4 mb-3">${t.fotos}</h2><div class="td-galeria">`;
    fotos.forEach((f, i) => {
      h += `<a href="${f}" target="_blank" rel="noopener" class="${i === 0 ? 'td-galeria-principal' : ''}"><img src="${f}" alt="${esc(altFoto(p, lang, i))}" ${i === 0 ? 'fetchpriority="high"' : 'loading="lazy"'} width="800" height="600"></a>`;
    });
    h += '</div>';
  }
  h += '<div class="row g-4 mt-2"><div class="col-md-7">';
  if (p.trabajo_realizado) h += `<h2 class="h5 fw-bold">${t.trabajo}</h2><p style="white-space:pre-line;color:#333;">${esc(p.trabajo_realizado)}</p>`;
  h += '</div><div class="col-md-5"><div class="p-3 rounded-3 bg-white">';
  if (veh) h += `<div class="td-fila"><span>${t.vehiculo}</span><span>${esc(veh)}${p.color ? ' · ' + esc(p.color) : ''}</span></div>`;
  if (p.comuna) h += `<div class="td-fila"><span>${t.comuna}</span><span>${comunaUrl ? `<a href="${comunaUrl}">${esc(p.comuna)}</a>` : esc(p.comuna)}</span></div>`;
  if (p.fecha_trabajo) h += `<div class="td-fila"><span>${t.fecha}</span><span>${esc(fechaBonita(p.fecha_trabajo))}</span></div>`;
  h += `<div class="d-grid gap-2 mt-3"><a class="td-btn text-center" style="background:#25d366;" target="_blank" rel="noopener" href="https://wa.me/${CONFIG.wa}?text=${encodeURIComponent((lang === 'en' ? 'Hi, I saw this job: ' : 'Hola, vi este trabajo: ') + titulo)}"><i class="fab fa-whatsapp me-1"></i>${t.cotizar}</a>`;
  if (comunaUrl) h += `<a class="btn btn-outline-secondary fw-bold" href="${comunaUrl}"><i class="fas fa-map-marker-alt me-1"></i>${t.servicioEn}${esc(p.comuna)}</a>`;
  h += '</div></div></div></div></article>';

  const mismos = posts.filter(x => x.id !== p.id && p.comuna && slug(x.comuna) === slug(p.comuna));
  const otros = (mismos.length ? mismos : posts.filter(x => x.id !== p.id)).slice(0, 4);
  if (otros.length) {
    h += `<h2 class="h4 fw-bold text-center mt-5 mb-4" style="color:${CONFIG.color};">${mismos.length ? t.otros + esc(p.comuna) : t.mas}</h2>`;
    h += `<div class="row g-4 justify-content-center">${tarjetas(otros, lang, 'col-12 col-sm-6 col-lg-3', false)}</div>`;
  }
  h += `<div class="text-center mt-4"><a href="${base}" class="td-btn"><i class="fas fa-images me-2"></i>${t.volver}</a></div></div>`;

  const ld = [
    {
      '@context': 'https://schema.org', '@type': 'Article', headline: titulo.slice(0, 110), description: desc,
      image: fotosAbs.length ? fotosAbs : undefined, inLanguage: lang,
      datePublished: fechaISO(p.fecha_publicacion || p.fecha_trabajo), dateModified: fechaISO(p.fecha_publicacion || p.fecha_trabajo),
      mainEntityOfPage: url,
      author: { '@type': 'Organization', name: CONFIG.marca, url: CONFIG.site },
      publisher: { '@type': 'Organization', name: CONFIG.marca, url: CONFIG.site },
      about: { '@type': 'Service', serviceType: lang === 'en' ? CONFIG.servicio_en : CONFIG.servicio_es, provider: { '@type': 'LocalBusiness', name: CONFIG.marca, telephone: '+' + CONFIG.wa, url: CONFIG.site }, areaServed: p.comuna ? { '@type': 'City', name: p.comuna } : undefined },
    },
    {
      '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: t.inicio, item: CONFIG.site + (lang === 'en' ? '/en/' : '/') },
        { '@type': 'ListItem', position: 2, name: t.titulo, item: CONFIG.site + base },
        { '@type': 'ListItem', position: 3, name: titulo, item: url },
      ],
    },
  ];

  const ogImg = fotosAbs[0];
  const res = new HTMLRewriter()
    .on('title', { element(el) { el.setInnerContent(title); } })
    .on('meta[name="description"]', { element(el) { el.setAttribute('content', desc); } })
    .on('meta[property="og:title"], meta[name="twitter:title"]', { element(el) { el.setAttribute('content', title); } })
    .on('meta[property="og:description"], meta[name="twitter:description"]', { element(el) { el.setAttribute('content', desc); } })
    .on('meta[property="og:url"]', { element(el) { el.setAttribute('content', url); } })
    .on('meta[property="og:type"]', { element(el) { el.setAttribute('content', 'article'); } })
    .on('meta[property="og:image"], meta[name="twitter:image"]', { element(el) { if (ogImg) el.setAttribute('content', ogImg); } })
    .on('link[rel="canonical"]', { element(el) { el.setAttribute('href', url); } })
    .on('link[rel="alternate"][hreflang]', { element(el) { el.remove(); } })
    .on('script[type="application/ld+json"]', { element(el) { el.remove(); } })
    .on('head', {
      element(el) {
        el.append(headExtra() +
          `<link rel="alternate" hreflang="${lang}" href="${url}"><link rel="alternate" hreflang="${lang === 'en' ? 'es' : 'en'}" href="${urlOtro}"><link rel="alternate" hreflang="x-default" href="${urlEs}">` +
          ldScript(ld), { html: true });
      },
    })
    .on('.page-hero h1', { element(el) { el.setInnerContent(`<i class="fas fa-tools me-3"></i>${esc(titulo)}`, { html: true }); } })
    .on('.page-hero p', { element(el) { el.setInnerContent(esc([veh, p.comuna].filter(Boolean).join(' · ') || t.titulo)); } })
    .on('.page-hero .breadcrumb', {
      element(el) {
        el.setInnerContent(`<li class="breadcrumb-item"><a href="${lang === 'en' ? '/en/' : '/'}">${t.inicio}</a></li>` +
          `<li class="breadcrumb-item"><a href="${base}">${t.titulo}</a></li>` +
          `<li class="breadcrumb-item active" aria-current="page">${esc(titulo.length > 50 ? titulo.slice(0, 50) + '…' : titulo)}</li>`, { html: true });
      },
    })
    .on(`a[href="${lang === 'en' ? URL_ES : URL_EN}"]`, { element(el) { el.setAttribute('href', urlDetalle(p, lang === 'en' ? 'es' : 'en')); } })
    .on('#trabajos-realizados-landing', { element(el) { el.setInnerContent(h, { html: true }); } })
    .transform(shell);
  const headers = new Headers(res.headers);
  headers.set('Cache-Control', 'public, max-age=300');
  return new Response(res.body, { status: 200, headers });
}

// ---------------------------------------------------------------- fotos con nombre SEO en el propio dominio
export async function foto(context) {
  const m = /^(\d+)-(\d+)(?:-[a-z0-9-]*)?\.jpe?g$/i.exec(String(context.params.foto || ''));
  if (!m) return new Response('No encontrado', { status: 404 });
  const r = await fetch(`${API_FOTO}?id=${m[1]}&n=${m[2]}`, { cf: { cacheTtl: 604800, cacheEverything: true } });
  if (!r.ok) return new Response('No encontrado', { status: 404 });
  const h = new Headers();
  h.set('Content-Type', r.headers.get('Content-Type') || 'image/jpeg');
  h.set('Cache-Control', 'public, max-age=86400, s-maxage=604800');
  return new Response(r.body, { headers: h });
}

// ---------------------------------------------------------------- sitemap
export async function sitemap(context) {
  const res = await context.next();
  if (res.status !== 200) return res;
  let xml = await res.text();
  const posts = await postsOVacio();
  if (posts && posts.length) {
    if (!xml.includes('xmlns:image=')) xml = xml.replace('<urlset ', '<urlset xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" ');
    const x = s => esc(s);
    const urls = posts.map(p => {
      const lm = fechaISO(p.fecha_publicacion || p.fecha_trabajo);
      const imgs = Array.from({ length: numFotos(p) }, (_, i) =>
        `<image:image><image:loc>${x(absoluta(urlFoto(p, i)))}</image:loc><image:title>${x(altFoto(p, 'es', i))}</image:title></image:image>`).join('');
      return ['es', 'en'].map(l =>
        `  <url><loc>${x(CONFIG.site + urlDetalle(p, l))}</loc>${lm ? `<lastmod>${lm.slice(0, 10)}</lastmod>` : ''}<changefreq>monthly</changefreq><priority>0.6</priority>${l === 'es' ? imgs : ''}</url>\n`).join('');
    }).join('');
    xml = xml.replace('</urlset>', urls + '</urlset>');
  }
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } });
}
