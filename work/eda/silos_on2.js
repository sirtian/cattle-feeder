const pours = await eda.pcb_PrimitivePour.getAll('GND');
const out = [];
for (const p of pours) {
  const id = p.getState_PrimitiveId();
  await eda.pcb_PrimitivePour.modify(id, { preserveSilos: true });
  const back = (await eda.pcb_PrimitivePour.getAll('GND')).find(x => x.getState_PrimitiveId() === id);
  out.push({ id, layer: back.getState_Layer(), silos: back.getState_PreserveSilos() });
}
return out;
