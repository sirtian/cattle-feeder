const all = await eda.pcb_PrimitiveComponent.getAll();
const c = all.find(x => x.getState_Designator() === 'U33');
const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
const p3 = pads.find(p => String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()) === '3');
const c34 = all.find(x => x.getState_Designator() === 'U34');
return {
  u33: { x: c.getState_X(), y: c.getState_Y(), rot: c.getState_Rotation() },
  u34: { x: c34.getState_X(), y: c34.getState_Y(), rot: c34.getState_Rotation() },
  pad3: { x: p3.getState_X(), y: p3.getState_Y() },
  c1: (() => { const c1 = all.find(x => x.getState_Designator() === 'C1'); return { x: c1.getState_X(), y: c1.getState_Y() }; })()
};
