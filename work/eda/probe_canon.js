const canon = await eda.lib_Device.get('2a16b44b218c4dfd96372a3decfe44ee', '0819f05c4eef4c71ace90d822a990e87');
return { keys: canon && Object.keys(canon), canon: canon && { name: canon.name, symbol: canon.symbolUuid, symbol2: canon.symbol, fp: canon.footprintUuid, other: canon.otherProperty } };
