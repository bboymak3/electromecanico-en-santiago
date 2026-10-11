// Lightbox de la galería de trabajos realizados.
// Cada foto es un elemento .gal-item con data-full, data-caption y data-group;
// las flechas recorren solo las fotos visibles del mismo grupo.
(function(){
  var lb, img, cap, list = [], idx = 0;

  function build(){
    lb = document.createElement('div');
    lb.id = 'galLightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<button class="gl-btn gl-close" aria-label="Cerrar">&times;</button>' +
      '<button class="gl-btn gl-prev" aria-label="Anterior">&#10094;</button>' +
      '<button class="gl-btn gl-next" aria-label="Siguiente">&#10095;</button>' +
      '<div><img alt=""><p></p></div>';
    document.body.appendChild(lb);
    img = lb.querySelector('img');
    cap = lb.querySelector('p');
    lb.querySelector('.gl-close').onclick = close;
    lb.querySelector('.gl-prev').onclick = function(){ show(idx - 1); };
    lb.querySelector('.gl-next').onclick = function(){ show(idx + 1); };
    lb.addEventListener('click', function(e){ if (e.target === lb) close(); });
  }

  function show(i){
    idx = (i + list.length) % list.length;
    img.src = list[idx].getAttribute('data-full');
    img.alt = list[idx].querySelector('img').alt;
    cap.textContent = list[idx].getAttribute('data-caption');
  }

  function close(){
    lb.classList.remove('open');
    if (!document.querySelector('.modal.show')) document.body.style.overflow = '';
  }

  document.addEventListener('click', function(e){
    var item = e.target.closest('.gal-item');
    if (!item) return;
    e.preventDefault();
    if (!lb) build();
    var group = item.getAttribute('data-group');
    list = Array.prototype.filter.call(
      document.querySelectorAll('.gal-item[data-group="' + group + '"]'),
      function(el){ return el.offsetParent !== null; }
    );
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
    show(Math.max(0, list.indexOf(item)));
  });

  document.addEventListener('keydown', function(e){
    if (!lb || !lb.classList.contains('open')) return;
    if (e.key === 'Escape') { e.stopPropagation(); close(); }
    if (e.key === 'ArrowRight') show(idx + 1);
    if (e.key === 'ArrowLeft') show(idx - 1);
  }, true);

  // Filtros por vehículo
  document.addEventListener('click', function(e){
    var btn = e.target.closest('.gal-filters button');
    if (!btn) return;
    var wrap = btn.closest('[data-gal-scope]');
    var f = btn.getAttribute('data-filter');
    wrap.querySelectorAll('.gal-filters button').forEach(function(b){ b.classList.toggle('active', b === btn); });
    wrap.querySelectorAll('.gal-grid .gal-item').forEach(function(el){
      el.style.display = (f === 'all' || el.getAttribute('data-veh') === f) ? '' : 'none';
    });
  });
})();
