const pours = await eda.pcb_PrimitivePour.getAll('GND');
const out = [];
for (const p of pours) {
  const r = await p.rebuildCopperRegion();
  out.push({ id: p.getState_PrimitiveId(), layer: p.getState_Layer(), ok: !!r });
}
return { rebuilt: out.length, out };
