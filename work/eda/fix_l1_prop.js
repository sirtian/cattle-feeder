const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const other = Object.assign({}, c.getState_OtherProperty() || {});
delete other['EasyEDA Copilot Part Ref'];
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), {
  manufacturer: 'PROD(谱罗德)',
  manufacturerId: 'PSPMAA063T-100M-ANP',
  supplier: 'LCSC',
  supplierId: 'C436568',
  otherProperty: other
});
return { ok: true };
