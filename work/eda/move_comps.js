const moves = {
  C7: [-2200,-1800], C8: [-1300,-1800], C77: [1400,-1800], C85: [1700,-1800],
  R4: [2300,-1800], R5: [-1600,-2000], R6: [-1300,-2000], C93: [-100,-2000], D2: [2300,-2000]
};
const all = await eda.pcb_PrimitiveComponent.getAll();
const out = [];
for (const d of Object.keys(moves)) {
  const c = all.find(x => x.getState_Designator() === d);
  if (!c) { out.push({d, missing:true}); continue; }
  const [x,y] = moves[d];
  await eda.pcb_PrimitiveComponent.modify(c.getState_PrimitiveId(), { x, y });
  const back = (await eda.pcb_PrimitiveComponent.getAll()).find(x2 => x2.getState_PrimitiveId() === c.getState_PrimitiveId());
  out.push({ d, x: back.getState_X(), y: back.getState_Y() });
}
return out;
