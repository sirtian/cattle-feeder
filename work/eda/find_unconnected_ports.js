const comps = await eda.sch_PrimitiveComponent.getAll();
const ports = comps.filter(c => (c.getState_ComponentType ? c.getState_ComponentType() : '') === 'netport');
if (!ports.length) return [];
const wires = await eda.sch_PrimitiveWire.getAll();
const pts = [];
for (const w of wires) {
  const line = w.getState_Line() || [];
  for (let i = 0; i + 1 < line.length; i += 2) pts.push([line[i], line[i+1]]);
}
const out = [];
for (const p of ports) {
  const x = p.getState_X(), y = p.getState_Y();
  let hit = false;
  for (const [qx,qy] of pts) if (Math.abs(qx-x) < 8 && Math.abs(qy-y) < 8) { hit = true; break; }
  if (!hit) out.push({ id: p.getState_PrimitiveId(), x, y, name: p.getState_Name ? p.getState_Name() : null });
}
return out;
