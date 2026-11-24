const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
const vs = cfg.Physics['Via Size'];
for (const k of Object.keys(vs)) {
  const f = vs[k].form || vs[k];
  f.viaOuterdiameterMin = 0.499999; f.viaOuterdiameterMax = 0.700001; f.viaOuterdiameterDefault = 0.61;
  f.viaInnerdiameterMin = 0.299999; f.viaInnerdiameterMax = 0.400001; f.viaInnerdiameterDefault = 0.31;
}
await eda.pcb_Drc.overwriteCurrentRuleConfiguration(cfg);
const chk = await eda.pcb_Drc.getCurrentRuleConfiguration();
const c2 = chk && chk.config ? chk.config : chk;
return c2.Physics['Via Size']['copperThickness1oz'].form;
