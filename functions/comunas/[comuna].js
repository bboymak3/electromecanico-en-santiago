import { conSeccion, redirigirHtml } from '../_shared/rutas.js';
export const onRequestGet = ctx => redirigirHtml(ctx) ||
  conSeccion(ctx, { lang: 'es', modo: 'comuna', comuna: String(ctx.params.comuna), grid: '#trabajos-realizados-comuna .row' });
