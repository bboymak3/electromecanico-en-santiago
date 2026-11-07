/*
 * Trabajos realizados publicados desde el panel Global Pro (globalprov2.pages.dev)
 * con el sitio "electromecanico" seleccionado.
 *
 * Se usa en: index, /galeria, /trabajos-realizados, landings de comuna (ES y EN).
 * El mismo archivo sirve para electromecanico-en-santiago.pages.dev y globalpro.pages.dev.
 * Cada p\u00e1gina tiene un contenedor:
 *   <div id="trabajos-dinamicos" data-modo="home|galeria|comuna|landing" data-lang="es|en"
 *        data-comuna="maipu" data-target="#trabajos-realizados .row"
 *        data-sitio="electromecanico|globalpro" data-color="#0d7377" data-wa="56973622291"></div>
 * - modo "landing": p\u00e1gina dedicada con TODOS los trabajos publicados, filtro por comuna
 *   y bot\u00f3n "Ver m\u00e1s".
 * - Si existe el grid de data-target (trabajos est\u00e1ticos de la galer\u00eda), las
 *   tarjetas nuevas se agregan al inicio de ese grid.
 * - Si no existe, se crea una secci\u00f3n propia dentro del contenedor.
 * - Si no hay publicaciones, no se muestra nada.
 *
 * Insertado por scripts/add_trabajos_dinamicos.py
 */
(function () {
  'use strict';

  var API = 'https://globalprov2.pages.dev/api/admin/posts';
  var API_ORIGIN = 'https://globalprov2.pages.dev';

  var box = document.getElementById('trabajos-dinamicos');
  if (!box) return;

  var SITIO = box.getAttribute('data-sitio') || 'electromecanico';
  var COLOR = box.getAttribute('data-color') || '#0d7377';
  var WA = box.getAttribute('data-wa') || '56973622291';
  var POR_PAGINA = 12;

  var modo = box.getAttribute('data-modo') || 'home';
  var lang = box.getAttribute('data-lang') === 'en' ? 'en' : 'es';
  var comunaPagina = box.getAttribute('data-comuna') || '';
  var targetSel = box.getAttribute('data-target') || '';
  var LIMITE_HOME = 8;
  var URL_LANDING = lang === 'en' ? '/en/completed-jobs' : '/trabajos-realizados';
  var BASE_COMUNAS = lang === 'en' ? '/en/comunas/' : '/comunas/';
  // Comunas con landing propia (mismos slugs en ambos sitios)
  var COMUNAS_CON_PAGINA = ('alhue buin calera-de-tango cerrillos cerro-navia colina conchali curacavi el-bosque el-monte ' +
    'estacion-central huechuraba independencia isla-de-maipo la-cisterna la-florida la-granja la-pintana la-reina lampa ' +
    'las-condes lo-barnechea lo-espejo lo-prado macul maipu maria-pinto melipilla nunoa padre-hurtado paine ' +
    'pedro-aguirre-cerda penaflor penalolen pirque providencia pudahuel puente-alto quilicura quinta-normal recoleta ' +
    'renca san-bernardo san-joaquin san-jose-de-maipo san-miguel san-pedro san-ramon santiago talagante tiltil vitacura').split(' ');

  var T = {
    es: {
      titulo: 'Trabajos Realizados',
      tituloComuna: 'Trabajos realizados en ',
      sub: 'Fotos reales de veh\u00edculos atendidos a domicilio por nuestro electromec\u00e1nico. Haz clic en cada veh\u00edculo para ver su ficha.',
      subComuna: 'Veh\u00edculos atendidos a domicilio por nuestro electromec\u00e1nico en ',
      verFicha: 'Ver ficha',
      fotos: 'foto(s)',
      cargando: 'Cargando fotos...',
      error: 'No se pudo cargar el trabajo.',
      sinFotos: 'Sin fotos disponibles',
      fecha: 'Fecha',
      color: 'Color',
      trabajo: 'Trabajo realizado',
      cerrar: 'Cerrar',
      cotizar: 'Cotizar por WhatsApp',
      verGaleria: 'Ver todos los trabajos realizados',
      nuevo: 'Reciente',
      todas: 'Todas las comunas',
      verMas: 'Ver m\u00e1s trabajos',
      mostrando: 'Mostrando {n} de {t} trabajos',
      vacio: 'Pronto publicaremos aqu\u00ed nuevos trabajos realizados. \u00a1Escr\u00edbenos por WhatsApp y agenda tu servicio a domicilio!',
      verComuna: 'Servicio en ',
      filtrar: 'Filtrar por comuna'
    },
    en: {
      titulo: 'Completed Jobs',
      tituloComuna: 'Completed jobs in ',
      sub: 'Real photos of vehicles serviced at home by our mobile mechanic. Click any vehicle to see its details.',
      subComuna: 'Vehicles serviced at home by our mobile mechanic in ',
      verFicha: 'View details',
      fotos: 'photo(s)',
      cargando: 'Loading photos...',
      error: 'Could not load this job.',
      sinFotos: 'No photos available',
      fecha: 'Date',
      color: 'Color',
      trabajo: 'Work performed',
      cerrar: 'Close',
      cotizar: 'Get a quote on WhatsApp',
      verGaleria: 'See all completed jobs',
      nuevo: 'Recent',
      todas: 'All areas',
      verMas: 'Load more jobs',
      mostrando: 'Showing {n} of {t} jobs',
      vacio: 'New completed jobs will be published here soon. Message us on WhatsApp to book a mobile service!',
      verComuna: 'Service in ',
      filtrar: 'Filter by area'
    }
  }[lang];

  // ---------- utilidades ----------
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function slug(s) {
    var out = String(s || '').toLowerCase().trim();
    if (out.normalize) out = out.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    out = out.replace(/\u00f1/g, 'n').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    var alias = {
      'til-til': 'tiltil',
      'santiago-centro': 'santiago',
      'pac': 'pedro-aguirre-cerda',
      'est-central': 'estacion-central'
    };
    return alias[out] || out;
  }
  function fotoUrl(f) {
    var u = f && typeof f === 'object' ? (f.url || '') : (f || '');
    if (u.charAt(0) === '/') u = API_ORIGIN + u;
    return u;
  }
  function fetchTimeout(url, ms) {
    return Promise.race([
      fetch(url),
      new Promise(function (_, rej) { setTimeout(function () { rej(new Error('timeout')); }, ms); })
    ]).then(function (r) { return r.json(); });
  }
  function vehiculo(p) {
    return [p.marca, p.modelo, p.anio].filter(Boolean).join(' ');
  }

  // ---------- estilos (autocontenidos: las p\u00e1ginas EN no cargan galeria.css) ----------
  function inyectarEstilos() {
    if (document.getElementById('td-estilos')) return;
    var css = '' +
      '.td-card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,.08);cursor:pointer;transition:transform .3s,box-shadow .3s;height:100%;border-top:4px solid var(--td-color);}' +
      '.td-card:hover,.td-card:focus{transform:translateY(-5px);box-shadow:0 10px 28px rgba(0,0,0,.18);outline:none;}' +
      '.td-card .td-img{width:100%;height:200px;background:#e9eef2;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;}' +
      '.td-card .td-img img{width:100%;height:200px;object-fit:cover;display:block;}' +
      '.td-card .td-img i{font-size:2rem;color:#9fb3c0;}' +
      '.td-card .td-count{position:absolute;top:8px;right:8px;background:rgba(0,0,0,.65);color:#fff;font-size:.7rem;font-weight:700;border-radius:999px;padding:3px 9px;}' +
      '.td-card .td-new{position:absolute;top:8px;left:8px;background:var(--td-color);color:#fff;font-size:.68rem;font-weight:700;border-radius:999px;padding:3px 9px;}' +
      '.td-card .td-body{padding:14px 16px 16px;}' +
      '.td-card h3{font-size:1.05rem;font-weight:800;color:#1a1a1a;margin:0 0 4px;}' +
      '.td-card p{font-size:.85rem;color:#666;margin:0;}' +
      '.td-card .td-meta{margin-top:8px;font-weight:700;color:var(--td-color);font-size:.8rem;}' +
      '.td-modal-fotos{display:flex;gap:8px;overflow-x:auto;padding:10px 0;}' +
      '.td-modal-fotos img{width:64px;height:64px;object-fit:cover;border-radius:8px;cursor:pointer;border:2px solid transparent;flex-shrink:0;}' +
      '.td-modal-fotos img.activa{border-color:var(--td-color);}' +
      '.td-foto-principal{width:100%;max-height:440px;object-fit:contain;background:#000;border-radius:10px;display:block;}' +
      '.td-chip{display:inline-block;padding:3px 10px;border-radius:999px;font-size:.72rem;font-weight:700;background:#e6f4f4;color:var(--td-color);margin:2px;}' +
      '.td-fila{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid #eee;font-size:.88rem;}' +
      '.td-fila span:first-child{color:#888;white-space:nowrap;}' +
      '.td-fila span:last-child{color:#222;font-weight:600;text-align:right;}' +
      '.td-filtros{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:22px;}' +
      '.td-filtro{border:1px solid var(--td-color);background:#fff;color:var(--td-color);border-radius:999px;padding:6px 14px;font-size:.82rem;font-weight:700;cursor:pointer;}' +
      '.td-filtro.activo,.td-filtro:hover{background:var(--td-color);color:#fff;}' +
      '.td-filtro small{opacity:.75;margin-left:4px;}' +
      '.td-contador{text-align:center;color:#777;font-size:.85rem;margin:18px 0 8px;}' +
      '.td-btn{display:inline-block;background:var(--td-color);color:#fff !important;border:none;border-radius:999px;padding:10px 26px;font-weight:700;text-decoration:none;cursor:pointer;}' +
      '.td-btn:hover{filter:brightness(1.1);}' +
      '.td-vacio{text-align:center;color:#666;padding:40px 16px;max-width:560px;margin:0 auto;}' +
      '.td-vacio i{font-size:2.6rem;color:var(--td-color);margin-bottom:10px;display:block;}';
    var st = document.createElement('style');
    st.id = 'td-estilos';
    st.textContent = ':root{--td-color:' + COLOR + ';}' + css;
    document.head.appendChild(st);
  }

  // ---------- tarjeta ----------
  function tarjeta(p, colClass, esNuevo) {
    var fc = p.foto_count || (p.fotos || []).length || 0;
    var alt = (vehiculo(p) || p.titulo || '') + (p.comuna ? (lang === 'en' ? ' \u2013 mobile mechanic in ' : ' \u2013 electromec\u00e1nico a domicilio en ') + p.comuna : '');
    var h = '<div class="' + colClass + '">';
    h += '<div class="td-card" role="button" tabindex="0" data-td-post="' + esc(p.id) + '" aria-label="' + esc(p.titulo || vehiculo(p)) + '">';
    h += '<div class="td-img" id="td-img-' + esc(p.id) + '" data-alt="' + esc(alt) + '"><i class="fas fa-car"></i>';
    if (esNuevo) h += '<span class="td-new"><i class="fas fa-star me-1"></i>' + T.nuevo + '</span>';
    if (fc > 0) h += '<span class="td-count"><i class="fas fa-camera"></i> ' + fc + '</span>';
    h += '</div>';
    h += '<div class="td-body">';
    h += '<h3>' + esc(p.titulo || vehiculo(p) || T.titulo) + '</h3>';
    if (p.descripcion) h += '<p>' + esc(p.descripcion.length > 140 ? p.descripcion.substring(0, 140) + '\u2026' : p.descripcion) + '</p>';
    h += '<p class="td-meta">';
    if (p.comuna) h += '<i class="fas fa-map-marker-alt me-1"></i>' + esc(p.comuna) + ' \u00b7 ';
    h += T.verFicha + ' <i class="fas fa-arrow-right ms-1"></i></p>';
    h += '</div></div></div>';
    return h;
  }

  function ponerImagen(p, url) {
    var el = document.getElementById('td-img-' + p.id);
    if (!el || !url) return;
    var img = document.createElement('img');
    img.src = url;
    img.alt = el.getAttribute('data-alt') || '';
    img.loading = 'lazy';
    var icono = el.querySelector('i.fa-car');
    if (icono) icono.remove();
    el.insertBefore(img, el.firstChild);
  }

  function cargarPortadas(posts) {
    posts.forEach(function (p) {
      var directa = (p.fotos || [])[0];
      if (directa) { ponerImagen(p, fotoUrl(directa)); return; }
      if ((p.foto_count || 0) > 0) {
        fetchTimeout(API + '?id=' + encodeURIComponent(p.id), 8000).then(function (d) {
          if (d && d.success && d.post && d.post.fotos && d.post.fotos.length) ponerImagen(p, fotoUrl(d.post.fotos[0]));
        }).catch(function () {});
      }
    });
  }

  // ---------- modal ----------
  function asegurarModal() {
    var m = document.getElementById('td-modal');
    if (m) return m;
    m = document.createElement('div');
    m.id = 'td-modal';
    m.className = 'modal fade';
    m.tabIndex = -1;
    m.setAttribute('aria-hidden', 'true');
    m.innerHTML = '<div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable"><div class="modal-content">' +
      '<div class="modal-header" style="background:' + COLOR + ';color:#fff;"><h5 class="modal-title" id="td-modal-titulo"></h5>' +
      '<button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="' + T.cerrar + '"></button></div>' +
      '<div class="modal-body" id="td-modal-body"></div>' +
      '<div class="modal-footer"><a id="td-modal-comuna" class="btn fw-bold" style="display:none;border:1px solid ' + COLOR + ';color:' + COLOR + ';"></a>' +
      '<a class="btn fw-bold text-white" style="background:#25d366;" target="_blank" rel="noopener" href="https://wa.me/' + WA + '"><i class="fab fa-whatsapp me-1"></i>' + T.cotizar + '</a>' +
      '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">' + T.cerrar + '</button></div>' +
      '</div></div>';
    document.body.appendChild(m);
    m.addEventListener('click', function (ev) {
      var t = ev.target;
      if (t && t.getAttribute && t.getAttribute('data-td-foto')) {
        var principal = document.getElementById('td-foto-principal');
        if (principal) principal.src = t.getAttribute('data-td-foto');
        m.querySelectorAll('.td-modal-fotos img').forEach(function (i) { i.classList.toggle('activa', i === t); });
      }
    });
    return m;
  }

  function mostrarModal(m) {
    if (window.bootstrap && window.bootstrap.Modal) {
      window.bootstrap.Modal.getOrCreateInstance(m).show();
    } else {
      // Respaldo si Bootstrap a\u00fan no carg\u00f3
      m.style.display = 'block';
      m.classList.add('show');
      m.querySelectorAll('[data-bs-dismiss="modal"]').forEach(function (b) {
        b.onclick = function () { m.style.display = 'none'; m.classList.remove('show'); };
      });
    }
  }

  function abrirPost(id) {
    var m = asegurarModal();
    document.getElementById('td-modal-titulo').textContent = '';
    var body = document.getElementById('td-modal-body');
    var linkComuna = document.getElementById('td-modal-comuna');
    if (linkComuna) linkComuna.style.display = 'none';
    body.innerHTML = '<div class="text-center py-5 text-muted"><div class="spinner-border" style="color:' + COLOR + ';"></div><p class="mt-2">' + T.cargando + '</p></div>';
    mostrarModal(m);

    fetchTimeout(API + '?id=' + encodeURIComponent(id), 10000).then(function (d) {
      if (!d || !d.success || !d.post) throw new Error('sin datos');
      var p = d.post;
      var fotos = (p.fotos || []).map(fotoUrl).filter(Boolean);
      document.getElementById('td-modal-titulo').textContent = p.titulo || vehiculo(p);
      var sc = slug(p.comuna);
      if (linkComuna && modo !== 'comuna' && COMUNAS_CON_PAGINA.indexOf(sc) !== -1) {
        linkComuna.href = BASE_COMUNAS + sc;
        linkComuna.innerHTML = '<i class="fas fa-map-marker-alt me-1"></i>' + T.verComuna + esc(p.comuna);
        linkComuna.style.display = '';
      }
      var h = '<div class="text-center mb-2">';
      if (p.marca) h += '<span class="td-chip">' + esc(p.marca) + '</span>';
      if (p.modelo) h += '<span class="td-chip">' + esc(p.modelo) + '</span>';
      if (p.anio) h += '<span class="td-chip">' + esc(p.anio) + '</span>';
      if (p.comuna) h += '<span class="td-chip"><i class="fas fa-map-marker-alt me-1"></i>' + esc(p.comuna) + '</span>';
      h += '</div>';
      if (p.descripcion) h += '<p class="text-center text-muted">' + esc(p.descripcion).replace(/\n/g, '<br>') + '</p>';
      if (fotos.length) {
        var alt = esc((vehiculo(p) || p.titulo || '') + (p.comuna ? ' \u2013 ' + p.comuna : ''));
        h += '<img id="td-foto-principal" class="td-foto-principal" src="' + esc(fotos[0]) + '" alt="' + alt + '">';
        if (fotos.length > 1) {
          h += '<div class="td-modal-fotos">';
          fotos.forEach(function (u, i) {
            h += '<img src="' + esc(u) + '" data-td-foto="' + esc(u) + '" alt="' + alt + ' ' + (i + 1) + '" loading="lazy"' + (i === 0 ? ' class="activa"' : '') + '>';
          });
          h += '</div>';
        }
      } else {
        h += '<div class="text-center text-muted py-4"><i class="fas fa-images" style="font-size:2.5rem;"></i><p class="mt-2">' + T.sinFotos + '</p></div>';
      }
      h += '<div class="mt-3">';
      if (p.fecha_trabajo) h += '<div class="td-fila"><span><i class="far fa-calendar me-1"></i>' + T.fecha + '</span><span>' + esc(p.fecha_trabajo) + '</span></div>';
      if (p.color) h += '<div class="td-fila"><span><i class="fas fa-palette me-1"></i>' + T.color + '</span><span>' + esc(p.color) + '</span></div>';
      if (p.trabajo_realizado) {
        var t = p.trabajo_realizado.length > 400 ? p.trabajo_realizado.substring(0, 400) + '\u2026' : p.trabajo_realizado;
        h += '<div class="td-fila"><span><i class="fas fa-tools me-1"></i>' + T.trabajo + '</span><span>' + esc(t).replace(/\n/g, '<br>') + '</span></div>';
      }
      h += '</div>';
      body.innerHTML = h;
    }).catch(function () {
      body.innerHTML = '<div class="text-center text-muted py-5">' + T.error + '</div>';
    });
  }

  function activarClicks(root) {
    root.addEventListener('click', function (ev) {
      var card = ev.target.closest ? ev.target.closest('[data-td-post]') : null;
      if (card) abrirPost(card.getAttribute('data-td-post'));
    });
    root.addEventListener('keydown', function (ev) {
      if (ev.key !== 'Enter' && ev.key !== ' ') return;
      var card = ev.target.closest ? ev.target.closest('[data-td-post]') : null;
      if (card) { ev.preventDefault(); abrirPost(card.getAttribute('data-td-post')); }
    });
  }

  // ---------- render ----------
  // ---------- landing: todos los trabajos, filtro por comuna, paginaci\u00f3n ----------
  function renderLanding(posts) {
    inyectarEstilos();
    if (!posts.length) {
      box.innerHTML = '<div class="td-vacio"><i class="fas fa-tools"></i><p>' + T.vacio + '</p>' +
        '<a class="td-btn" style="background:#25d366;" target="_blank" rel="noopener" href="https://wa.me/' + WA + '"><i class="fab fa-whatsapp me-1"></i>' + T.cotizar + '</a></div>';
      return;
    }
    var comunas = {};
    posts.forEach(function (p) {
      var k = slug(p.comuna);
      if (!k) return;
      if (!comunas[k]) comunas[k] = { nombre: p.comuna, n: 0 };
      comunas[k].n++;
    });
    var claves = Object.keys(comunas).sort(function (a, b) { return comunas[b].n - comunas[a].n || a.localeCompare(b); });
    var filtro = '';
    try { filtro = slug(new URLSearchParams(location.search).get('comuna') || ''); } catch (e) {}
    if (filtro && !comunas[filtro]) filtro = '';
    var mostrados = POR_PAGINA;

    var h = '';
    if (claves.length > 1) {
      h += '<div class="td-filtros" role="group" aria-label="' + T.filtrar + '">';
      h += '<button type="button" class="td-filtro" data-td-filtro="">' + T.todas + '<small>(' + posts.length + ')</small></button>';
      claves.forEach(function (k) {
        h += '<button type="button" class="td-filtro" data-td-filtro="' + esc(k) + '"><i class="fas fa-map-marker-alt me-1"></i>' + esc(comunas[k].nombre) + '<small>(' + comunas[k].n + ')</small></button>';
      });
      h += '</div>';
    }
    h += '<div class="row g-4" id="td-grid"></div>';
    h += '<p class="td-contador" id="td-contador"></p>';
    h += '<div class="text-center"><button type="button" class="td-btn" id="td-ver-mas" style="display:none;">' + T.verMas + ' <i class="fas fa-chevron-down ms-1"></i></button></div>';
    box.innerHTML = h;
    var grid = document.getElementById('td-grid');
    activarClicks(grid);

    function pintar() {
      var lista = filtro ? posts.filter(function (p) { return slug(p.comuna) === filtro; }) : posts;
      var visibles = lista.slice(0, mostrados);
      grid.innerHTML = visibles.map(function (p, i) { return tarjeta(p, 'col-12 col-sm-6 col-lg-4 col-xl-3', !filtro && i < 3); }).join('');
      cargarPortadas(visibles);
      document.getElementById('td-contador').textContent = T.mostrando.replace('{n}', visibles.length).replace('{t}', lista.length);
      document.getElementById('td-ver-mas').style.display = lista.length > visibles.length ? '' : 'none';
      box.querySelectorAll('[data-td-filtro]').forEach(function (b) {
        var activo = b.getAttribute('data-td-filtro') === filtro;
        b.classList.toggle('activo', activo);
        b.setAttribute('aria-pressed', activo ? 'true' : 'false');
      });
    }
    box.addEventListener('click', function (ev) {
      var b = ev.target.closest ? ev.target.closest('[data-td-filtro]') : null;
      if (b) {
        filtro = b.getAttribute('data-td-filtro');
        mostrados = POR_PAGINA;
        try {
          var u = new URL(location.href);
          if (filtro) u.searchParams.set('comuna', filtro); else u.searchParams.delete('comuna');
          history.replaceState(null, '', u.toString());
        } catch (e) {}
        pintar();
        return;
      }
      if (ev.target.closest && ev.target.closest('#td-ver-mas')) {
        mostrados += POR_PAGINA;
        pintar();
      }
    });
    pintar();
  }

  function render(posts) {
    if (modo === 'landing') { renderLanding(posts); return; }
    if (modo === 'comuna') {
      var objetivo = slug(comunaPagina);
      posts = posts.filter(function (p) { return slug(p.comuna) === objetivo; });
    } else if (modo === 'home') {
      posts = posts.slice(0, LIMITE_HOME);
    }
    if (!posts.length) return;

    inyectarEstilos();
    var grid = targetSel ? document.querySelector(targetSel) : null;
    var col = modo === 'comuna' ? 'col-12 col-sm-6 col-lg-4' : 'col-12 col-sm-6 col-lg-3';

    if (grid) {
      // Se agregan al inicio del grid existente de trabajos realizados
      var colGrid = (grid.firstElementChild && grid.firstElementChild.className) || col;
      var html = posts.map(function (p, i) { return tarjeta(p, colGrid, i < 3); }).join('');
      grid.insertAdjacentHTML('afterbegin', html);
      activarClicks(grid);
      // Si la secci\u00f3n estaba oculta (sin trabajos est\u00e1ticos), mostrarla
      var sec = grid.closest ? grid.closest('section') : null;
      if (sec) sec.style.display = '';
    } else {
      var nombre = modo === 'comuna' ? posts[0].comuna : '';
      var h = '<section class="py-5" style="background:#f0f4f8;" id="trabajos-dinamicos-seccion"><div class="container">';
      h += '<div class="text-center mb-4"><h2 class="fw-bold" style="color:' + COLOR + ';font-size:2rem;"><i class="fas fa-camera me-2"></i>' +
        (modo === 'comuna' ? T.tituloComuna + esc(nombre) : T.titulo) + '</h2>';
      h += '<p style="color:#666;max-width:640px;margin:0 auto;">' + (modo === 'comuna' ? T.subComuna + esc(nombre) + '.' : T.sub) + '</p></div>';
      h += '<div class="row g-4 justify-content-center">' + posts.map(function (p, i) { return tarjeta(p, col, i < 3); }).join('') + '</div>';
      h += '<div class="text-center mt-4"><a href="' + URL_LANDING + '" class="td-btn"><i class="fas fa-images me-2"></i>' + T.verGaleria + '</a></div>';
      h += '</div></section>';
      box.innerHTML = h;
      activarClicks(box);
    }
    cargarPortadas(posts);
  }

  fetchTimeout(API + '?estado=publicado&sitio=' + SITIO + '&limit=200', 10000)
    .then(function (d) {
      if (d && d.success && Array.isArray(d.posts)) render(d.posts);
      else if (modo === 'landing') render([]);
    })
    .catch(function () {
      // sin conexi\u00f3n con el panel: en las dem\u00e1s p\u00e1ginas se muestran solo los trabajos est\u00e1ticos
      if (modo === 'landing') render([]);
    });
})();
