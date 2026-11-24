const out = {};
try {
  const p = await eda.pcb_PrimitivePad.get(['f29e6f04d3cc3529']);
  if (p && p.length) out.pad = { x: p[0].getState_X(), y: p[0].getState_Y(), net: p[0].getState_Net(), layer: p[0].getState_Layer ? p[0].getState_Layer() : null };
} catch(e) { out.err = String(e); }
const all = await eda.pcb_PrimitiveComponent.getAll();
const near = [];
for (const c of all) {
  const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const q of ps) {
    const x = q.getState_X(), y = q.getState_Y();
    if (Math.hypot(x + 3690.9, y - 1968.2) < 200) near.push({ comp: c.getState_Designator(), n: String(q.getState_Number ? q.getState_Number() : q.getState_PadNumber()), net: q.getState_Net(), x: +x.toFixed(0), y: +y.toFixed(0) });
  }
}
out.near = near;
return out;
