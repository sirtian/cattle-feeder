const vs = await eda.pcb_PrimitiveVia.getAll();
const near = vs.filter(v => (Math.hypot(v.getState_X()+5447.4, v.getState_Y()-1560.4)<3) || (Math.hypot(v.getState_X()-1770.2, v.getState_Y()+3339.2)<3))
  .map(v=>({id:v.getState_PrimitiveId(),net:v.getState_Net(),x:v.getState_X(),y:v.getState_Y()}));
return near;
