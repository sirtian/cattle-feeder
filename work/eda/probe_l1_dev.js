const libUuid = '0819f05c4eef4c71ace90d822a990e87';
const dev = await eda.lib_Device.get('bb962029a175660d', libUuid);
const byLcsc = await eda.lib_Device.getByLcscIds(['C436568'], libUuid, true);
return { dev, byLcsc };
