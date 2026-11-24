const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
const cfg = r && r.config ? r.config : r;
const t = cfg.Physics.Track;
for (const k of ['copperThickness1oz', 'copilot_router_net_0_track']) {
  const d = t[k] && t[k].form && t[k].form.data && t[k].form.data['1'];
  if (d) d.maxValue = 2.40000014;
}
await eda.pcb_Drc.overwriteCurrentRuleConfiguration(cfg);
return { max: t.copperThickness1oz.form.data['1'].maxValue };
