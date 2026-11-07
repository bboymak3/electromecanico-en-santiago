import { conSeccion } from './_shared/rutas.js';
// Home: trabajos publicados al inicio del grid "Trabajos Realizados" (HTML para Google)
export const onRequestGet = ctx => conSeccion(ctx, { lang: 'es', modo: 'home', grid: '#trabajos-realizados .row', limite: 8 });
