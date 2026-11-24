const comps = await eda.pcb_PrimitiveComponent.getAll();
const pads = [];
for (const c of comps) {
  const d = c.getState_Designator();
  const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    const sh = p.getState_Pad ? p.getState_Pad() : null;
    pads.push({ comp: d, num: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()),
      net: p.getState_Net(), x: p.getState_X(), y: p.getState_Y(),
      rot: p.getState_Rotation ? p.getState_Rotation() : 0,
      shape: sh });
  }
}
return pads;
