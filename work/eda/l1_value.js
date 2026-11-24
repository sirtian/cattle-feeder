const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const other = Object.assign({}, c.getState_OtherProperty() || {}, { Value: '10uH' });
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), { name: '10uH', otherProperty: other });
return { ok: true };
