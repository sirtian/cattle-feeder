const pours = await eda.pcb_PrimitivePour.getAll('GND');
const res = [];
for (const p of pours) {
  const id = p.getState_PrimitiveId();
  await eda.pcb_PrimitivePour.modify(id, { preserveSilos: false });
  const back = (await eda.pcb_PrimitivePour.getAll('GND')).find(x => x.getState_PrimitiveId() === id);
  res.push({ id, layer: back.getState_Layer(), preserveSilos: back.getState_PreserveSilos() });
}
return { count: pours.length, res };
