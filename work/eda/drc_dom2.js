await eda.sch_Drc.check(true, true, true);
await new Promise(r => setTimeout(r, 2500));
let txt = '';
try { txt = document.body.innerText; } catch(e) { txt = 'ERR:' + e; }
const lines = txt.split('\n').filter(l => l.includes('[') || l.includes('DRC') || l.includes('检查') || l.includes('完成')).slice(0, 40);
return { lines };
