const comps = await eda.pcb_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
if (!c) return { missing: true };
const x = c.getState_X(), y = c.getState_Y(), rot = c.getState_Rotation(), layer = c.getState_Layer();
await eda.pcb_PrimitiveComponent.delete([c.getState_PrimitiveId()]);
const nc = await eda.pcb_PrimitiveComponent.create(
  { libraryType: '4', libraryUuid: '0819f05c4eef4c71ace90d822a990e87', uuid: '0a956972613a413195dd8939923f26c4' },
  layer, x, y, rot, false
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
return { created: true, x, y, rot, layer, set };
