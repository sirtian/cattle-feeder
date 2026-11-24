const all = await eda.pcb_PrimitiveComponent.getAll();
const c = all.find(x => x.getState_Designator() === 'U37');
const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
return { x: c.getState_X(), y: c.getState_Y(), rot: c.getState_Rotation(),
  pads: ps.map(p => ({ n: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()), net: p.getState_Net(), x: +p.getState_X().toFixed(0), y: +p.getState_Y().toFixed(0) })).sort((a,b)=>Number(a.n)-Number(b.n)) };
