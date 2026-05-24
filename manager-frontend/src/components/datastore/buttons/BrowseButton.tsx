import { DatabaseOutlined } from "@ant-design/icons";
import { Button } from "antd";
import type { DataStore } from "@/api/model";

interface Props {
	ds: DataStore;
	active: boolean;
	onClick: () => void;
}

export function BrowseButton({ ds, active, onClick }: Props) {
	return (
		<Button
			type={active ? "primary" : "default"}
			icon={<DatabaseOutlined />}
			onClick={onClick}
		>
			{ds[0].toUpperCase() + ds.slice(1)}
		</Button>
	);
}
