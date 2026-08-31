import os
import re
import glob

# ============================================================
# TAPIZADO DE VOLANTES - Template para comunas ES
# ============================================================
def make_tapizado_es():
    return '''
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

# ============================================================
# TAPIZADO DE VOLANTES - Template para comunas EN
# ============================================================
def make_tapizado_en():
    return '''
<!-- SECTION: STEERING WHEEL UPHOLSTERY LINK -->
<section class="py-5 bg-white">
  <div class="container">
    <div class="alert alert-success border-2 border-success shadow-lg p-4" role="alert">
      <div class="row align-items-center justify-content-center">
        <div class="col-12 text-center mb-4">
             <img src="https://tapizadodevolante.com/images/forrar-un-volante-con-cuero-forrar-volante-coche-en-santiago-monocromatico.jpg" class="img-fluid rounded shadow border border-3 border-success mx-auto d-block" style="max-height: 400px; object-fit: contain;" alt="Steering Wheel Upholstery">
        </div>
        <div class="col-12 text-center">
          <h2 class="text-uppercase fw-bold text-dark mb-3" style="font-size: 2rem;">
           Steering Wheel Upholstery AT HOME IN SANTIAGO
          </h2>
          <p class="text-justify mb-4" style="font-size: 1.1rem; line-height: 1.6;">
Steering wheel upholstery in Santiago to renew the look of your car. We work with high-quality leather, improving grip and aesthetics of the steering wheel. Quick and convenient solution without leaving home.
          </p>
          <p class="lead mb-4">
            If you want information about steering wheel upholstery in Santiago at home, visit the following link.
          </p>
          <a href="https://tapizadodevolante.com/" class="btn btn-success btn-lg fw-bold text-white">
            VISIT WEBSITE <i class="fas fa-external-link-alt ms-2"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# ============================================================
# ADD TAPIZADO TO ALL ES COMUNAS
# ============================================================
tapizado_es = make_tapizado_es()
count_es = 0
for fpath in sorted(glob.glob('comunas/*.html')):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has tapizado section
    if 'Tapizado de volantes' in content or 'tapizado de volantes' in content:
        print(f"SKIP (already has tapizado): {fpath}")
        continue
    
    # Insert before <!-- FOOTER -->
    if '<!-- FOOTER -->' in content:
        content = content.replace('<!-- FOOTER -->', tapizado_es + '\n<!-- FOOTER -->')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        count_es += 1
    else:
        print(f"WARNING: No <!-- FOOTER --> found in {fpath}")

print(f"Added tapizado to {count_es} ES comuna pages")

# ============================================================
# ADD TAPIZADO TO ALL EN COMUNAS
# ============================================================
tapizado_en = make_tapizado_en()
count_en = 0
for fpath in sorted(glob.glob('en/comunas/*.html')):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has tapizado section
    if 'Steering Wheel Upholstery' in content or 'steering wheel upholstery' in content:
        print(f"SKIP (already has tapizado): {fpath}")
        continue
    
    # Insert before <!-- FOOTER --> or <footer
    if '<!-- FOOTER -->' in content:
        content = content.replace('<!-- FOOTER -->', tapizado_en + '\n<!-- FOOTER -->')
    elif '<footer' in content:
        # Find the footer and insert before it
        content = content.replace('<footer', tapizado_en + '\n<footer', 1)
    else:
        print(f"WARNING: No footer found in {fpath}")
        continue
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    count_en += 1

print(f"Added tapizado to {count_en} EN comuna pages")

# ============================================================
# ALSO ADD TAPIZADO TO EN INDEX IF NOT PRESENT
# ============================================================
# Already handled separately

print("\nDone!")
