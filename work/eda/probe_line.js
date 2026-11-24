const out = {};
try { const r = await eda.pcb_PrimitiveLine.get(['88c3be866006b62a']); if (r&&r.length) out.line = { a:[r[0].getState_StartX(),r[0].getState_StartY()], b:[r[0].getState_EndX(),r[0].getState_EndY()], net:r[0].getState_Net(), layer:r[0].getState_Layer() }; } catch(e){ out.lineErr=String(e); }
try { const r2 = await eda.pcb_PrimitiveVia.get(['de8be7fbe4d9d385']); if (r2&&r2.length) out.via = { x:r2[0].getState_X(), y:r2[0].getState_Y(), net:r2[0].getState_Net() }; } catch(e){ out.viaErr=String(e); }
return out;
