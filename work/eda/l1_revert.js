const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const other = Object.assign({}, c.getState_OtherProperty() || {});
delete other['Value'];
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), { name: null, otherProperty: other });
return { name: (await eda.sch_PrimitiveComponent.get([c.getState_PrimitiveId()]))[0].getState_Name() };
