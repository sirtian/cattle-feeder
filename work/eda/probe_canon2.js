const canon = await eda.lib_Device.get('2a16b44b218c4dfd96372a3decfe44ee', '0819f05c4eef4c71ace90d822a990e87');
const dev = await eda.lib_Device.get('bb962029a175660d', '0819f05c4eef4c71ace90d822a990e87');
return { canonProp: canon.property, devProp: dev.property };
