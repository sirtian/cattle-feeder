const lib='ffd1283dd35949a9b4e3c1887040a91c';
const out={};
try { const f=await eda.lib_Footprint.get('92305db896ac9d21',lib); out.fp={found:!!f,name:f&&f.name}; } catch(e){ out.fpErr=String(e); }
try { const d=await eda.lib_Device.get('bb962029a175660d',lib); out.dev={found:!!d,name:d&&d.name}; } catch(e){ out.devErr=String(e); }
try { const d2=await eda.lib_Device.get('3df0e9da5e7e44cb992bebec68a34654',lib); out.part={found:!!d2,name:d2&&d2.name}; } catch(e){ out.partErr=String(e); }
return out;
