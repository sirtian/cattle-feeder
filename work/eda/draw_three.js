const W=8;
const made=[];
made.push(await eda.pcb_PrimitiveLine.create("BMS_TX", 1, -4958.2, 1556.3, -4753.7, 1555, W, false));
made.push(await eda.pcb_PrimitiveLine.create("CLK_SC", 1, -5035, 1556.3, 3246.8, 1854.8, W, false));
made.push(await eda.pcb_PrimitiveLine.create("RST_SC", 1, -5262, 1011.5, -5122.7, 1011.5, W, false));
made.push(await eda.pcb_PrimitiveLine.create("RST_SC", 1, -5122.7, 1011.5, -5009.4, 1556.3, W, false));
return { created: made.filter(Boolean).length };