const comps = await eda.sch_PrimitiveComponent.getAll();
const out = [];
for (const c of comps) {
  const d = c.getState_Designator ? c.getState_Designator() : null;
  if (d) continue;
  out.push({ name: c.getState_Name ? c.getState_Name() : null, type: c.getState_ComponentType ? c.getState_ComponentType() : null,
    x: c.getState_X ? c.getState_X() : null, y: c.getState_Y ? c.getState_Y() : null,
    id: c.getState_PrimitiveId ? c.getState_PrimitiveId() : null,
    comp: c.getState_Component ? c.getState_Component() : null });
}
return out;
