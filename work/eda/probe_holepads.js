const comps = await eda.pcb_PrimitiveComponent.getAll();
const pads = await eda.pcb_PrimitivePad.getAll();
const out = [];
for (const p of pads) {
  const net = p.getState_Net ? p.getState_Net() : null;
  const lay = p.getState_Layer ? p.getState_Layer() : null;
  if (net) continue;
  if (lay !== 12) continue;
  out.push({ id: p.getState_PrimitiveId(), x: +p.getState_X().toFixed(1), y: +p.getState_Y().toFixed(1),
    parent: p.getState_ParentComponentPrimitiveId ? p.getState_ParentComponentPrimitiveId() : null,
    shape: p.getState_Pad ? p.getState_Pad() : null });
}
return out;
