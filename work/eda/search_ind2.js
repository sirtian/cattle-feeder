const sys = await eda.lib_LibrariesList.getSystemLibraryUuid();
const out = {};
for (const key of ['10uH 5A', '10uH 4A', '10uH 6A']) {
  try { const res = await eda.lib_Device.search(key, sys, undefined, undefined, 6, 1); out[key] = (res||[]).map(d=>({name:d.name,uuid:d.uuid,fp:d.footprintUuid,fpName:d.footprintName,sid:d.supplierId})); }
  catch(e){ out[key] = String(e); }
}
return out;
