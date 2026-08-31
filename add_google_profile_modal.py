#!/usr/bin/env python3
"""
Inserta un modal de Google Business Profile en las 52 paginas de comunas.
El modal es identico para todas y se activa con un boton prominente.
"""

import os
import re
import glob

COMUNAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comunas')

# =========================================================================
# HTML del boton que abre el modal - se inserta ANTES del FAQ section
# =========================================================================
GOOGLE_PROFILE_BUTTON_HTML = """
<!-- ======================================================================= -->
<!-- GOOGLE BUSINESS PROFILE - BOTON -->
<!-- ======================================================================= -->
<section class="py-4" style="background: linear-gradient(135deg, #fff8f0 0%, #fff 100%); position: relative; overflow: hidden;">
  <div style="position:absolute; top:-50px; left:50%; transform:translateX(-50%); width:600px; height:200px; background:radial-gradient(ellipse, rgba(255,193,7,0.10) 0%, transparent 70%); pointer-events:none;"></div>
  <div class="container" style="position:relative; z-index:2;">
    <div class="text-center">
      <div style="display:inline-flex; align-items:center; gap:12px; background:#fff; border:2px solid #FFC107; border-radius:16px; padding:18px 30px; box-shadow:0 6px 25px rgba(255,193,7,0.15); transition:all 0.3s; cursor:pointer;" onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 10px 35px rgba(255,193,7,0.25)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 6px 25px rgba(255,193,7,0.15)'" onclick="document.getElementById('modal-google-profile').style.display='flex'">
        <div style="width:55px; height:55px; background:linear-gradient(135deg, #4285F4, #34A853, #FBBC05, #EA4335); border-radius:14px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fab fa-google" style="font-size:1.6rem; color:#fff;"></i>
        </div>
        <div style="text-align:left;">
          <div style="font-weight:800; font-size:1.1rem; color:#1a1a1a;">Ver Nuestro Perfil de Google</div>
          <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
            <span style="color:#FBBC05; font-size:1.1rem;">
              <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
            </span>
            <span style="font-weight:700; color:#1a1a1a; font-size:0.95rem;">4.9</span>
            <span style="color:#666; font-size:0.85rem;">| 155+ opiniones verificadas</span>
          </div>
        </div>
        <i class="fas fa-external-link-alt" style="color:#4285F4; font-size:1rem; margin-left:8px;"></i>
      </div>
    </div>
  </div>
</section>
"""

# =========================================================================
# HTML del modal - se inserta ANTES del footer
# =========================================================================
GOOGLE_PROFILE_MODAL_HTML = """
<!-- ======================================================================= -->
<!-- MODAL GOOGLE BUSINESS PROFILE -->
<!-- ======================================================================= -->
<div id="modal-google-profile" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.75); z-index:10000; align-items:center; justify-content:center; padding:15px; overflow-y:auto;">
  <div style="background:#fff; border-radius:20px; max-width:580px; width:100%; margin:auto; box-shadow:0 25px 60px rgba(0,0,0,0.4); position:relative; animation:modalSlideIn 0.3s ease; overflow:hidden;">
    <!-- Header con gradiente Google -->
    <div style="background:linear-gradient(135deg, #4285F4 0%, #34A853 50%, #FBBC05 100%); padding:28px 24px 22px; position:relative; overflow:hidden;">
      <div style="position:absolute; top:-30px; right:-30px; width:120px; height:120px; background:rgba(255,255,255,0.08); border-radius:50%;"></div>
      <div style="position:absolute; bottom:-40px; left:-20px; width:100px; height:100px; background:rgba(255,255,255,0.05); border-radius:50%;"></div>
      <button onclick="document.getElementById('modal-google-profile').style.display='none'" style="position:absolute; top:12px; right:16px; background:rgba(255,255,255,0.2); border:none; color:#fff; font-size:1.4rem; cursor:pointer; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.4)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">&times;</button>
      <div style="display:flex; align-items:center; gap:16px; position:relative; z-index:2;">
        <div style="width:65px; height:65px; background:#fff; border-radius:16px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 15px rgba(0,0,0,0.2); flex-shrink:0;">
          <i class="fas fa-wrench" style="font-size:1.8rem; color:#a80000;"></i>
        </div>
        <div>
          <h3 style="margin:0; font-size:1.2rem; font-weight:800; color:#fff; line-height:1.3;">MECANICO A DOMICILIO 24/7</h3>
          <p style="margin:4px 0 0; font-size:0.85rem; color:rgba(255,255,255,0.9); font-weight:600;">GLOBAL PRO Automotriz</p>
          <p style="margin:2px 0 0; font-size:0.78rem; color:rgba(255,255,255,0.8);">Especialistas en Motor Frenos y Electricidad</p>
        </div>
      </div>
    </div>
    <!-- Rating y opiniones -->
    <div style="padding:20px 24px 0; text-align:center;">
      <div style="display:inline-flex; align-items:center; gap:10px; background:#fef9e7; border:2px solid #FBBC05; border-radius:14px; padding:12px 22px;">
        <span style="font-size:2rem; font-weight:900; color:#1a1a1a;">4.9</span>
        <div>
          <div style="color:#FBBC05; font-size:1.2rem;">
            <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
          </div>
          <div style="font-size:0.8rem; color:#666; font-weight:600;">155+ opiniones en Google</div>
        </div>
        <i class="fab fa-google" style="font-size:1.4rem; color:#4285F4;"></i>
      </div>
    </div>
    <!-- Info del negocio -->
    <div style="padding:20px 24px;">
      <!-- Direccion -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid #f0f0f0;">
        <div style="width:40px; height:40px; background:#e8f5e9; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-map-marker-alt" style="color:#34A853; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Direccion</div>
          <div style="font-size:0.85rem; color:#555; margin-top:2px;">Av. Padre Alberto Hurtado 3598, Pedro Aguirre Cerda, Region Metropolitana, Chile</div>
        </div>
      </div>
      <!-- Telefono -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid #f0f0f0;">
        <div style="width:40px; height:40px; background:#e3f2fd; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-phone-alt" style="color:#4285F4; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Telefono</div>
          <a href="tel:+56939026185" style="font-size:0.95rem; color:#4285F4; font-weight:700; text-decoration:none;">+56 9 3902 6185</a>
        </div>
      </div>
      <!-- Horario -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid #f0f0f0;">
        <div style="width:40px; height:40px; background:#fff3e0; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-clock" style="color:#FBBC05; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Horario</div>
          <div style="font-size:0.85rem; color:#555; margin-top:2px;"><span style="background:#e8f5e9; color:#2E7D32; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.78rem;">ABIERTO</span> Las 24 horas</div>
        </div>
      </div>
      <!-- Servicios principales -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid #f0f0f0;">
        <div style="width:40px; height:40px; background:#fce4ec; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-tools" style="color:#EA4335; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Servicios Principales</div>
          <div style="font-size:0.82rem; color:#555; margin-top:4px; line-height:1.7;">
            <i class="fas fa-check" style="color:#34A853; margin-right:4px;"></i> Mecanico a Domicilio en Santiago<br>
            <i class="fas fa-check" style="color:#34A853; margin-right:4px;"></i> Reparacion de motor y transmision<br>
            <i class="fas fa-check" style="color:#34A853; margin-right:4px;"></i> Sistema electrico computarizado<br>
            <i class="fas fa-check" style="color:#34A853; margin-right:4px;"></i> Frenos, suspension y direccion<br>
            <i class="fas fa-check" style="color:#34A853; margin-right:4px;"></i> Mantenimiento preventivo
          </div>
        </div>
      </div>
      <!-- Servicio de Urgencia -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0; border-bottom:1px solid #f0f0f0;">
        <div style="width:40px; height:40px; background:#ffebee; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-exclamation-triangle" style="color:#D32F2F; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Servicio de Urgencia 24/7</div>
          <div style="font-size:0.82rem; color:#555; margin-top:4px; line-height:1.7;">
            <i class="fas fa-angle-right" style="color:#D32F2F; margin-right:4px;"></i> Atencion a domicilio o trabajo<br>
            <i class="fas fa-angle-right" style="color:#D32F2F; margin-right:4px;"></i> Auxilio en carretera<br>
            <i class="fas fa-angle-right" style="color:#D32F2F; margin-right:4px;"></i> Problemas de arranque<br>
            <i class="fas fa-angle-right" style="color:#D32F2F; margin-right:4px;"></i> Fallas electricas repentinas
          </div>
        </div>
      </div>
      <!-- Garantias -->
      <div style="display:flex; align-items:flex-start; gap:14px; padding:12px 0;">
        <div style="width:40px; height:40px; background:#e8eaf6; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <i class="fas fa-shield-alt" style="color:#3F51B5; font-size:1.1rem;"></i>
        </div>
        <div>
          <div style="font-weight:700; font-size:0.9rem; color:#333;">Nueas Garantias</div>
          <div style="font-size:0.82rem; color:#555; margin-top:4px; line-height:1.7;">
            <i class="fas fa-check-double" style="color:#3F51B5; margin-right:4px;"></i> Profesionales con experiencia comprobada<br>
            <i class="fas fa-check-double" style="color:#3F51B5; margin-right:4px;"></i> Repuestos de calidad garantizada<br>
            <i class="fas fa-check-double" style="color:#3F51B5; margin-right:4px;"></i> Presupuesto claro sin costo<br>
            <i class="fas fa-check-double" style="color:#3F51B5; margin-right:4px;"></i> Garantia en todas las reparaciones
          </div>
        </div>
      </div>
    </div>
    <!-- Boton prominente al perfil de Google -->
    <div style="padding:0 24px 24px;">
      <a href="https://share.google/H2Gwc1WC2PzyJ2oma" target="_blank" rel="noopener noreferrer" style="display:flex; align-items:center; justify-content:center; gap:10px; width:100%; padding:16px; background:linear-gradient(135deg, #4285F4, #34A853); color:#fff; border-radius:14px; text-decoration:none; font-weight:800; font-size:1.1rem; transition:all 0.3s; box-shadow:0 6px 20px rgba(66,133,244,0.35);" onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 10px 30px rgba(66,133,244,0.5)'" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 6px 20px rgba(66,133,244,0.35)'">
        <i class="fab fa-google" style="font-size:1.3rem;"></i>
        Ver Perfil Completo en Google
        <i class="fas fa-external-link-alt" style="font-size:0.85rem;"></i>
      </a>
      <div style="text-align:center; margin-top:12px;">
        <a href="https://wa.me/56939026185?text=Hola%20necesito%20un%20mecanico%20a%20domicilio" target="_blank" style="display:inline-flex; align-items:center; gap:8px; padding:10px 22px; background:#25D366; color:#fff; border-radius:50px; text-decoration:none; font-weight:700; font-size:0.9rem; transition:all 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
          <i class="fab fa-whatsapp"></i> Cotizar por WhatsApp
        </a>
      </div>
    </div>
  </div>
</div>
<!-- FIN MODAL GOOGLE BUSINESS PROFILE -->
"""


def process_comuna_file(filepath):
    """Inserta el boton y modal de Google Business Profile en una comuna."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has the modal
    if 'modal-google-profile' in content:
        print(f"  SKIP (ya tiene modal): {os.path.basename(filepath)}")
        return False

    # 1. Insert button BEFORE the FAQ section
    # Find the FAQ section marker
    faq_marker = '<!-- PREGUNTAS FRECUENTES (FAQ) -->'
    if faq_marker not in content:
        # Try alternative
        faq_marker = '<section class="py-5 bg-light" id="faq">'
        if faq_marker not in content:
            # Try another pattern
            faq_marker = 'Preguntas Frecuentes'
            if faq_marker not in content:
                print(f"  WARN: No FAQ found in {os.path.basename(filepath)}")
                return False
            # Find the section tag before FAQ
            faq_pos = content.find(faq_marker)
            # Look backwards for <!--
            section_start = content.rfind('<!--', 0, faq_pos)
            if section_start == -1:
                section_start = faq_pos
            faq_marker = content[section_start:faq_pos + 50]

    if faq_marker in content:
        content = content.replace(faq_marker, GOOGLE_PROFILE_BUTTON_HTML + '\n' + faq_marker, 1)
    else:
        print(f"  WARN: Could not insert button in {os.path.basename(filepath)}")
        return False

    # 2. Insert modal BEFORE the footer
    footer_marker = '<!-- FOOTER -->'
    if footer_marker not in content:
        footer_marker = '<footer class="main-footer">'
        if footer_marker not in content:
            footer_marker = '<footer'
            if footer_marker not in content:
                print(f"  WARN: No footer found in {os.path.basename(filepath)}")
                return False

    if footer_marker in content:
        content = content.replace(footer_marker, GOOGLE_PROFILE_MODAL_HTML + '\n' + footer_marker, 1)
    else:
        print(f"  WARN: Could not insert modal in {os.path.basename(filepath)}")
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    comuna_files = sorted(glob.glob(os.path.join(COMUNAS_DIR, '*.html')))
    print(f"Encontradas {len(comuna_files)} paginas de comunas")

    success = 0
    skip = 0
    fail = 0

    for fpath in comuna_files:
        fname = os.path.basename(fpath)
        result = process_comuna_file(fpath)
        if result is True:
            success += 1
            print(f"  OK: {fname}")
        elif result is False and 'modal-google-profile' in open(fpath, 'r', encoding='utf-8').read():
            skip += 1
        else:
            fail += 1

    print(f"\nResultado: {success} insertados, {skip} omitidos, {fail} fallidos de {len(comuna_files)} total")


if __name__ == '__main__':
    main()
