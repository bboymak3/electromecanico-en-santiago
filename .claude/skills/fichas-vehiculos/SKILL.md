---
name: fichas-vehiculos
description: Agrega un vehículo atendido a la galería del sitio Electromecánico en Santiago (index + /galeria) con su ficha modal y sus fotos renombradas con palabras clave y la comuna al final. Usar cuando el usuario envíe fotos de un vehículo y pida "agrega este vehículo", "súbelo a la galería", "crea la ficha", o indique el trabajo realizado y la comuna.
---

# Fichas de vehículos (galería de trabajos realizados)

Cada vehículo atendido se agrega como una **ficha**: tarjeta en "Trabajos Realizados" del index, ficha modal (vehículo, servicio, comuna, descripción, trabajos realizados, fotos), fotos en la grilla 3:4 del index y en `/galeria` con su filtro. Todo sale de `scripts/galeria_data.json`.

## 1. Reunir los datos (no inventar)

| Dato | De dónde | Si falta |
|---|---|---|
| Vehículo (marca, modelo, año) | Mensaje del usuario o identificarlo en la foto (logo, parrilla) | Identificarlo y **decir que lo identificaste por la foto** |
| Servicio / trabajo realizado | Mensaje del usuario | Deducirlo de la foto con prudencia y **pedir confirmación** |
| Comuna | Mensaje del usuario | Usar **Santiago** y avisarlo |
| ¿Fue a domicilio? | Mensaje / foto | Si la foto muestra taller (grúa, motor desmontado), **no escribir "a domicilio"** y avisarlo |

- Si el mensaje no trae imágenes adjuntas, **pedir las fotos**; no crear la ficha sin fotos.
- Interpretar errores de dictado razonables (p. ej. "el vehículo encendida" = "no encendía") y decirlo.
- No agregar precios, garantías ni datos que el usuario no dio.
- Si el usuario agrega una frase de marca (p. ej. "recuerda que somos tu mejor opción M&E"), incluirla al final de la descripción.

## 2. Escribir la ficha

Crear un JSON temporal en el scratchpad (no en el repositorio):

```json
{
  "vehiculo": "Suzuki Alto",
  "servicio": "Auto no enciende: cables del distribuidor cortados",
  "comuna": "La Cisterna",
  "icono": "fa-bolt",
  "resumen": "Una línea para la tarjeta (≈ 15–20 palabras).",
  "descripcion": "Párrafo: problema → diagnóstico → reparación → resultado. Mencionar la comuna.",
  "trabajos_realizados": ["Diagnóstico ...", "Detección ...", "Reparación ...", "Prueba ..."],
  "fotos": [
    {"src": "/root/.claude/uploads/.../foto.jpg",
     "nombre": "suzuki-alto-no-enciende-cables-distribuidor-cortados-a-domicilio",
     "caption": "Suzuki Alto atendido a domicilio en La Cisterna"}
  ]
}
```

- **Nombre de cada foto**: `marca-modelo-palabras-clave-del-trabajo-a-domicilio` (o `electromecanico-a-domicilio`, `mecanico-a-domicilio`), sin tildes, separado con `-`. El script agrega la **comuna al final** (`...-la-cisterna`). Cada foto con un nombre distinto.
- **Orden de fotos**: primero la que mejor muestra el vehículo completo (será la portada de la tarjeta).
- **Ícono** (Font Awesome): `fa-bolt` eléctrico, `fa-car-battery` batería/arranque, `fa-temperature-high` / `fa-temperature-low` refrigeración, `fa-cogs` motor/distribución, `fa-lightbulb` luces, `fa-water` agua/fugas, `fa-tools` general.
- Fotos de contexto (p. ej. la carretera camino a la comuna) se pueden incluir con un nombre como `electromecanico-a-domicilio-en-ruta-a-<comuna>`.

## 3. Ejecutar

Desde la raíz del repositorio:

```bash
python3 .claude/skills/fichas-vehiculos/scripts/agregar_vehiculo.py /ruta/ficha.json          # simulación
python3 .claude/skills/fichas-vehiculos/scripts/agregar_vehiculo.py /ruta/ficha.json --apply  # aplicar
```

El script descarta fotos duplicadas (mismo contenido), redimensiona (1200 px + miniatura 480 px), inserta la ficha **al inicio** de `scripts/galeria_data.json` y ejecuta `build_galeria.py` y `seo_social_schema.py`.

## 4. Verificar antes de subir

- `git status`: solo deben cambiar `index.html`, `galeria.html`, `sitemap.xml`, `scripts/galeria_data.json` y las fotos nuevas.
- Probar con Playwright (servidor local `python3 -m http.server`; servir Bootstrap local porque el CDN está bloqueado): la ficha modal abre, la foto abre en el lightbox, el filtro de `/galeria` muestra las fotos del vehículo, sin scroll horizontal a 390 px y 1280 px.
- `galeria.html` debe conservar el script `REDIRECT 301` y el crédito `https://makeseo.app`.

## 5. Subir y avisar

- Commit `feat: <Vehículo> en galería (<trabajo>, <comuna>)` y push a `main`.
- Responder con: datos de la ficha, nombres de las fotos, total de vehículos/fotos de la galería, y lo que se supuso (modelo identificado por foto, comuna por defecto, "a domicilio" o no, interpretación del texto) para que el usuario lo confirme.

## Editar o corregir una ficha existente

Editar la entrada en `scripts/galeria_data.json` (para renombrar fotos usar `git mv` en `images/galeria/`, también la `-thumb`), luego `python3 scripts/build_galeria.py && python3 scripts/seo_social_schema.py`.
