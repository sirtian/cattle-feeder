const W=8, VIA_H=12.2, VIA_D=24;
const made=[];
made.push(await eda.pcb_PrimitiveLine.create('MCP_P16', 1, -4129.1, 2684.3, -4129.1, 2770, W, false));
made.push(await eda.pcb_PrimitiveVia.create('MCP_P16', -4129.1, 2770, VIA_H, VIA_D));
made.push(await eda.pcb_PrimitiveLine.create('MCP_P16', 16, -4129.1, 2770, -4771.3, 2770, W, false));
made.push(await eda.pcb_PrimitiveVia.create('MCP_P16', -4771.3, 2770, VIA_H, VIA_D));
made.push(await eda.pcb_PrimitiveLine.create('MCP_P16', 1, -4771.3, 2770, -4771.3, 2682.7, W, false));
return { created: made.filter(Boolean).length };
