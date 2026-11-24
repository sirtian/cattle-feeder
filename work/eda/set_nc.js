const want = {
  U44: ['1','3','4'], J43: ['1','8','9'], U45: ['5'],
  U40: ['1','2','7','12','15','16','17','18','19','20','21','25','26','27','28'],
  U37: ['12','13','18','25','26','27','28'],
  U3: ['15','23','26','28','29','30','33','34','35'],
  J3: ['B8','A8'],
  U33: ['11','14','19','23','24','25','26','27','28'],
  U1: ['4']
};
const comps = await eda.sch_PrimitiveComponent.getAll();
const done = [];
for (const [d, pins] of Object.entries(want)) {
  const c = comps.find(x => x.getState_Designator() === d);
  if (!c) continue;
  const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    const num = String(p.getState_PinNumber());
    if (!pins.includes(num)) continue;
    const ap = p.toAsync ? p.toAsync() : p;
    ap.setState_NoConnected(true);
    if (ap.done) await ap.done();
    done.push(d + '.' + num);
  }
}
return done;
