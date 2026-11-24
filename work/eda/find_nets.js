const nets = ['CHARGE_INT','GATE_CURR_L','GATE_CURR_R'];
const comps = await eda.sch_PrimitiveComponent.getAll();
const hits = [];
for (const c of comps) {
  const d = c.getState_Designator();
  if (!d) continue;
  const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    const net = p.getState_Net ? p.getState_Net() : null;
    if (nets.includes(net)) hits.push({ comp: d, pin: String(p.getState_PinNumber()), net, nc: p.getState_NoConnected() });
  }
}
return hits;
