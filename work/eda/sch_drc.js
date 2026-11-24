const v = await eda.sch_Drc.check(true, false, true);
return { count: v.length, sample: v.slice(0, 15).map(x => typeof x === 'string' ? x : JSON.stringify(x)) };
