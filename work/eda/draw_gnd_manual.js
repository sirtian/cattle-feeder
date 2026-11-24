const W=8, VIA_H=12.2, VIA_D=24;
const made=[];
const man=[
  [[-5426,1622],[-5426,1668]], [[-5452,1622],[-5452,1698]], [[-5503,1622],[-5503,1668]],
  [[-4285,2716],[-4285,2760]], [[-4336,2444],[-4336,2400]], [[671,2034],[671,2072]]
];
for (const it of man) {
  made.push(await eda.pcb_PrimitiveLine.create("GND", 1, it[0][0], it[0][1], it[1][0], it[1][1], W, false));
  made.push(await eda.pcb_PrimitiveVia.create("GND", it[1][0], it[1][1], VIA_H, VIA_D));
}
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1614.3, 1812, 1606.0, 1812.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1606.0, 1812.0, 1606.0, 1912.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1606.0, 1912.0, 1606, 1911, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1746.1, 1812, 1746.0, 1827.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1746.0, 1827.0, 1751.0, 1827.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1751.0, 1827.0, 1751.0, 1832.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1751.0, 1832.0, 1756.0, 1832.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1756.0, 1832.0, 1756.0, 1837.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1756.0, 1837.0, 1761.0, 1837.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1761.0, 1837.0, 1761.0, 1842.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1761.0, 1842.0, 1766.0, 1842.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1766.0, 1842.0, 1766.0, 1847.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1766.0, 1847.0, 1771.0, 1847.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1771.0, 1847.0, 1771.0, 1852.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1771.0, 1852.0, 1826.0, 1852.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1826.0, 1852.0, 1826.0, 1857.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1826.0, 1857.0, 1831.0, 1857.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1831.0, 1857.0, 1831.0, 1862.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1831.0, 1862.0, 1836.0, 1862.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1836.0, 1862.0, 1836.0, 1892.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1836.0, 1892.0, 1831.0, 1892.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1831.0, 1892.0, 1831.0, 1897.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1831.0, 1897.0, 1666.0, 1897.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1666.0, 1897.0, 1666.0, 1892.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1666.0, 1892.0, 1661.0, 1892.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1661.0, 1892.0, 1661.0, 1887.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1661.0, 1887.0, 1606.0, 1887.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1606.0, 1887.0, 1606.0, 1912.0, W, false));
made.push(await eda.pcb_PrimitiveLine.create("GND", 1, 1606.0, 1912.0, 1606, 1911, W, false));
return { created: made.filter(Boolean).length };