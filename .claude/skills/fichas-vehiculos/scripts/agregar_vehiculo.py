#!/usr/bin/env python3
"""Agrega un vehículo (ficha + fotos) a la galería del sitio y regenera todo.

Uso (desde la raíz del repositorio):
    python3 .claude/skills/fichas-vehiculos/scripts/agregar_vehiculo.py ficha.json            # simulación
    python3 .claude/skills/fichas-vehiculos/scripts/agregar_vehiculo.py ficha.json --apply    # aplica

ficha.json:
{
  "vehiculo": "Opel Corsa 2023",
  "servicio": "Servicio de escáner y cambio de batería a domicilio",
  "comuna": "Macul",
  "icono": "fa-car-battery",
  "resumen": "Una línea para la tarjeta del index.",
  "descripcion": "Párrafo de la ficha.",
  "trabajos_realizados": ["Paso 1", "Paso 2"],
  "fotos": [
    {"src": "/ruta/a/foto1.jpg", "nombre": "opel-corsa-2023-escaner-cambio-de-bateria-a-domicilio",
     "caption": "Opel Corsa 2023 – escáner y cambio de batería a domicilio en Macul"}
  ]
}
- "slug" es opcional (se calcula desde "vehiculo").
- "nombre" de cada foto: palabras clave separadas con "-"; la comuna se agrega al final
  automáticamente si no está.
- Las fotos repetidas (mismo contenido) se descartan.

Qué hace con --apply:
  1. Redimensiona cada foto a máx. 1200 px (+ miniatura 480 px) en images/galeria/.
  2. Inserta la ficha al inicio de scripts/galeria_data.json.
  3. Ejecuta scripts/build_galeria.py (index, /galeria, fichas modales) y
     scripts/seo_social_schema.py (metadatos y sitemap).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

ROOT = os.getcwd()
DATA = os.path.join(ROOT, "scripts", "galeria_data.json")
IMG = os.path.join(ROOT, "images", "galeria")


def slugify(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ficha")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(DATA):
        sys.exit("No encuentro scripts/galeria_data.json: ejecuta desde la raíz del repositorio.")
    f = json.load(open(a.ficha, encoding="utf-8"))
    for k in ("vehiculo", "servicio", "comuna", "resumen", "descripcion", "trabajos_realizados", "fotos"):
        if not f.get(k):
            sys.exit(f"Falta el campo '{k}' en {a.ficha}")
    slug = f.get("slug") or slugify(f["vehiculo"])
    comuna_slug = slugify(f["comuna"])
    data = json.load(open(DATA, encoding="utf-8"))
    if any(t["slug"] == slug for t in data["trabajos"]):
        sys.exit(f"Ya existe un vehículo con slug '{slug}'. Usa otro 'slug' (p. ej. '{slug}-2') o edita el existente.")

    vistos, fotos = set(), []
    for p in f["fotos"]:
        h = hashlib.md5(open(p["src"], "rb").read()).hexdigest()
        if h in vistos:
            print(f"  · foto repetida descartada: {p['src']}")
            continue
        vistos.add(h)
        nombre = slugify(p["nombre"])
        if not nombre.endswith(comuna_slug):
            nombre = f"{nombre}-{comuna_slug}"
        if os.path.exists(os.path.join(IMG, nombre + ".jpg")):
            sys.exit(f"Ya existe images/galeria/{nombre}.jpg: elige otro 'nombre'.")
        fotos.append((p["src"], nombre, p.get("caption") or f'{f["vehiculo"]} – {f["servicio"]}'))

    entry = {"slug": slug, "vehiculo": f["vehiculo"], "servicio": f["servicio"], "comuna": f["comuna"],
             "icono": f.get("icono", "fa-tools"), "resumen": f["resumen"], "descripcion": f["descripcion"],
             "trabajos_realizados": f["trabajos_realizados"],
             "fotos": [{"file": n, "caption": c} for _, n, c in fotos]}
    print(f"Vehículo: {entry['vehiculo']}  (slug: {slug}, comuna: {entry['comuna']})")
    for src, n, c in fotos:
        print(f"  foto: images/galeria/{n}.jpg  ← {os.path.basename(src)}  «{c}»")
    if not a.apply:
        print("\nSimulación: no se escribió nada. Repite con --apply para agregarlo.")
        return
    from PIL import Image, ImageOps
    for src, n, _ in fotos:
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        big = im.copy(); big.thumbnail((1200, 1200))
        big.save(os.path.join(IMG, n + ".jpg"), quality=82, optimize=True, progressive=True)
        th = im.copy(); th.thumbnail((480, 480))
        th.save(os.path.join(IMG, n + "-thumb.jpg"), quality=78, optimize=True, progressive=True)
    data["trabajos"].insert(0, entry)
    with open(DATA, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    for s in ("build_galeria.py", "seo_social_schema.py"):
        print(subprocess.run([sys.executable, os.path.join("scripts", s)], check=True, capture_output=True, text=True).stdout.strip())
    print(f"\nListo: {entry['vehiculo']} agregado con {len(fotos)} foto(s).")


if __name__ == "__main__":
    main()
