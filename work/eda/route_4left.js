drc({ trackWidthMm: 0.2, minTrackWidthMm: 0.15, clearanceMm: 0.127, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" },
  { kind: "dielectric", thicknessMm: 1.6, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const nets = ["AIN1","BMS_TX","CLK_SC","RST_SC"];
for (const n of nets) signalNet(n, { priority: "critical" });
onlyNets(...nets);
runAll();
