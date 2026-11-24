const all = await eda.pcb_PrimitiveComponent.getAll();
const j = all.find(c => c.getState_Designator() === 'J1');
if (!j) throw new Error('J1 not found');
const id = j.getState_PrimitiveId();
const cx = 340 / 0.0254, cy = -90 / 0.0254;
await eda.pcb_PrimitiveComponent.modify(id, { x: cx - 77 / 0.0254, y: cy - 47 / 0.0254, rotation: 0 });
const back = (await eda.pcb_PrimitiveComponent.getAll()).find(c => c.getState_PrimitiveId() === id);
return { id, x: back.getState_X(), y: back.getState_Y(), rot: back.getState_Rotation() };
