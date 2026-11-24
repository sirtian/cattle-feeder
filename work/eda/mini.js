board.roundedRect(160, 100, { radius: 3, layers: ["top", "bottom"], defaultLayer: "top", clearance: 0.25, edge: 0.5 });
block("B1", ["R1", "C1"]);
block("B2", ["J1"]);
fixed("J1", { x: -70, y: 0, rotate: 0, layer: "top" });
solver({ grid: 1, ignoredSignals: ["GND"] });
