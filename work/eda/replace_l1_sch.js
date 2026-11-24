const comps = await eda.sch_PrimitiveComponent.getAll();
const old = comps.find(x => x.getState_Designator() === 'L1');
const x = old.getState_X(), y = old.getState_Y(), rot = old.getState_Rotation(), mir = old.getState_Mirror();
await eda.sch_PrimitiveComponent.delete([old.getState_PrimitiveId()]);
const nc = await eda.sch_PrimitiveComponent.create(
  { libraryUuid: '0819f05c4eef4c71ace90d822a990e87', uuid: '70064afff7a24b0ca09f576b54ed848e' },
  x, y, undefined, rot, mir, true, true
);
await eda.sch_PrimitiveComponent.modify(nc.getState_PrimitiveId(), { designator: 'L1' });
const back = (await eda.sch_PrimitiveComponent.getAll()).find(z => z.getState_PrimitiveId() === nc.getState_PrimitiveId());
return { id: back.getState_PrimitiveId(), uniqueId: back.getState_UniqueId ? back.getState_UniqueId() : null,
  fp: back.getState_Footprint ? back.getState_Footprint() : null };
