const ids = ['4da14b9722521f76','eeffb278153e5684','dad171fd49dff3da','951419ceb5ecae09','33299b7e09969a95',
  'fac132f71571a6b1','5f450bab454a1933','d7167980c8492f67','90abddbd126e07bd','14a72dd39908ce89'];
const out = {};
for (const id of ids) {
  let info = null;
  for (const [kind, api] of [['pad', eda.pcb_PrimitivePad], ['via', eda.pcb_PrimitiveVia], ['line', eda.pcb_PrimitiveLine]]) {
    try {
      const r = await api.get([id]);
      if (r && r.length) {
        const o = r[0];
        info = { kind, x: o.getState_X ? o.getState_X() : null, y: o.getState_Y ? o.getState_Y() : null,
          net: o.getState_Net ? o.getState_Net() : null, layer: o.getState_Layer ? o.getState_Layer() : null,
          d: o.getState_Diameter ? o.getState_Diameter() : null, drill: o.getState_HoleDiameter ? o.getState_HoleDiameter() : null,
          shape: o.getState_Pad ? o.getState_Pad() : null };
        break;
      }
    } catch(e) {}
  }
  out[id] = info;
}
return out;
