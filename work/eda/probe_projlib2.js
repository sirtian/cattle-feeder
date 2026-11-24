const lib='ffd1283dd35949a9b4e3c1887040a91c';
const out={};
try { const f=await eda.lib_Footprint.get('9e165ad2346adb5b',lib); out.fp={found:!!f,name:f&&f.name}; } catch(e){ out.fpErr=String(e); }
try { const d=await eda.lib_Device.get('70064afff7a24b0ca09f576b54ed848e',lib); out.dev={found:!!d,name:d&&d.name}; } catch(e){ out.devErr=String(e); }
return out;
