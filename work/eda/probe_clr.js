const ids = ['1f5022c0ce55c35b','74a75c254edc3346','65797a59f8a9bc51','9d4140331dd97804','f29e6f04d3cc3529'];
const out = { lines: [], vias: [], other: [] };
for (const id of ids) {
  let found = false;
  try { const l = await eda.pcb_PrimitiveLine.get([id]); if (l && l.length) { out.lines.push({ id, net: l[0].getState_Net(), layer: l[0].getState_Layer(), a: [l[0].getState_StartX(), l[0].getState_StartY()], b: [l[0].getState_EndX(), l[0].getState_EndY()], w: l[0].getState_LineWidth() }); found = true; } } catch(e) {}
  if (found) continue;
  try { const v = await eda.pcb_PrimitiveVia.get([id]); if (v && v.length) { out.vias.push({ id, net: v[0].getState_Net(), x: v[0].getState_X(), y: v[0].getState_Y() }); found = true; } } catch(e) {}
  if (found) continue;
  out.other.push(id);
}
const all = await eda.pcb_PrimitiveComponent.getAll();
const k = all.find(c => c.getState_Designator() === 'K15');
if (k) {
  const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(k.getState_PrimitiveId());
  out.k15 = pads.map(p => ({ n: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()), x: p.getState_X(), y: p.getState_Y(), net: p.getState_Net() }));
}
return out;
