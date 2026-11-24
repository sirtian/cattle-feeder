const lines = await eda.pcb_PrimitiveLine.getAll();
const onOutline = lines.filter(l => l.getState_Layer() === 11);
const pts = onOutline.flatMap(l => [
  { x: l.getState_StartX(), y: l.getState_StartY() },
  { x: l.getState_EndX(), y: l.getState_EndY() }
]);
let bb = null;
if (pts.length) {
  const xs = pts.map(p => p.x), ys = pts.map(p => p.y);
  bb = { minx: Math.min(...xs), maxx: Math.max(...xs), miny: Math.min(...ys), maxy: Math.max(...ys) };
}
return { totalLines: lines.length, outlineLines: onOutline.length, bboxMil: bb,
  bboxMm: bb && { minx: bb.minx*0.0254, maxx: bb.maxx*0.0254, miny: bb.miny*0.0254, maxy: bb.maxy*0.0254 } };
