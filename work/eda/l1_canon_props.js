const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const dev = await eda.lib_Device.getByLcscIds(['C436568'], '0819f05c4eef4c71ace90d822a990e87', true);
const src = dev && dev[0] && dev[0].otherProperty ? dev[0].otherProperty : {};
const other = Object.assign({}, src);
delete other['Symbol']; delete other['Footprint']; delete other['Designator']; delete other['3D Model'];
await eda.sch_PrimitiveComponent.modify(c.getState_PrimitiveId(), {
  manufacturer: 'PROD(谱罗德)', manufacturerId: 'PSPMAA063T-100M-ANP',
  supplier: 'LCSC', supplierId: 'C436568', otherProperty: other
});
return { keys: Object.keys(other).length };
