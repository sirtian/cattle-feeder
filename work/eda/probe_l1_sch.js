const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
if (!c) return { missing: true };
return { id: c.getState_PrimitiveId(),
  uniqueId: c.getState_UniqueId ? c.getState_UniqueId() : null,
  footprint: c.getState_Footprint ? c.getState_Footprint() : null,
  component: c.getState_Component ? c.getState_Component() : null };
