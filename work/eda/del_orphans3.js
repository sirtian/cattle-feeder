const coords = [[-4513.0,1420.3],[-5315.0,1299.2],[1299.2,1771.7]];
const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = [];
for (const v of vs) {
  if (v.getState_Net() !== 'GND') continue;
  const x = v.getState_X(), y = v.getState_Y();
  for (const [cx,cy] of coords) if (Math.abs(x-cx)<3 && Math.abs(y-cy)<3) { kill.push(v.getState_PrimitiveId()); break; }
}
if (kill.length) await eda.pcb_PrimitiveVia.delete(kill);
return { killed: kill.length };
