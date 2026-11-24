const out={};
const lines = await eda.pcb_PrimitiveLine.getAll();
const kl = lines.filter(l => l.getState_Net()==='GND' && Math.hypot((l.getState_StartX()+l.getState_EndX())/2+5622.4,(l.getState_StartY()+l.getState_EndY())/2-1500.4)<15).map(l=>l.getState_PrimitiveId());
const vs = await eda.pcb_PrimitiveVia.getAll();
const kv = vs.filter(v => v.getState_Net()==='GND' && Math.hypot(v.getState_X()+4133.9, v.getState_Y()-1299.2)<15).map(v=>v.getState_PrimitiveId());
if (kl.length) await eda.pcb_PrimitiveLine.delete(kl);
if (kv.length) await eda.pcb_PrimitiveVia.delete(kv);
return { lines: kl.length, vias: kv.length };
