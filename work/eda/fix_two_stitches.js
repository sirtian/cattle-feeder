// remove old C86 and U33.10 stitches
const lines = ['b799b39dc8488cb4','2baa93b96943b7b2'];
await eda.pcb_PrimitiveLine.delete(lines);
const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = vs.filter(v => (Math.abs(v.getState_X()+2457.8)<2 && Math.abs(v.getState_Y()-1067.3)<2) || (Math.abs(v.getState_X()+4205.8)<2 && Math.abs(v.getState_Y()-2560)<2)).map(v=>v.getState_PrimitiveId());
await eda.pcb_PrimitiveVia.delete(kill);
const made=[];
// U33.10 -> U33.17 GND pad inside body
made.push(await eda.pcb_PrimitiveLine.create('GND', 1, -4205.8, 2684.3, -4257, 2412.3, 8, false));
return { killed: kill.length, created: made.filter(Boolean).length };
