const pts = [[900,645],[970,645],[900,655],[970,655],[480,455],[480,490],[560,455]];
const comps = await eda.sch_PrimitiveComponent.getAll();
const out = [];
for (const c of comps) {
  const d = c.getState_Designator(); if (!d) continue;
  const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    const x = p.getState_X(), y = p.getState_Y();
    for (const [qx,qy] of pts) {
      if (Math.abs(x-qx) < 15 && Math.abs(y-qy) < 15) out.push({ comp:d, pin:String(p.getState_PinNumber()), nc:p.getState_NoConnected(), x, y });
    }
  }
}
return out;
