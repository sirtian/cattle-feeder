drc({ trackWidthMm: 0.25, minTrackWidthMm: 0.15, clearanceMm: 0.15, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({
  boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1,
  layers: [
    { kind: "copper", name: "TOP" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
    { kind: "copper", name: "INNER_1" }, { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
    { kind: "copper", name: "INNER_2" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
    { kind: "copper", name: "BOTTOM" },
  ],
});
signalNet("24V_P", { priority: "critical" });
signalNet("3V3", { priority: "critical" });
signalNet("24V_SENSE", { priority: "critical" });
signalNet("48V_SENSE", { priority: "critical" });
onlyNets("24V_P", "3V3", "24V_SENSE", "48V_SENSE");
runAll();
