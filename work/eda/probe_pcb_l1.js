const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
if (!c) return { missing: true };
return { id: c.getState_PrimitiveId(), x: c.getState_X(), y: c.getState_Y(), rot: c.getState_Rotation(),
  fp: c.getState_Footprint ? c.getState_Footprint() : null, comp: c.getState_Component ? c.getState_Component() : null,
  uniqueId: c.getState_UniqueId ? c.getState_UniqueId() : null };
