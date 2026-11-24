const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const ps = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
const wires = await eda.sch_PrimitiveWire.getAll();
const wpts = [];
for (const w of wires) { const line = w.getState_Line() || []; for (let i=0;i+1<line.length;i+=2) wpts.push({ x: line[i], y: line[i+1], net: w.getState_Net() }); }
const out = [];
for (const p of ps) {
  const x = p.getState_X(), y = p.getState_Y();
  const hit = wpts.find(q => Math.abs(q.x-x)<6 && Math.abs(q.y-y)<6);
  out.push({ pin: String(p.getState_PinNumber()), x, y, net: hit ? hit.net : null });
}
return out;
