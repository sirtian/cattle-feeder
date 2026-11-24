const ids = ['4c083bf3a2761dd6','ec1a14e2ffe46a84','c79a5a5c23ed4589','396a5c56c3d15e21','e6d12b711a2019cf','50ef90866c45f19b'];
const r = await eda.pcb_PrimitiveVia.delete(ids);
return { deleted: r };
