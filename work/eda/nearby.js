const pts = { U33_3: [1083.9, 403.6], U33_6: [1007.1, 403.6], U34_3: [3046.5, 1139.4], U34_6: [2896.4, 1139.4] };
const lines = await eda.pcb_PrimitiveLine.getAll();
const vias = await eda.pcb_PrimitiveVia.getAll();
function dseg(px, py, x1, y1, x2, y2) {
  const dx = x2 - x1, dy = y2 - y1;
  const L = dx*dx + dy*dy;
  let t = L ? ((px-x1)*dx + (py-y1)*dy) / L : 0;
  t = Math.max(0, Math.min(1, t));
  const qx = x1 + t*dx, qy = y1 + t*dy;
  return Math.hypot(px-qx, py-qy);
}
const out = {};
for (const [k, [px, py]] of Object.entries(pts)) {
  const near = [];
  for (const l of lines) {
    const d = dseg(px, py, l.getState_StartX(), l.getState_StartY(), l.getState_EndX(), l.getState_EndY());
    if (d < 120) near.push({ t: 'trk', net: l.getState_Net(), layer: l.getState_Layer(), d: +d.toFixed(1),
      a: [Math.round(l.getState_StartX()), Math.round(l.getState_StartY())],
      b: [Math.round(l.getState_EndX()), Math.round(l.getState_EndY())] });
  }
  for (const v of vias) {
    const d = Math.hypot(px - v.getState_X(), py - v.getState_Y());
    if (d < 120) near.push({ t: 'via', net: v.getState_Net(), d: +d.toFixed(1), p: [Math.round(v.getState_X()), Math.round(v.getState_Y())] });
  }
  out[k] = near.sort((a,b)=>a.d-b.d).slice(0, 12);
}
return out;
