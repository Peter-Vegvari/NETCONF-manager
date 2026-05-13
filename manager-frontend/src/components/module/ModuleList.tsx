import { Collapse } from "antd";
import { useMemo, useState } from "react";
import type { DataStore, ModuleSummary } from "../../api/model";
import { ModuleContent } from "./ModuleContent";
import { ModuleItemActions, ModuleItemLabel } from "./ModuleItem";
import { ModulesToolbar } from "./ModulesToolbar";

interface Props {
	modules: ModuleSummary[];
	onDownload: (name: string) => void;
	onDelete: (name: string) => void;
	downloadPending: boolean;
	downloadingName?: string;
	dataStore: DataStore;
}

export function ModuleList({
	modules,
	onDownload,
	onDelete,
	downloadPending,
	downloadingName,
	dataStore,
}: Props) {
	const [search, setSearch] = useState("");
	const [statusFilter, setStatusFilter] = useState<string | undefined>();
	const [sort, setSort] = useState<"name" | "status">("name");

	const filtered = useMemo(() => {
		return modules
			.filter(
				(m) =>
					m.name.includes(search) &&
					(!statusFilter || m.status === statusFilter),
			)
			.sort((a, b) => a[sort].localeCompare(b[sort]));
	}, [modules, search, statusFilter, sort]);

	const items = filtered.map((m) => ({
		key: m.name,
		label: <ModuleItemLabel module={m} />,
		extra: (
			<ModuleItemActions
				module={m}
				onDownload={onDownload}
				onDelete={onDelete}
				downloadPending={downloadPending}
				downloadingName={downloadingName}
			/>
		),
		children: <ModuleContent module={m} dataStore={dataStore} />,
	}));

	return (
		<>
			<ModulesToolbar
				onSearchChange={setSearch}
				onStatusChange={setStatusFilter}
				sort={sort}
				onSortChange={setSort}
			/>
			{filtered.length === 0 ? "No modules found." : <Collapse items={items} />}
		</>
	);
}
