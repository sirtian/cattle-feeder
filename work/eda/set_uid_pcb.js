const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
await eda.pcb_PrimitiveComponent.modify(c.getState_PrimitiveId(), { uniqueId: 'L1-P10A-01' });
return { ok: true };
