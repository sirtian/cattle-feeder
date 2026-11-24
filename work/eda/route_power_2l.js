drc({
  trackWidthMm: 0.25,
  minTrackWidthMm: 0.15,
  clearanceMm: 0.15,
  edgeClearanceMm: 0.3,
  via: { diameterMm: 0.61, drillMm: 0.31 },
});
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" },
  { kind: "dielectric", thicknessMm: 1.6, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
powerNet("24V_P", { maxCurrentA: 1.4, maxTempRiseC: 10, maxTrackWidthMm: 1.5, priority: "high" });
powerNet("5V", { maxCurrentA: 1.4, maxTempRiseC: 10, maxTrackWidthMm: 1.5, priority: "high" });
powerNet("3V3", { maxCurrentA: 0.8, maxTempRiseC: 10, maxTrackWidthMm: 1.0, priority: "high" });
onlyNets("24V_P", "5V", "3V3");
runAll();
