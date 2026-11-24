const all = await eda.pcb_PrimitiveComponent.getAll();
const out = {};
for (const d of ['U33', 'U34']) {
  const c = all.find(x => x.getState_Designator() === d);
  if (!c) { out[d] = 'not found'; continue; }
  const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  out[d] = pads.map(p => ({
    net: p.getState_Net ? p.getState_Net() : null,
    x: p.getState_X ? p.getState_X() : null,
    y: p.getState_Y ? p.getState_Y() : null,
    layer: p.getState_Layer ? p.getState_Layer() : null,
    num: p.getState_Number ? p.getState_Number() : (p.getState_PadNumber ? p.getState_PadNumber() : null)
  }));
}
return out;
