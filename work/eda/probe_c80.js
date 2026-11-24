const lines = await eda.pcb_PrimitiveLine.getAll();
const vs = await eda.pcb_PrimitiveVia.getAll();
const cx=-1931.4, cy=1118.9;
const nearL = lines.filter(l => Math.hypot((l.getState_StartX()+l.getState_EndX())/2-cx,(l.getState_StartY()+l.getState_EndY())/2-cy)<60)
  .map(l => ({net:l.getState_Net(),layer:l.getState_Layer(),a:[l.getState_StartX(),l.getState_StartY()],b:[l.getState_EndX(),l.getState_EndY()]}));
const nearV = vs.filter(v => Math.hypot(v.getState_X()-cx,v.getState_Y()-cy)<60)
  .map(v => ({net:v.getState_Net(),x:v.getState_X(),y:v.getState_Y()}));
return { nearL, nearV };
