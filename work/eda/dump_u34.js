const all = await eda.pcb_PrimitiveComponent.getAll();
const c = all.find(x => x.getState_Designator() === 'U34');
const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
return pads.map(p => {
  const num = p.getState_Number ? p.getState_Number() : p.getState_PadNumber();
  return [String(num), p.getState_Net(), +p.getState_X().toFixed(0), +p.getState_Y().toFixed(0)];
}).sort((a,b)=>Number(a[0])-Number(b[0]));
