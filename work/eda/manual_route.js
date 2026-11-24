const W = 8;      // 0.2 mm
const VIA_H = 12.2, VIA_D = 24;
const L_TOP = 1, L_BOT = 2;
async function trk(net, layer, a, b) {
  if (a[0] === b[0] && a[1] === b[1]) return null;
  return await eda.pcb_PrimitiveLine.create(net, layer, a[0], a[1], b[0], b[1], W, false);
}
async function via(net, p) {
  return await eda.pcb_PrimitiveVia.create(net, p[0], p[1], VIA_H, VIA_D);
}
const made = [];
// MCP_P15: U33.6 (1007.1,403.6) -> U34.6 (2896.4,1139.4)
made.push(await trk('MCP_P15', L_TOP, [1007.1,403.6], [1007,470]));
made.push(await via('MCP_P15', [1007,470]));
made.push(await trk('MCP_P15', L_BOT, [1007,470], [1007,-1200]));
made.push(await trk('MCP_P15', L_BOT, [1007,-1200], [2896,-1200]));
made.push(await trk('MCP_P15', L_BOT, [2896,-1200], [2896,1160]));
made.push(await via('MCP_P15', [2896,1160]));
made.push(await trk('MCP_P15', L_TOP, [2896,1160], [2896.4,1139.4]));
// MCP_P14: U33.5 (1032.7,403.6) -> U34.5 (2946.5,1139.4)
made.push(await trk('MCP_P14', L_TOP, [1032.7,403.6], [1032,540]));
made.push(await via('MCP_P14', [1032,540]));
made.push(await trk('MCP_P14', L_BOT, [1032,540], [1032,-1250]));
made.push(await trk('MCP_P14', L_BOT, [1032,-1250], [2946,-1250]));
made.push(await trk('MCP_P14', L_BOT, [2946,-1250], [2946,1160]));
made.push(await via('MCP_P14', [2946,1160]));
made.push(await trk('MCP_P14', L_TOP, [2946,1160], [2946.5,1139.4]));
return { created: made.filter(Boolean).length, total: made.length };
