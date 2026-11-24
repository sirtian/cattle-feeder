const tracks = (await eda.pcb_PrimitiveLine.getAll()).map(l => ({
  net: l.getState_Net(), layer: l.getState_Layer(),
  x1: l.getState_StartX(), y1: l.getState_StartY(),
  x2: l.getState_EndX(), y2: l.getState_EndY(),
  w: l.getState_LineWidth()
}));
const vias = (await eda.pcb_PrimitiveVia.getAll()).map(v => ({
  net: v.getState_Net(), x: v.getState_X(), y: v.getState_Y(),
  d: v.getState_Diameter ? v.getState_Diameter() : null,
  drill: v.getState_HoleDiameter ? v.getState_HoleDiameter() : null
}));
const comps = await eda.pcb_PrimitiveComponent.getAll();
const pads = [];
for (const c of comps) {
  const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    pads.push({ net: p.getState_Net(), x: p.getState_X(), y: p.getState_Y(),
      comp: c.getState_Designator(),
      num: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()) });
  }
}
return { tracks, vias, pads };
