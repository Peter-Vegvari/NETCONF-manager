import {
	CopyOutlined,
	DatabaseOutlined,
	DeleteOutlined,
	LockOutlined,
	UnlockOutlined,
} from "@ant-design/icons";
import { Button, Space } from "antd";
import { useGetLock } from "../../api/datastore/datastore";
import type { DataStore } from "../../api/model";
import { useConnected } from "../../hooks/connected";

export function DatastoreButton({
	ds,
	active,
	onBrowse,
	onCopy,
	onDelete,
	onToggleLock,
}: {
	ds: DataStore;
	active: boolean;
	onBrowse: () => void;
	onCopy: () => void;
	onDelete?: () => void;
	onToggleLock: (locked: boolean) => void;
}) {
	const connected = useConnected();
	const { data } = useGetLock(ds, { query: { enabled: connected } });
	const locked = data?.status === 200 ? data.data : false;

	return (
		<Space.Compact block>
			<Button
				type={active ? "primary" : "default"}
				icon={<DatabaseOutlined />}
				onClick={onBrowse}
			>
				{ds[0].toUpperCase() + ds.slice(1)}
			</Button>
			<Button icon={<CopyOutlined />} onClick={onCopy} title="Copy config" />
			{onDelete && (
				<Button
					icon={<DeleteOutlined />}
					onClick={onDelete}
					title="Delete config"
				/>
			)}
			<Button
				icon={locked ? <UnlockOutlined /> : <LockOutlined />}
				onClick={() => onToggleLock(locked)}
				title={locked ? "Unlock" : "Lock"}
			/>
		</Space.Compact>
	);
}
