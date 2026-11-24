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
ignoreNets("GND");
runAll();
