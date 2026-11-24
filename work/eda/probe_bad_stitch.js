const out={};
for (const id of ['b799b39dc8488cb4','2baa93b96943b7b2']) {
  try { const r=await eda.pcb_PrimitiveLine.get([id]); if(r&&r.length) out[id]={a:[r[0].getState_StartX(),r[0].getState_StartY()],b:[r[0].getState_EndX(),r[0].getState_EndY()],net:r[0].getState_Net()}; } catch(e){}
}
for (const id of ['3c148069cc506445']) {
  try { const v=await eda.pcb_PrimitiveVia.get([id]); if(v&&v.length) out[id]={x:v[0].getState_X(),y:v[0].getState_Y(),net:v[0].getState_Net()}; } catch(e){}
}
return out;
