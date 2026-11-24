let fp=null, err=null;
try { fp = await eda.lib_Footprint.get('9e165ad2346adb5b','0819f05c4eef4c71ace90d822a990e87'); } catch(e){ err=String(e); }
return { found: !!fp, name: fp && fp.name, err };
