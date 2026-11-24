const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
const vs = cfg.Physics['Via Size'];
const out = {};
for (const k of Object.keys(vs)) out[k] = vs[k].form || vs[k];
return out;
