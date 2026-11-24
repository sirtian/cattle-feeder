const pours = await eda.pcb_PrimitivePour.getAll('GND');
for (const p of pours) await eda.pcb_PrimitivePour.modify(p.getState_PrimitiveId(), { preserveSilos: true });
for (const p of pours) await p.rebuildCopperRegion();
return { count: pours.length, silos: pours.map(p => p.getState_PreserveSilos()) };
