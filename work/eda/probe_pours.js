const pours = await eda.pcb_PrimitivePour.getAll('GND');
return pours.map(p => ({ id:p.getState_PrimitiveId(), layer:p.getState_Layer(), silos:p.getState_PreserveSilos? p.getState_PreserveSilos(): null, name:p.getState_PourName?p.getState_PourName():null }));
