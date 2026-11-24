drc({ trackWidthMm: 0.2, minTrackWidthMm: 0.15, clearanceMm: 0.127, edgeClearanceMm: 0.3, via: { diameterMm: 0.61, drillMm: 0.31 } });
stack({ boardThicknessMm: 1.6, fallbackCopperThicknessOz: 1, layers: [
  { kind: "copper", name: "TOP" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_1" }, { kind: "dielectric", thicknessMm: 0.9, relativePermittivity: 4.4 },
  { kind: "copper", name: "INNER_2" }, { kind: "dielectric", thicknessMm: 0.2, relativePermittivity: 4.4 },
  { kind: "copper", name: "BOTTOM" } ] });
const nets = ["AIN1_F","AIN1","SPI_SCK","ADS_DRDY","AIN0","VREF","SPI_MOSI",
  "MCP_P10","MCP_P11","MCP_P12","MCP_P13","MCP_P14","MCP_P15","MCP_P16","MCP_P17",
  "3V3","I2C_SCL","I2C_SDA","RS485_RX","SD_CS"];
clearRouting({ nets, items: ["tracks", "vias"] });
runCopper();
