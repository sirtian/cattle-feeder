const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
const bb = cfg.Physics['Blind/Buried Via'];
const nr = await eda.pcb_Drc.getNetRules();
return { blind: bb, netRulesSample: Array.isArray(nr) ? nr.slice(0,3) : nr };
