import { useGetSchema, useGetModuleData } from "../../api/modules/modules";
import { SchemaTree } from "../schema/SchemaTree";
import type { ModuleSummary } from "../../api/model";

export function ModuleContent({ module }: { module: ModuleSummary }) {
  const isLocal = module.status === "local";
  const { data: schemaRes, isLoading: schemaLoading } = useGetSchema(module.name, { query: { enabled: isLocal } });
  const { data: dataRes, isLoading: dataLoading } = useGetModuleData(module.name, { query: { enabled: isLocal } });

  if (!isLocal) return <span>Download module to view schema.</span>;
  if (schemaLoading || dataLoading) return <span>Loading...</span>;
  if (!schemaRes?.data?.children) return <span>No schema available.</span>;

  return <SchemaTree node={schemaRes.data} data={dataRes?.data} />;
}
