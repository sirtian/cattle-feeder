drc({ trackWidthMm: 0.15, minTrackWidthMm: 0.15, clearanceMm: 0.1, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" },
  { kind: "dielectric", thicknessMm: 1.6, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const nets = ["BMS_TX","CLK_SC","RST_SC","24V_SENSE","SPI_MOSI","MCP_INT","BMS_RX"];
clearRouting({ nets, items: ["tracks","vias"] });
signalNet("BMS_TX", { priority: "critical" });
signalNet("CLK_SC", { priority: "critical" });
signalNet("RST_SC", { priority: "critical" });
onlyNets("BMS_TX","CLK_SC","RST_SC");
runAll();
