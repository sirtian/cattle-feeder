const all = await eda.pcb_PrimitiveComponent.getAll();
const out = [];
for (const [d, nums] of [['U33', ['3', '6']], ['U34', ['3', '6']]]) {
  const c = all.find(x => x.getState_Designator() === d);
  const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of pads) {
    const num = p.getState_Number ? p.getState_Number() : p.getState_PadNumber();
    if (nums.includes(String(num))) out.push({
      d, num, net: p.getState_Net(),
      xmm: +(p.getState_X() * 0.0254).toFixed(3),
      ymm: +(p.getState_Y() * 0.0254).toFixed(3),
      layer: p.getState_Layer()
    });
  }
}
const comp = all.filter(c => ['U33', 'U34'].includes(c.getState_Designator())).map(c => ({
  d: c.getState_Designator(),
  xmm: +(c.getState_X() * 0.0254).toFixed(2),
  ymm: +(c.getState_Y() * 0.0254).toFixed(2),
  rot: c.getState_Rotation()
}));
return { pads: out, comp };
