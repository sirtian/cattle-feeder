const made=[];
made.push(await eda.pcb_PrimitiveLine.create('GND', 1, -1653.4, 1118.9, -1681.6, 1129.2, 8, false));
made.push(await eda.pcb_PrimitiveVia.create('GND', -1681.6, 1129.2, 12.2, 24));
return { created: made.filter(Boolean).length };
