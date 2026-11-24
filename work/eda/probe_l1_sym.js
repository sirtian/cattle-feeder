const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const dev = await eda.lib_Device.get('bb962029a175660d', '0819f05c4eef4c71ace90d822a990e87');
const canon = await eda.lib_Device.get('2a16b44b218c4dfd96372a3decfe44ee', '0819f05c4eef4c71ace90d822a990e87');
const pick = (o) => o && ({ name: o.name || o.deviceName, symbol: o.symbolUuid || (o.otherProperty && o.otherProperty['Symbol']), footprint: o.footprintUuid || (o.otherProperty && o.otherProperty['Footprint']) });
return { compSym: c.getState_Symbol(), dev: pick(dev), canon: pick(canon) };
