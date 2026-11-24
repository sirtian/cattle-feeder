const comps = await eda.sch_PrimitiveComponent.getAll();
const out = [];
for (const c of comps) {
  const d = c.getState_Designator();
  if (!d) continue;
  const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  const nc = ps.filter(p => p.getState_NoConnected && p.getState_NoConnected()).map(p => String(p.getState_PinNumber()));
  if (nc.length) out.push({ d, nc });
}
return out;
