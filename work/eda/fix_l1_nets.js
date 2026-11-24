const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
const out = [];
for (const p of pads) {
  const n = String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber());
  const net = n === '1' ? 'SW' : (n === '2' ? '5V' : null);
  if (net) { const ap = p.toAsync ? p.toAsync() : p; ap.setState_Net(net); if (ap.done) await ap.done(); out.push(n + ':' + net); }
}
return out;
