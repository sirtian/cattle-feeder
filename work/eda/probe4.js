const lines = await eda.pcb_PrimitiveLine.getAll();
const on11 = lines.filter(l => l.getState_Layer() === 11).map(l => ({
  id: l.getState_PrimitiveId(), type: l.getState_PrimitiveType(),
  x1: l.getState_StartX(), y1: l.getState_StartY(),
  x2: l.getState_EndX(), y2: l.getState_EndY()
}));
return { n: on11.length, on11 };
