const v = await eda.pcb_Drc.check(true, false, true);
const arr = Array.isArray(v) ? v : [];
return { count: arr.length, sample: arr.slice(0, 30) };
