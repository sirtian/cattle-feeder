const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'U34');
if (!c) return { missing: true };
const x = c.getState_X(), y = c.getState_Y(), rot = c.getState_Rotation();
const nx = x - 78.74; // 2 mm west
await eda.pcb_PrimitiveComponent.modify(c.getState_PrimitiveId(), { x: nx });
const back = (await eda.pcb_PrimitiveComponent.getAll()).find(z => z.getState_PrimitiveId() === c.getState_PrimitiveId());
return { from: [x, y], to: [back.getState_X(), back.getState_Y()], rot };
