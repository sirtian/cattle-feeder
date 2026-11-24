const nets = ['CHARGE_INT','GATE_CURR_L','GATE_CURR_R'];
const ws = await eda.sch_PrimitiveWire.getAll();
const out = [];
for (const w of ws) {
  const n = w.getState_Net();
  if (nets.includes(n)) out.push({ net: n, line: w.getState_Line(), id: w.getState_PrimitiveId() });
}
return out;
