#!/usr/bin/env python3
"""Deja un solo recuadro '+100 Clientes Atendidos' en los bloques de estadísticas
que mostraban clientes junto a años de experiencia / garantía / disponibilidad,
y actualiza la cifra de clientes en los textos (+50 → +100). Idempotente."""
import glob
import re

COL = re.compile(r'(<div class="col-[^"]*">)\s*<div class="stat-item[^"]*"[^>]*>\s*<div class="stat-number[^"]*"[^>]*>([^<]*)</div>\s*'
                 r'<div class="stat-label[^"]*"[^>]*>([^<]*)</div>\s*</div>\s*</div>')
CLIENT = re.compile(r'clientes atendidos|customers served|cars repaired|autos reparados', re.I)
TEXT = [(r'<div class="stat-number">\+50</div>', '<div class="stat-number">+100</div>'),
        (r'\+50 (clientes|customers)', r'+100 \1'), (r'\b50\+ customers', '100+ customers'),
        (r'([Mm][aá]s de|[Mm]ore de|[Mm]ore than|[Oo]ver) 50 (clientes|customers|satisfied customers)', r'\1 100 \2'),
        (r'\+5\.?000 (clientes|customers)', r'+100 \1')]


def groups(s):
    ms = list(COL.finditer(s))
    out, cur = [], []
    for m in ms:
        if cur and s[cur[-1].end():m.start()].strip() == "":
            cur.append(m)
        else:
            if cur:
                out.append(cur)
            cur = [m]
    if cur:
        out.append(cur)
    return out


blocks = files = 0
for f in glob.glob("**/*.html", recursive=True):
    s = o = open(f, encoding="utf-8").read()
    en = f.startswith("en/")
    for g in reversed(groups(s)):
        if not any(CLIENT.search(m.group(3)) for m in g):
            continue
        if len(g) == 1 and g[0].group(2).strip() == "+100":
            continue
        label = "Customers Served" if en else "Clientes Atendidos"
        new = (f'<div class="col-12"><div class="stat-item"><div class="stat-number">+100</div>'
               f'<div class="stat-label">{label}</div></div></div>')
        s = s[:g[0].start()] + new + s[g[-1].end():]
        blocks += 1
    for a, b in TEXT:
        s = re.sub(a, b, s)
    if s != o:
        open(f, "w", encoding="utf-8").write(s)
        files += 1
print(f"bloques de estadísticas simplificados: {blocks}; archivos modificados: {files}")
