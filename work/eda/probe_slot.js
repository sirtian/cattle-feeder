const out = { vias: [], pads: [] };
const vs = await eda.pcb_PrimitiveVia.getAll();
for (const v of vs) if (Math.hypot(v.getState_X()-1781.5, v.getState_Y()+3343.4)<10) out.vias.push({ id:v.getState_PrimitiveId(), net:v.getState_Net(), x:v.getState_X(), y:v.getState_Y() });
const pads = await eda.pcb_PrimitivePad.getAll();
for (const p of pads) {
  const x=p.getState_X(), y=p.getState_Y();
  if (Math.hypot(x+5441.3,y-1560.4)<40) out.pads.push({ id:p.getState_PrimitiveId(), net:p.getState_Net(), layer:p.getState_Layer(), x, y, shape:p.getState_Pad?p.getState_Pad():null });
}
return out;
