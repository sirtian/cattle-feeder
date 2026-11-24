const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
const vs = cfg.Physics['Via Size'];
const D = 0.50000012, H = 0.30000018;
for (const k of Object.keys(vs)) {
  const f = vs[k] && vs[k].form;
  if (!f) continue;
  if (f.viaOuterdiameterMin !== undefined) { f.viaOuterdiameterMin = D; f.viaOuterdiameterMax = D; f.viaOuterdiameterDefault = D; }
  if (f.viaInnerdiameterMin !== undefined) { f.viaInnerdiameterMin = H; f.viaInnerdiameterMax = H; f.viaInnerdiameterDefault = H; }
}
await eda.pcb_Drc.overwriteCurrentRuleConfiguration(cfg);
const chk = await eda.pcb_Drc.getCurrentRuleConfiguration();
const c2 = chk && chk.config ? chk.config : chk;
return c2.Physics['Via Size']['copperThickness1oz'].form;
