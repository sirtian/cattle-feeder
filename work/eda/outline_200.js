const polys = await eda.pcb_PrimitivePolyline.getAll();
const ids = polys.filter(p => p.getState_Layer() === 11).map(p => p.getState_PrimitiveId());
if (ids.length) await eda.pcb_PrimitivePolyline.delete(ids);
const poly = eda.pcb_MathPolygon.createPolygon([240, -40, 'L', 440, -40, 440, -140, 240, -140, 240, -40]);
const pl = await eda.pcb_PrimitivePolyline.create('', 11, poly, 0.15, false);
return { deleted: ids.length, id: pl && pl.getState_PrimitiveId() };
