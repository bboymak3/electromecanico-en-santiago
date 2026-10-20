---
name: makeseo-footer
description: Cambia el crédito del footer de sitios web estáticos de "En Santiago 360" / "Santiago 360" / "Grupo 360 Soluciones" a "Página web desarrollada por makeseo.app" (enlace https://makeseo.app), lo agrega en las páginas que no lo tienen y actualiza el README. Usar cuando el usuario pida cambiar el footer, el crédito de la agencia, "desarrollada por 360" o poner makeseo.app en uno o varios sitios.
---

# Footer makeseo.app

Reemplaza el crédito de la agencia anterior por **makeseo.app** en todo un sitio HTML estático, sin romper ni eliminar contenido.

## Qué cambia

| Antes | Después |
|---|---|
| `Página web desarrollada por <strong>En Santiago 360</strong>` | `Página web desarrollada por <strong>makeseo.app</strong>` |
| `Página web desarrollada por Grupo 360 Soluciones` | `Página web desarrollada por makeseo.app` |
| `Website developed by En Santiago 360` | `Website developed by makeseo.app` |
| `href` del enlace del crédito (p. ej. `share.google/...`, `maps.app.goo.gl/...`) | `https://makeseo.app` |
| README: `Grupo 360 Soluciones` | `[makeseo.app](https://makeseo.app)` |
| Página sin crédito | Se agrega una barra de crédito antes de `</footer>` (o de `</body>`) |

No toca otros "360" (por ejemplo `rotate(360deg)`, "cámara 360°", "visibilidad 360º"): solo las formas de la marca `En Santiago 360`, `Santiago 360`, `Santiago360`, `Grupo 360 (Soluciones)` y `360 Soluciones`.

## Pasos

1. **Ubicarse en la raíz del sitio** (la carpeta del repositorio con los `.html`).
2. **Simular primero** (no escribe nada, muestra qué cambiaría):
   ```bash
   python3 .claude/skills/makeseo-footer/scripts/apply_makeseo_footer.py .
   ```
   Si la skill está instalada en otra ruta, usa esa ruta al script.
3. Revisar la lista. Cada línea indica el archivo y qué se hará:
   - `enlace de crédito → makeseo.app`
   - `texto de la agencia anterior → makeseo.app`
   - `crédito agregado (no tenía)`
4. **Aplicar**:
   ```bash
   python3 .claude/skills/makeseo-footer/scripts/apply_makeseo_footer.py . --apply
   ```
   - `--no-add`: solo reemplaza; no agrega crédito en páginas que no lo tienen.
   El script termina con `Menciones restantes de la marca anterior: 0`. Si no es 0, revisar esos archivos a mano.
5. **Verificar** antes de subir:
   - Ejecutar de nuevo con `--apply`: debe decir `0 archivos con cambios` (es idempotente).
   - `git diff --stat` y revisar que las líneas eliminadas sean solo los créditos antiguos.
   - Abrir una página con footer y una sin footer (o capturarlas con Playwright) y comprobar que el crédito se ve y enlaza a https://makeseo.app.
6. **Commit y push** a la rama que el usuario indique.

## Notas

- Las páginas con `<html lang="en...">` reciben el texto en inglés: "Website developed by makeseo.app".
- La barra que se agrega usa estilos en línea (degradado turquesa, botón tipo píldora), así se ve igual aunque la página no cargue el CSS global. Va marcada con `<!-- MAKESEO-CREDIT:START/END -->`.
- Si una página ya tiene un enlace a `https://makeseo.app`, no se agrega un segundo crédito.
- Si el sitio genera páginas con scripts o plantillas, actualizar también la plantilla para que el crédito no se pierda al regenerar (buscar "Santiago 360" o "Grupo 360" en los scripts).
- Ignora `.git`, `node_modules`, `.wrangler`, `dist`, `build`, `out`, `.claude` y los archivos de verificación `google*.html`.

## Usarla en otros sitios

Copiar la carpeta `.claude/skills/makeseo-footer/` al repositorio de cada sitio (o a `~/.claude/skills/` en tu computador para tenerla en todos los proyectos) y pedir: *"cambia el footer a makeseo.app"*.
