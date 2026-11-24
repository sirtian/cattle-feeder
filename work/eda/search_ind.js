const sys = await eda.lib_LibrariesList.getSystemLibraryUuid();
const res = await eda.lib_Device.search('10uH', sys, undefined, undefined, 10, 1);
return (res || []).slice(0, 10).map(d => ({ uuid: d.uuid, name: d.name, fp: d.footprintUuid, fpName: d.footprintName, mfr: d.manufacturer, sid: d.supplierId }));
