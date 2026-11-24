const v = await eda.pcb_Drc.check(true, false, true);
return { count: v.length, sample: (v||[]).slice(0,20) };
