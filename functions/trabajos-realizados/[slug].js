import { detalle } from '../_shared/rutas.js';
// Ficha de cada trabajo: /trabajos-realizados/<titulo>-<id>
export const onRequestGet = ctx => detalle(ctx, 'es');
