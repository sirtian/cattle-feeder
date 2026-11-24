const comps = await eda.pcb_PrimitiveComponent.getAll();
const out = [];
for (const [d,x,y] of [['C78',-5350,1480],['C79',-5290,1480]]) {
  const c = comps.find(z => z.getState_Designator() === d);
  if (!c) { out.push({d,missing:true}); continue; }
  await eda.pcb_PrimitiveComponent.modify(c.getState_PrimitiveId(), { x, y });
  out.push({d,x,y});
}
return out;
