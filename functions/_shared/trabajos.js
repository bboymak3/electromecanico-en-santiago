// ============================================================
// "Trabajos Realizados" renderizados en el servidor (SEO)
// Los posts se publican desde el panel globalprov2.pages.dev y se leen de
// su API. Estas funciones arman el HTML que recibe Google (sin depender de
// JavaScript). js/trabajos-dinamicos.js solo agrega filtros y el modal.
// ============================================================
import { CONFIG } from './config.js';

export const API = 'https://globalprov2.pages.dev/api/admin/posts';
export const API_FOTO = 'https://globalprov2.pages.dev/api/public/post-foto';
export const URL_ES = '/trabajos-realizados';
export const URL_EN = '/en/completed-jobs';
export const CSS_HREF = '/css/trabajos-dinamicos.css';

export const COMUNAS = ('alhue buin calera-de-tango cerrillos cerro-navia colina conchali curacavi el-bosque el-monte ' +
  'estacion-central huechuraba independencia isla-de-maipo la-cisterna la-florida la-granja la-pintana la-reina lampa ' +
  'las-condes lo-barnechea lo-espejo lo-prado macul maipu maria-pinto melipilla nunoa padre-hurtado paine ' +
  'pedro-aguirre-cerda penaflor penalolen pirque providencia pudahuel puente-alto quilicura quinta-normal recoleta ' +
  'renca san-bernardo san-joaquin san-jose-de-maipo san-miguel san-pedro san-ramon santiago talagante tiltil vitacura').split(' ');

const T = {
  es: { verFicha: 'Ver ficha', nuevo: 'Reciente', titulo: 'Trabajos Realizados', tituloComuna: 'Trabajos realizados en ',
        sub: 'Fotos reales de vehículos atendidos a domicilio. Haz clic en cada vehículo para ver su ficha.',
        subComuna: 'Vehículos atendidos a domicilio por nuestro equipo en ', verTodos: 'Ver todos los trabajos realizados',
        inicio: 'Inicio', trabajo: 'Trabajo realizado', vehiculo: 'Vehículo', comuna: 'Comuna', fecha: 'Fecha',
        cotizar: 'Cotizar por WhatsApp', volver: 'Ver todos los trabajos realizados', otros: 'Otros trabajos en ',
        mas: 'Más trabajos realizados', servicioEn: 'Servicio a domicilio en ', fotos: 'Fotos del trabajo',
        foto: 'foto', aDomicilio: 'a domicilio en ' },
  en: { verFicha: 'View details', nuevo: 'Recent', titulo: 'Completed Jobs', tituloComuna: 'Completed jobs in ',
        sub: 'Real photos of vehicles serviced at home. Click any vehicle to see its details.',
        subComuna: 'Vehicles serviced at home by our team in ', verTodos: 'See all completed jobs',
        inicio: 'Home', trabajo: 'Work performed', vehiculo: 'Vehicle', comuna: 'Area', fecha: 'Date',
        cotizar: 'Get a quote on WhatsApp', volver: 'See all completed jobs', otros: 'Other jobs in ',
        mas: 'More completed jobs', servicioEn: 'Mobile service in ', fotos: 'Job photos',
        foto: 'photo', aDomicilio: 'at home in ' },
};
export const textos = lang => T[lang === 'en' ? 'en' : 'es'];

export function esc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

export function slug(s) {
  let out = String(s || '').toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  out = out.replace(/\u00f1/g, 'n').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  const alias = { 'til-til': 'tiltil', 'santiago-centro': 'santiago', 'pac': 'pedro-aguirre-cerda', 'est-central': 'estacion-central' };
  return alias[out] || out;
}

export const vehiculo = p => [p.marca, p.modelo, p.anio].filter(Boolean).join(' ');
export const postSlug = p => (slug(p.titulo || vehiculo(p) || 'trabajo').slice(0, 70).replace(/-+$/, '') || 'trabajo') + '-' + p.id;
export const urlDetalle = (p, lang) => (lang === 'en' ? URL_EN : URL_ES) + '/' + postSlug(p);
export const urlComuna = (c, lang) => {
  const s = slug(c);
  return COMUNAS.includes(s) ? (lang === 'en' ? '/en/comunas/' : '/comunas/') + s : '';
};

// /trabajos-realizados/fotos/<id>-<n>-<nombre-seo>.jpg (proxy en este mismo dominio)
export function urlFoto(p, n) {
  const meta = (p.fotos_meta || [])[n] || {};
  let nombre = slug(String(meta.nombre_archivo || '').replace(/\.[a-z0-9]+$/i, ''));
  if (!nombre) nombre = slug([vehiculo(p), p.comuna].filter(Boolean).join(' ')) || 'trabajo';
  return `${URL_ES}/fotos/${p.id}-${n}-${nombre.slice(0, 90)}.jpg`;
}
export const numFotos = p => (p.fotos_meta ? p.fotos_meta.length : (p.foto_count || 0));

export function altFoto(p, lang, n) {
  const t = textos(lang);
  const base = vehiculo(p) || p.titulo || '';
  return (base + (p.comuna ? ' – ' + (lang === 'en' ? CONFIG.servicio_en : CONFIG.servicio_es) + ' ' + (lang === 'en' ? 'in ' : 'en ') + p.comuna : '') +
    (n ? ' – ' + t.foto + ' ' + (n + 1) : '')).trim();
}

export function fechaBonita(f) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(f || ''));
  return m ? `${m[3]}-${m[2]}-${m[1]}` : String(f || '');
}
export function fechaISO(f) {
  const m = /^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}:\d{2}(?::\d{2})?))?/.exec(String(f || ''));
  return m ? (m[4] ? `${m[1]}-${m[2]}-${m[3]}T${m[4].length === 5 ? m[4] + ':00' : m[4]}-03:00` : `${m[1]}-${m[2]}-${m[3]}`) : undefined;
}

// Posts publicados para este sitio (caché de 5 minutos en el borde de Cloudflare)
export async function obtenerPosts() {
  const r = await fetch(`${API}?estado=publicado&sitio=${CONFIG.sitio}&limit=200`, {
    cf: { cacheTtl: 300, cacheEverything: true },
  });
  if (!r.ok) throw new Error('API ' + r.status);
  const d = await r.json();
  if (!d || !d.success || !Array.isArray(d.posts)) throw new Error('API sin posts');
  return d.posts;
}

export function tarjeta(p, lang, col, esNuevo) {
  const t = textos(lang);
  const n = numFotos(p);
  const titulo = p.titulo || vehiculo(p) || t.titulo;
  const desc = p.descripcion ? (p.descripcion.length > 140 ? p.descripcion.slice(0, 140) + '…' : p.descripcion) : '';
  let h = `<div class="${esc(col)}"><a class="td-card" href="${urlDetalle(p, lang)}" data-td-post="${esc(p.id)}">`;
  h += `<div class="td-img" id="td-img-${esc(p.id)}">`;
  h += n > 0 ? `<img src="${urlFoto(p, 0)}" alt="${esc(altFoto(p, lang, 0))}" loading="lazy" width="400" height="200">` : '<i class="fas fa-car"></i>';
  if (esNuevo) h += `<span class="td-new"><i class="fas fa-star me-1"></i>${t.nuevo}</span>`;
  if (n > 1) h += `<span class="td-count"><i class="fas fa-camera"></i> ${n}</span>`;
  h += `</div><div class="td-body"><h3>${esc(titulo)}</h3>`;
  if (desc) h += `<p>${esc(desc)}</p>`;
  h += `<p class="td-meta">${p.comuna ? `<i class="fas fa-map-marker-alt me-1"></i>${esc(p.comuna)} · ` : ''}${t.verFicha} <i class="fas fa-arrow-right ms-1"></i></p>`;
  h += '</div></a></div>';
  return h;
}

export const tarjetas = (posts, lang, col, conNuevo = true) =>
  posts.map((p, i) => tarjeta(p, lang, col, conNuevo && i < 3)).join('');

export function seccion(posts, lang, comunaNombre) {
  const t = textos(lang);
  const col = comunaNombre ? 'col-12 col-sm-6 col-lg-4' : 'col-12 col-sm-6 col-lg-3';
  return `<section class="py-5" style="background:#f0f4f8;" id="trabajos-dinamicos-seccion"><div class="container">` +
    `<div class="text-center mb-4"><h2 class="fw-bold" style="color:${CONFIG.color};font-size:2rem;"><i class="fas fa-camera me-2"></i>` +
    (comunaNombre ? t.tituloComuna + esc(comunaNombre) : t.titulo) + '</h2>' +
    `<p style="color:#666;max-width:640px;margin:0 auto;">${comunaNombre ? t.subComuna + esc(comunaNombre) + '.' : t.sub}</p></div>` +
    `<div class="row g-4 justify-content-center">${tarjetas(posts, lang, col)}</div>` +
    `<div class="text-center mt-4"><a href="${lang === 'en' ? URL_EN : URL_ES}" class="td-btn"><i class="fas fa-images me-2"></i>${t.verTodos}</a></div>` +
    '</div></section>';
}

export const headExtra = () =>
  `<link rel="stylesheet" href="${CSS_HREF}"><style>:root{--td-color:${CONFIG.color};}</style>`;

export function ldScript(obj) {
  return `<script type="application/ld+json">${JSON.stringify(obj).replace(/</g, '\\u003c')}</script>`;
}

export function itemListLD(posts, lang) {
  return {
    '@context': 'https://schema.org', '@type': 'ItemList',
    itemListElement: posts.map((p, i) => ({ '@type': 'ListItem', position: i + 1, url: CONFIG.site + urlDetalle(p, lang), name: p.titulo || vehiculo(p) })),
  };
}

// Respuesta HTML "segura": si algo falla se sirve la página estática tal cual
export function esHTML(res) {
  return res && res.status === 200 && (res.headers.get('Content-Type') || '').includes('text/html');
}
