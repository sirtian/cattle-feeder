const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
let n=0;
function walk(o){
  if (Array.isArray(o)) { for (let i=0;i<o.length;i++){ if (typeof o[i]==='number'){ if (Math.abs(o[i]-0.13)<1e-4){o[i]=0.127;n++;} } else walk(o[i]); } }
  else if (o && typeof o==='object') { for (const k of Object.keys(o)){ if (typeof o[k]==='number'){ if (Math.abs(o[k]-0.13)<1e-4){o[k]=0.127;n++;} } else walk(o[k]); } }
}
walk(cfg.Spacing);
await eda.pcb_Drc.overwriteCurrentRuleConfiguration(cfg);
return { changed:n };
