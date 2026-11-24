const out = { a: [], b: [] };
const vs = await eda.pcb_PrimitiveVia.getAll();
for (const v of vs) {
  const x=v.getState_X(), y=v.getState_Y();
  if (Math.hypot(x+5441.3,y-1560.4)<30) out.a.push({t:'via',id:v.getState_PrimitiveId(),net:v.getState_Net(),x,y});
  if (Math.hypot(x-1781.5,y+3343.4)<30) out.b.push({t:'via',id:v.getState_PrimitiveId(),net:v.getState_Net(),x,y});
}
const pads = await eda.pcb_PrimitivePad.getAll();
for (const p of pads) {
  const x=p.getState_X(), y=p.getState_Y();
  if (Math.hypot(x+5441.3,y-1560.4)<40) out.a.push({t:'pad',id:p.getState_PrimitiveId(),net:p.getState_Net(),x,y,layer:p.getState_Layer(),shape:p.getState_Pad?p.getState_Pad():null});
  if (Math.hypot(x-1781.5,y+3343.4)<40) out.b.push({t:'pad',id:p.getState_PrimitiveId(),net:p.getState_Net(),x,y,layer:p.getState_Layer()});
}
return out;
