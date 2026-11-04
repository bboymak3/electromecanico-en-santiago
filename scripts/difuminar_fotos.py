#!/usr/bin/env python3
"""Difumina patentes y números de serie en las fotos de la galería.

Cada foto de scripts/galeria_data.json puede tener:
  "difuminar": [[x1, y1, x2, y2], ...]   zonas en proporción de la foto (0 a 1)
  "difuminado": true                      ya revisada/aplicada (no se vuelve a aplicar)

Uso:
  python3 scripts/difuminar_fotos.py            # aplica a las fotos pendientes
  python3 scripts/difuminar_fotos.py --preview DIR   # guarda vistas con las zonas marcadas
Rehace la miniatura (-thumb.jpg) desde la foto difuminada. Idempotente.
"""
import argparse
import json
import os

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "scripts", "galeria_data.json")
IMG = os.path.join(ROOT, "images", "galeria")


def boxes_px(zonas, w, h, pad=0.01):
    for x1, y1, x2, y2 in zonas:
        yield (max(0, int((x1 - pad) * w)), max(0, int((y1 - pad) * h)),
               min(w, int((x2 + pad) * w)), min(h, int((y2 + pad) * h)))


def difuminar(im, zonas):
    w, h = im.size
    for b in boxes_px(zonas, w, h):
        reg = im.crop(b)
        bw, bh = reg.size
        if bw < 2 or bh < 2:
            continue
        small = reg.resize((max(1, bw // 14), max(1, bh // 14)), Image.BILINEAR)
        reg = small.resize((bw, bh), Image.NEAREST).filter(ImageFilter.GaussianBlur(max(3, min(bw, bh) // 6)))
        im.paste(reg, b)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview")
    a = ap.parse_args()
    data = json.load(open(DATA, encoding="utf-8"))
    n = 0
    for t in data["trabajos"]:
        for f in t["fotos"]:
            zonas = f.get("difuminar", [])
            path = os.path.join(IMG, f["file"] + ".jpg")
            if a.preview:
                im = Image.open(path).convert("RGB")
                dr = ImageDraw.Draw(im)
                for b in boxes_px(zonas, *im.size):
                    dr.rectangle(b, outline=(255, 0, 255), width=4)
                os.makedirs(a.preview, exist_ok=True)
                im.save(os.path.join(a.preview, f["file"] + ".jpg"), quality=80)
                continue
            if f.get("difuminado") or not zonas:
                continue
            im = difuminar(Image.open(path).convert("RGB"), zonas)
            im.save(path, quality=85, optimize=True, progressive=True)
            th = im.copy()
            th.thumbnail((480, 480))
            th.save(os.path.join(IMG, f["file"] + "-thumb.jpg"), quality=78, optimize=True, progressive=True)
            f["difuminado"] = True
            n += 1
    if not a.preview:
        with open(DATA, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"fotos difuminadas: {n}")


if __name__ == "__main__":
    main()
