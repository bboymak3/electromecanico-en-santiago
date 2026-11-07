import { conSeccion, redirigirHtml } from '../../_shared/rutas.js';
export const onRequestGet = ctx => redirigirHtml(ctx) ||
  conSeccion(ctx, { lang: 'en', modo: 'comuna', comuna: String(ctx.params.comuna) });
