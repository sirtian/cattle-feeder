const W=8, VIA_H=12.2, VIA_D=24;
const items = [
  { pad: [-5426,1622], via: [-5426,1665] },
  { pad: [-5452,1622], via: [-5452,1695] },
  { pad: [-5503,1622], via: [-5503,1665] },
  { pad: [671,2034],   via: [567,1985] },
  { pad: [1614,1812],  via: [1655,1841] },
  { pad: [1746,1812],  via: [1807,1847] },
  { pad: [-4285,2716], via: [-4274,2840] },
  { pad: [-4336,2444], via: [-4316,2478] }
];
const made = [];
for (const it of items) {
  made.push(await eda.pcb_PrimitiveLine.create('GND', 1, it.pad[0], it.pad[1], it.via[0], it.via[1], W, false));
  made.push(await eda.pcb_PrimitiveVia.create('GND', it.via[0], it.via[1], VIA_H, VIA_D));
}
return { created: made.filter(Boolean).length };
