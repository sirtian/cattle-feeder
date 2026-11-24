const ids = ["32f756264aff79d4"];
if (ids.length) return { del: await eda.pcb_PrimitivePoured.delete(ids), n: ids.length };
return {n:0};