await eda.sch_PrimitiveWire.delete(['f601ac775eeb4370']);
const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'J50');
const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
let n = 0;
for (const p of ps) {
  if (String(p.getState_PinNumber()) === '1') {
    const ap = p.toAsync ? p.toAsync() : p;
    ap.setState_NoConnected(true);
    if (ap.done) await ap.done();
    n++;
  }
}
return { pins: n };
