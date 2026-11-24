const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
if (!c) return { missing: true };
const x = c.getState_X(), y = c.getState_Y(), rot = c.getState_Rotation(), mir = c.getState_Mirror();
const id = c.getState_PrimitiveId();
const nc = await eda.sch_PrimitiveComponent.create(
  { libraryUuid: '0819f05c4eef4c71ace90d822a990e87', uuid: '2a16b44b218c4dfd96372a3decfe44ee' },
  x, y, undefined, rot, mir, true, true
);
if (!nc) return { created: false };
await eda.sch_PrimitiveComponent.modify(nc.getState_PrimitiveId(), { designator: 'L1' });
await eda.sch_PrimitiveComponent.delete([id]);
return { created: true, x, y, rot, mir };
