const sys = await eda.lib_LibrariesList.getSystemLibraryUuid();
let fp = null, err = null;
try { fp = await eda.lib_Footprint.get('f38b786f5a7b43d78fde8f0e095c485d', sys); } catch(e) { err = String(e); }
return { found: !!fp, name: fp && fp.name, err };
