const p = await eda.pcb_PrimitivePad.get(['f29e6f04d3cc3529']);
if (!p || !p.length) return { missing: true };
const pad = p[0];
const parentId = pad.getState_ParentComponentPrimitiveId ? pad.getState_ParentComponentPrimitiveId() : null;
let parent = null;
if (parentId) {
  const comps = await eda.pcb_PrimitiveComponent.get([parentId]);
  if (comps && comps.length) parent = { d: comps[0].getState_Designator(), x: comps[0].getState_X(), y: comps[0].getState_Y() };
}
return { pad: { x: pad.getState_X(), y: pad.getState_Y(), net: pad.getState_Net(), layer: pad.getState_Layer(),
  w: pad.getState_Width ? pad.getState_Width() : null, h: pad.getState_Height ? pad.getState_Height() : null }, parentId, parent };
