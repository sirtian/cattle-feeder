const vs = await eda.pcb_PrimitiveVia.getAll();
const kill = vs.filter(v => v.getState_Net()==='GND' && Math.abs(v.getState_X()-4063.8)<3 && Math.abs(v.getState_Y()-1303.2)<3).map(v=>v.getState_PrimitiveId());
if (kill.length) await eda.pcb_PrimitiveVia.delete(kill);
return { killed: kill.length };
