drc({
  trackWidthMm: 0.2,
  minTrackWidthMm: 0.15,
  clearanceMm: 0.15,
  edgeClearanceMm: 0.3,
  via: { diameterMm: 0.5, drillMm: 0.3 },
});
stack({
  boardThicknessMm: 1.6,
  fallbackCopperThicknessOz: 1,
  layers: [
    { kind: "copper", name: "TOP" },
    { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
    { kind: "copper", name: "INNER_1" },
    { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
    { kind: "copper", name: "INNER_2" },
    { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
    { kind: "copper", name: "BOTTOM" },
  ],
});
const bus = ["MCP_P10","MCP_P11","MCP_P12","MCP_P13","MCP_P14","MCP_P15","MCP_P16","MCP_P17"];
clearRouting({ nets: bus, items: ["tracks", "vias"] });
for (const n of bus) signalNet(n, { priority: "high", allowedLayers: ["TOP", "INNER_1", "INNER_2", "BOTTOM"] });
onlyNets(...bus);
runAll();
