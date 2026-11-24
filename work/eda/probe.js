const t0 = Date.now();
const info = await eda.dmt_SelectControl.getCurrentDocumentInfo();
const comps = await eda.pcb_PrimitiveComponent.getAll();
const t1 = Date.now();
const sample = comps.slice(0, 5).map(c => ({
  id: c.getState_PrimitiveId(),
  d: c.getState_Designator(),
  x: c.getState_X(), y: c.getState_Y(),
  rot: c.getState_Rotation(), layer: c.getState_Layer()
}));
let busy = 0;
const b0 = Date.now();
while (Date.now() - b0 < 2000) { busy++; }
return { info, n: comps.length, sample, api_ms: t1 - t0, busy_ms: Date.now() - b0, ticks: busy };
