import { useMemo, useState } from "react";
import { Collapse } from "antd";
import type { ModuleSummary } from "../../api/model";
import { ModuleItemLabel, ModuleItemActions } from "./ModuleItem";
import { ModuleContent } from "./ModuleContent";
import { ModulesToolbar } from "./ModulesToolbar";

interface Props {
  modules: ModuleSummary[];
  onDownload: (name: string) => void;
  onDelete: (name: string) => void;
  downloadPending: boolean;
  downloadingName?: string;
}

export function ModuleList({ modules, onDownload, onDelete, downloadPending, downloadingName }: Props) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [sort, setSort] = useState<"name" | "status">("name");

  const filtered = useMemo(() => {
    let result = modules.filter((m) => m.name.toLowerCase().includes(search.toLowerCase()));
    if (statusFilter) result = result.filter((m) => m.status === statusFilter);
    result.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : a.status.localeCompare(b.status));
    return result;
  }, [modules, search, statusFilter, sort]);

  return (
    <>
      <ModulesToolbar onSearchChange={setSearch} onStatusChange={setStatusFilter} sort={sort} onSortChange={setSort} />
      {filtered.length === 0 ? "No modules found." : (
        <Collapse items={filtered.map((m) => ({
          key: m.name,
          label: <ModuleItemLabel module={m} />,
          extra: <ModuleItemActions module={m} onDownload={onDownload} onDelete={onDelete} downloadPending={downloadPending} downloadingName={downloadingName} />,
          children: <ModuleContent module={m} />,
        }))} />
      )}
    </>
  );
}
