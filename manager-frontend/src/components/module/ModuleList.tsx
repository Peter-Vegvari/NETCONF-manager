import { useMemo, useState } from "react";
import { Collapse } from "antd";
import type { ModuleSummary } from "../../api/model";
import { ModuleCollapseItem } from "./ModuleCollapseItem";
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
    return modules
      .filter((m) => m.name.includes(search) && (!statusFilter || m.status === statusFilter))
      .sort((a, b) => a[sort].localeCompare(b[sort]));
  }, [modules, search, statusFilter, sort]);

  return (
    <>
      <ModulesToolbar onSearchChange={setSearch} onStatusChange={setStatusFilter} sort={sort} onSortChange={setSort} />
      {filtered.length === 0 ? "No modules found." : (
        <Collapse>
          {filtered.map((m) => (
            <ModuleCollapseItem
              key={m.name}
              module={m}
              onDownload={onDownload}
              onDelete={onDelete}
              downloadPending={downloadPending}
              downloadingName={downloadingName}
            />
          ))}
        </Collapse>
      )}
    </>
  );
}
