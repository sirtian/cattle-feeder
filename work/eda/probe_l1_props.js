const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
return { manufacturer: c.getState_Manufacturer(), manufacturerId: c.getState_ManufacturerId(),
  supplier: c.getState_Supplier(), supplierId: c.getState_SupplierId(),
  other: c.getState_OtherProperty() };
