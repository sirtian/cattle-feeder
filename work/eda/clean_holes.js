const keep = new Set(['5f450bab454a1933','90abddbd126e07bd','eeffb278153e5684','951419ceb5ecae09']);
const pads = await eda.pcb_PrimitivePad.getAll();
const kill = [];
for (const p of pads) {
  const net = p.getState_Net ? p.getState_Net() : null;
  const lay = p.getState_Layer ? p.getState_Layer() : null;
  if (net) continue;
  if (lay !== 12) continue;
  const id = p.getState_PrimitiveId();
  if (!keep.has(id)) kill.push(id);
}
if (kill.length) await eda.pcb_PrimitivePad.delete(kill);
return { deleted: kill.length, kept: [...keep] };
