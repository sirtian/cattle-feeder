const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = vs.filter(v => Math.abs(v.getState_X()+4205.8)<2 && Math.abs(v.getState_Y()-2979.3)<2).map(v=>v.getState_PrimitiveId());
await eda.pcb_PrimitiveVia.delete(kill);
await eda.pcb_PrimitiveLine.delete(['88c3be866006b62a']);
const made=[];
made.push(await eda.pcb_PrimitiveLine.create('GND', 1, -4205.8, 2684.3, -4205.8, 2560, 8, false));
made.push(await eda.pcb_PrimitiveVia.create('GND', -4205.8, 2560, 12.2, 24));
await eda.pcb_PrimitiveVia.delete(['de8be7fbe4d9d385']);
return { created: made.filter(Boolean).length, killed: kill.length };
