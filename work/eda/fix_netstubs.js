const wires = ['863f90ed9caf4dfb','9cb7c2f331244096'];
await eda.sch_PrimitiveWire.delete(wires);
const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'U3');
const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
let n = 0;
for (const p of ps) {
  const num = String(p.getState_PinNumber());
  if (num === '38' || num === '39') {
    const ap = p.toAsync ? p.toAsync() : p;
    ap.setState_NoConnected(true);
    if (ap.done) await ap.done();
    n++;
  }
}
return { wires: wires.length, pins: n };
