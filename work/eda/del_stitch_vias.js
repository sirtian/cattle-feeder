const coords = [[-5382.8,1452.4],[-5677.1,1333.5],[-2394.4,951.0],[-5073.6,1256.7],[3870.0,1023.9],
  [-5422,1499],[-5547,1802],[-5677,1333],[-1915,1212],[-2394,951],[-2458,1067],[-5079,1263],[3870,1024],[877,1296],[-4206,2979],[-4205.8,2560],[-1681.6,1129.2]];
const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = [];
for (const v of vs) {
  if (v.getState_Net() !== 'GND') continue;
  const x = v.getState_X(), y = v.getState_Y();
  for (const [cx,cy] of coords) if (Math.abs(x-cx)<3 && Math.abs(y-cy)<3) { kill.push(v.getState_PrimitiveId()); break; }
}
if (kill.length) await eda.pcb_PrimitiveVia.delete(kill);
return { deleted: kill.length };
