const comps = await eda.sch_PrimitiveComponent.getAll();
const c = comps.find(x => x.getState_Designator() === 'L1');
const out = { sch: null, pcb: null };
if (c) out.sch = { id: c.getState_PrimitiveId(), uniqueId: c.getState_UniqueId ? c.getState_UniqueId() : null,
  footprint: c.getState_Footprint ? c.getState_Footprint() : null, comp: c.getState_Component ? c.getState_Component() : null };
const pcbs = await eda.pcb_PrimitiveComponent.getAll();
const p = pcbs.find(x => x.getState_Designator() === 'L1');
if (p) out.pcb = { id: p.getState_PrimitiveId(), uniqueId: p.getState_UniqueId ? p.getState_UniqueId() : null, fp: p.getState_Footprint ? p.getState_Footprint() : null };
return out;
