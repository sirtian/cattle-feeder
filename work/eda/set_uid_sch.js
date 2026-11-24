const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), { uniqueId: 'L1-P10A-01' });
return { ok: true };
