const v = await eda.sch_Drc.check(true, false, true);
return { raw: v, keys: v.map(x => x && Object.keys(x)) };
