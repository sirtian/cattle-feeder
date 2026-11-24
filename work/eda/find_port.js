const comps = await eda.sch_PrimitiveComponent.getAll();
const out = [];
for (const c of comps) {
  const n = c.getState_Name ? c.getState_Name() : null;
  const u = c.getState_UniqueId ? c.getState_UniqueId() : null;
  const d = c.getState_Designator ? c.getState_Designator() : null;
  if ((n && String(n).includes('17I8')) || (u && String(u).includes('17I8'))) out.push({ d, n, u, x: c.getState_X(), y: c.getState_Y(), type: c.getState_ComponentType && c.getState_ComponentType() });
}
return out;
