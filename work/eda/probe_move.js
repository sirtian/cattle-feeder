const all = await eda.pcb_PrimitiveComponent.getAll();
const want = ['C7','C8','C77','C85','R4','R5','R6','C93','D2'];
const out = [];
for (const d of want) {
  const c = all.find(x => x.getState_Designator() === d);
  if (!c) { out.push({d, missing:true}); continue; }
  const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  out.push({ d, id: c.getState_PrimitiveId(), x: c.getState_X(), y: c.getState_Y(), rot: c.getState_Rotation(),
    pads: pads.map(p => ({ n: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()), net: p.getState_Net(), x: +p.getState_X().toFixed(0), y: +p.getState_Y().toFixed(0) })) });
}
return out;
