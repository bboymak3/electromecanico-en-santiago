import { conSeccion } from './_shared/rutas.js';
export const onRequestGet = ctx => conSeccion(ctx, { lang: 'es', modo: 'galeria', grid: '#fichas .row' });
