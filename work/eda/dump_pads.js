const all = await eda.pcb_PrimitiveComponent.getAll();
const out = {};
for (const d of ['U33', 'U34']) {
  const c = all.find(x => x.getState_Designator() === d);
  const pads = await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(c.getState_PrimitiveId());
  out[d] = pads.map(p => {
    const num = p.getState_Number ? p.getState_Number() : p.getState_PadNumber();
    return { n: String(num), net: p.getState_Net(), x: +p.getState_X().toFixed(1), y: +p.getState_Y().toFixed(1),
      w: p.getState_Width ? +p.getState_Width().toFixed(1) : null, h: p.getState_Height ? +p.getState_Height().toFixed(1) : null };
  }).sort((a,b)=> Number(a.n)-Number(b.n));
}
return out;
