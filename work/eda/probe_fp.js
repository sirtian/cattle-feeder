const sys = await eda.lib_LibrariesList.getSystemLibraryUuid();
const out = { sys, tries: [] };
for (const lib of ['0819f05c4eef4c71ace90d822a990e87', sys]) {
  for (const uuid of ['0a956972613a413195dd8939923f26c4', '92305db896ac9d21']) {
    try { const f = await eda.lib_Footprint.get(uuid, lib); out.tries.push({ lib, uuid, found: !!f, name: f && f.name }); }
    catch(e) { out.tries.push({ lib, uuid, err: String(e).slice(0,80) }); }
  }
}
try { const s = await eda.lib_Footprint.search('IND-SMD_L7.1-W6.6', sys, undefined, undefined, 5, 1); out.search = (s || []).map(x => ({ uuid: x.uuid, name: x.name, lib: x.libraryUuid })); } catch(e) { out.searchErr = String(e); }
return out;
