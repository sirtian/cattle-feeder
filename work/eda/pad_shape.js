const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'U33');
const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
const p = ps.find(q => String(q.getState_Number ? q.getState_Number() : q.getState_PadNumber()) === '7');
return { shape: p.getState_Pad ? p.getState_Pad() : null, hole: p.getState_Hole ? p.getState_Hole() : null, rot: p.getState_Rotation ? p.getState_Rotation() : null };
