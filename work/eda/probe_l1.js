const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
if (!c) return { missing: true };
const g = (f) => { try { return c[f] ? c[f]() : null; } catch(e) { return 'ERR'; } };
return {
  id: c.getState_PrimitiveId(),
  supplier: g('getState_Supplier'),
  supplierId: g('getState_SupplierId'),
  manufacturer: g('getState_Manufacturer'),
  component: g('getState_Component'),
  footprint: g('getState_Footprint'),
  value: g('getState_Value'),
  name: g('getState_Name'),
  keys: Object.getOwnPropertyNames(Object.getPrototypeOf(c)).filter(k => k.startsWith('getState_')).slice(0, 60)
};
