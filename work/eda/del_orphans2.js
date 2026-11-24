const coords = [[-1535.4,1063.0],[3907.9,1259.6],[844.4,1031.1],[-5787.4,1063.0]];
const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = [];
for (const v of vs) {
  if (v.getState_Net() !== 'GND') continue;
  const x = v.getState_X(), y = v.getState_Y();
  for (const [cx,cy] of coords) if (Math.abs(x-cx)<2 && Math.abs(y-cy)<2) { kill.push(v.getState_PrimitiveId()); break; }
}
if (kill.length) await eda.pcb_PrimitiveVia.delete(kill);
return { killed: kill.length };
