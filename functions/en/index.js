import { conSeccion } from '../_shared/rutas.js';
export const onRequestGet = ctx => conSeccion(ctx, { lang: 'en', modo: 'home', limite: 8 });
