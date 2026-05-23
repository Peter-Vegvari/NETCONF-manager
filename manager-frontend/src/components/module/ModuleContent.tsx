import { useGetModuleData } from "../../api/datastore/datastore";
import type { DataStore, ModuleSummary } from "../../api/model";
import { useGetSchema } from "../../api/modules/modules";
import { SchemaTree } from "../schema/SchemaTree";

export function ModuleContent({
	module,
	dataStore,
}: {
	module: ModuleSummary;
	dataStore: DataStore;
}) {
	const isLocal = module.status === "local";
	const { data: schemaRes, isLoading: schemaLoading } = useGetSchema(
		module.name,
		{ query: { enabled: isLocal } },
	);
	const { data: dataRes, isLoading: dataLoading } = useGetModuleData(
		dataStore,
		module.name,
		{ query: { enabled: isLocal } },
	);

	if (!isLocal) return <span>Download module to view schema.</span>;
	if (schemaLoading || dataLoading) return <span>Loading...</span>;
	if (!schemaRes || schemaRes.status !== 200 || !schemaRes.data.children)
		return <span>No schema available.</span>;

	return (
		<SchemaTree
			node={schemaRes.data}
			data={dataRes?.status === 200 ? dataRes.data : undefined}
			dataStore={dataStore}
			moduleName={module.name}
		/>
	);
}
