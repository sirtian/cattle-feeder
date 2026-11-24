await eda.sch_Drc.check(true, true, true);
await new Promise(r => setTimeout(r, 1200));
let txt = '';
try { txt = (document && document.body && document.body.innerText) ? document.body.innerText : ''; } catch(e) { txt = 'ERR:' + e; }
const lines = txt.split('\n').filter(l => l.includes('悬空') || l.includes('DRC') || l.includes('警告') || l.includes('错误')).slice(0, 40);
return { lines, len: txt.length };
