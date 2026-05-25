import { DatabaseOutlined } from "@ant-design/icons";
import { Button } from "antd";
import type { DataStore } from "@/api/model";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";

interface Props {
	ds: DataStore;
	active: boolean;
	onClick: () => void;
}

export function BrowseButton({ ds, active, onClick }: Props) {
	const disabled = useDisabled();
	return (
		<DisabledTooltip>
			<Button
				type={active ? "primary" : "default"}
				icon={<DatabaseOutlined />}
				onClick={onClick}
				disabled={disabled}
			>
				{ds[0].toUpperCase() + ds.slice(1)}
			</Button>
		</DisabledTooltip>
	);
}
