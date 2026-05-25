import { DeleteOutlined, DownloadOutlined } from "@ant-design/icons";
import { Button, Popconfirm, Tag } from "antd";
import type { ModuleSummary } from "@/api/model";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";
import { statusColor } from "@/utils/constants";

interface Props {
	module: ModuleSummary;
	onDownload: (name: string) => void;
	onDelete: (name: string) => void;
	downloadPending: boolean;
	downloadingName?: string;
}

export function ModuleItemLabel({ module: m }: { module: ModuleSummary }) {
	return (
		<span>
			{m.name} <Tag color={statusColor[m.status]}>{m.status}</Tag>
		</span>
	);
}

export function ModuleItemActions({
	module: m,
	onDownload,
	onDelete,
	downloadPending,
	downloadingName,
}: Props) {
	const disabled = useDisabled();

	if (m.status === "remote") {
		return (
			<DisabledTooltip>
				<Button
					type="text"
					size="small"
					icon={<DownloadOutlined />}
					loading={downloadPending && downloadingName === m.name}
					disabled={disabled}
					onClick={(e) => {
						e.stopPropagation();
						onDownload(m.name);
					}}
				/>
			</DisabledTooltip>
		);
	}
	return (
		<DisabledTooltip>
			<Popconfirm
				title="Delete this module?"
				onConfirm={() => onDelete(m.name)}
				onPopupClick={(e) => e.stopPropagation()}
			>
				<Button
					danger
					type="text"
					size="small"
					icon={<DeleteOutlined />}
					disabled={disabled}
					onClick={(e) => e.stopPropagation()}
				/>
			</Popconfirm>
		</DisabledTooltip>
	);
}
