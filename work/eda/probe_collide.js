const pts = [[2803,1812],[2992,1834],[3616,1842],[3715,1842]];
const all = await eda.pcb_PrimitiveComponent.getAll();
const out = [];
for (const c of all) {
  const ps = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  for (const p of ps) {
    if (p.getState_Net()) continue;
    const px = p.getState_X(), py = p.getState_Y();
    for (const [qx,qy] of pts) {
      const d = Math.hypot(px-qx, py-qy);
      if (d < 40) out.push({ comp: c.getState_Designator(), pad: String(p.getState_Number ? p.getState_Number() : p.getState_PadNumber()), x: +px.toFixed(0), y: +py.toFixed(0), d: +d.toFixed(1) });
    }
  }
}
return out;
