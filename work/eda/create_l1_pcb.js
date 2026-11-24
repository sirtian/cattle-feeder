const all = await eda.pcb_PrimitiveComponent.getAll();
const exists = all.find(x => x.getState_Designator() === 'L1');
if (exists) return { already: true, id: exists.getState_PrimitiveId() };
const nc = await eda.pcb_PrimitiveComponent.create(
  { libraryUuid: '0819f05c4eef4c71ace90d822a990e87', uuid: '2a16b44b218c4dfd96372a3decfe44ee' },
  1, 0, 0, 0, false
);
if (!nc) return { created: false };
await eda.pcb_PrimitiveComponent.modify(nc.getState_PrimitiveId(), { designator: 'L1' });
const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(nc.getState_PrimitiveId());
const set = [];
for (const p of pads) {
  const n = String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber());
  const net = n === '1' ? '5V' : (n === '2' ? 'SW' : null);
  if (net) { const ap = p.toAsync ? p.toAsync() : p; ap.setState_Net(net); if (ap.done) await ap.done(); set.push(n + ':' + net); }
}
return { created: true, id: nc.getState_PrimitiveId(), set };
