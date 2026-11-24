drc({ trackWidthMm: 0.2, minTrackWidthMm: 0.15, clearanceMm: 0.127, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_1" }, { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_2" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const blockers = ["MCP_P16","3V3","SD_CS","SPI_MOSI","SPI_SCK","RS485_TX","RS485_RX"];
clearRouting({ nets: blockers, items: ["tracks", "vias"] });
signalNet("MCP_P16", { priority: "critical" });
onlyNets("MCP_P16");
runAll();
