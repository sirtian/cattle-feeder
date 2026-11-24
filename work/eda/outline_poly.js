const lines = await eda.pcb_PrimitiveLine.getAll();
const ids = lines.filter(l => l.getState_Layer() === 11).map(l => l.getState_PrimitiveId());
await eda.pcb_PrimitiveLine.delete(ids);
const poly = eda.pcb_MathPolygon.createPolygon([260, -40, 'L', 420, -40, 420, -140, 260, -140, 260, -40]);
const pl = await eda.pcb_PrimitivePolyline.create('', 11, poly, 0.15, false);
const all = await eda.pcb_PrimitivePolyline.getAll();
return { deleted: ids.length, id: pl && pl.getState_PrimitiveId(), type: pl && pl.getState_PrimitiveType(), nPoly: all.length };
