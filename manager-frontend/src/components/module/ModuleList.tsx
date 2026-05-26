import { Collapse, message } from "antd";
import { useMemo, useState } from "react";
import type { DataStore } from "@/api/model";
import {
	useDeleteModule,
	useDownloadModule,
	useGetModules,
} from "@/api/modules/modules";
import { useMutationOptions } from "@/hooks/useMutationOptions";
import { ModuleContent } from "./ModuleContent";
import { ModuleItemActions, ModuleItemLabel } from "./ModuleItem";
import { ModulesToolbar, type ToolbarFilters } from "./ModulesToolbar";
import { StagedContent } from "./StagedContent";

interface Props {
	dataStore: DataStore;
	view?: "browse" | "staged";
}

export function ModuleList({ dataStore, view = "browse" }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const [filters, setFilters] = useState<ToolbarFilters>({
		search: "",
		status: undefined,
		sort: "name",
	});

	const { data } = useGetModules();
	const download = useDownloadModule(opts("Module downloaded"));
	const remove = useDeleteModule(opts("Module deleted"));

	const modules = useMemo(
		() => (Array.isArray(data?.data) ? data.data : []),
		[data],
	);

	const filtered = useMemo(() => {
		return modules
			.filter(
				(m) =>
					m.name.includes(filters.search) &&
					(!filters.status || m.status === filters.status),
			)
			.sort((a, b) => a[filters.sort].localeCompare(b[filters.sort]));
	}, [modules, filters]);

	const items = filtered.map((m) => ({
		key: m.name,
		label: <ModuleItemLabel module={m} />,
		extra: (
			<ModuleItemActions
				module={m}
				onDownload={(name) => download.mutate({ moduleName: name })}
				onDelete={(name) => remove.mutate({ moduleName: name })}
				downloadPending={download.isPending}
				downloadingName={download.variables?.moduleName}
			/>
		),
		children:
			view === "staged" ? (
				<StagedContent module={m} />
			) : (
				<ModuleContent module={m} dataStore={dataStore} />
			),
	}));

	return (
		<>
			{contextHolder}
			<ModulesToolbar moduleCount={modules.length} onChange={setFilters} />
			{filtered.length === 0 ? "No modules found." : <Collapse items={items} />}
		</>
	);
}
