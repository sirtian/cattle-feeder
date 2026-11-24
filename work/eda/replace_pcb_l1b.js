const comps = await eda.pcb_PrimitiveComponent.getAll();
const old = comps.find(x => x.getState_Designator() === 'L1');
const x = old.getState_X(), y = old.getState_Y(), rot = old.getState_Rotation();
await eda.pcb_PrimitiveComponent.delete([old.getState_PrimitiveId()]);
const nc = await eda.pcb_PrimitiveComponent.create(
  { libraryUuid: '0819f05c4eef4c71ace90d822a990e87', uuid: '70064afff7a24b0ca09f576b54ed848e' },
  1, x, y, rot, false
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
const back = (await eda.pcb_PrimitiveComponent.getAll()).find(z => z.getState_PrimitiveId() === nc.getState_PrimitiveId());
return { created: true, comp: back.getState_Component ? back.getState_Component() : null, fp: back.getState_Footprint ? back.getState_Footprint() : null, set };
