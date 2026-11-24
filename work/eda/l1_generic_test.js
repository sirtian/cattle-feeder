const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), {
  manufacturer: '', manufacturerId: '', supplier: '', supplierId: ''
});
return { id: c.getState_PrimitiveId() };
