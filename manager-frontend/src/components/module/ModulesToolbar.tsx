import { CloudDownloadOutlined, DeleteOutlined } from "@ant-design/icons";
import {
	Button,
	Input,
	message,
	Popconfirm,
	Select,
	Space,
	Typography,
} from "antd";
import { useRef } from "react";
import {
	useDeleteAllModules,
	useDownloadAllModules,
} from "@/api/modules/modules";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";
import { useMutationOptions } from "@/hooks/useMutationOptions";

export interface ToolbarFilters {
	search: string;
	status: string | undefined;
	sort: "name" | "status";
}

interface Props {
	moduleCount: number;
	onChange: (filters: ToolbarFilters) => void;
}

export function ModulesToolbar({ moduleCount, onChange }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const disabled = useDisabled();
	const downloadAll = useDownloadAllModules(opts("All modules downloaded"));
	const deleteAll = useDeleteAllModules(opts("All modules deleted"));

	const filters = useRef<ToolbarFilters>({
		search: "",
		status: undefined,
		sort: "name",
	});

	const emit = (patch: Partial<ToolbarFilters>) => {
		Object.assign(filters.current, patch);
		onChange({ ...filters.current });
	};

	return (
		<>
			{contextHolder}
			<Space style={{ marginBottom: 16, width: "100%" }}>
				<Typography.Title
					level={5}
					style={{ margin: 0 }}
				>{`Modules (${moduleCount})`}</Typography.Title>
				<Input.Search
					placeholder="Filter by name"
					allowClear
					onChange={(e) => emit({ search: e.target.value })}
					style={{ width: 250 }}
				/>
				<Select
					placeholder="Status"
					allowClear
					onChange={(v) => emit({ status: v })}
					style={{ width: 120 }}
					options={[
						{ value: "local", label: "Local" },
						{ value: "remote", label: "Remote" },
					]}
				/>
				<Select
					defaultValue={"name" as const}
					onChange={(v) => emit({ sort: v })}
					style={{ width: 140 }}
					options={[
						{ value: "name", label: "Sort: Name" },
						{ value: "status", label: "Sort: Status" },
					]}
				/>
				<DisabledTooltip>
					<Button
						icon={<CloudDownloadOutlined />}
						loading={downloadAll.isPending}
						onClick={() => downloadAll.mutate()}
						disabled={disabled}
					/>
				</DisabledTooltip>
				<DisabledTooltip>
					<Popconfirm
						title="Delete all downloaded modules?"
						onConfirm={() => deleteAll.mutate()}
					>
						<Button
							danger
							icon={<DeleteOutlined />}
							loading={deleteAll.isPending}
							disabled={disabled}
						/>
					</Popconfirm>
				</DisabledTooltip>
			</Space>
		</>
	);
}
