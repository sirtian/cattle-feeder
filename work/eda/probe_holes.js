const vs = await eda.pcb_PrimitiveVia.getAll();
const empt = vs.filter(v => !v.getState_Net());
const ids = ['e8','e10','e11','e12','e13','e14','e15','e5','e0'];
const byId = {};
for (const id of ids) {
  try { const r = await eda.pcb_PrimitiveVia.get([id]); if (r && r.length) byId[id] = { x: r[0].getState_X(), y: r[0].getState_Y(), net: r[0].getState_Net() }; } catch(e) {}
}
return { emptyCount: empt.length, sample: empt.slice(0,10).map(v => ({ x: v.getState_X(), y: v.getState_Y(), d: v.getState_Diameter ? v.getState_Diameter() : null, drill: v.getState_HoleDiameter ? v.getState_HoleDiameter() : null })), byId };
