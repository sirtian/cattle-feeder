drc({ trackWidthMm: 0.2, minTrackWidthMm: 0.15, clearanceMm: 0.127, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_1" }, { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_2" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const nets = ["MCP_P10","MCP_P11","MCP_P12","MCP_P13","MCP_P14","MCP_P15","MCP_P16","MCP_P17",
  "COIL2_1","COIL2_2","COIL2_3","COIL2_4","COIL2_5","COIL2_6","COIL2_7","COIL2_8","24V_P"];
clearRouting({ nets, items: ["tracks", "vias"] });
for (const n of nets) signalNet(n, { priority: "high" });
onlyNets(...nets);
runAll();
