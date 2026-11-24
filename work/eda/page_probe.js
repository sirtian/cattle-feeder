const comps = await eda.sch_PrimitiveComponent.getAll();
return comps.map(c => c.getState_Designator()).sort();
