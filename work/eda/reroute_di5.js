drc({ trackWidthMm: 0.2, minTrackWidthMm: 0.15, clearanceMm: 0.127, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_1" }, { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_2" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const nets = ["DI5","MCP_INT","MCP_P17","24V_P","GND"];
clearRouting({ nets, items: ["tracks", "vias"] });
signalNet("DI5", { priority: "high" }); signalNet("MCP_INT", { priority: "high" }); signalNet("MCP_P17", { priority: "high" });
signalNet("24V_P", { priority: "high" });
onlyNets("DI5","MCP_INT","MCP_P17","24V_P");
runAll();
