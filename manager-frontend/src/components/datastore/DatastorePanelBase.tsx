import { Space } from "antd";
import type { ReactNode } from "react";
import { useGetLock } from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";
import { useConnected } from "@/hooks/connected";
import { BrowseButton } from "./buttons/BrowseButton";
import { LockButton } from "./buttons/LockButton";

interface Props {
	ds: DataStore;
	active: boolean;
	onBrowse: () => void;
	onToggleLock: (locked: boolean) => void;
	children?: ReactNode;
}

export function DatastorePanelBase({
	ds,
	active,
	onBrowse,
	onToggleLock,
	children,
}: Props) {
	const connected = useConnected();
	const { data } = useGetLock(ds, { query: { enabled: connected } });
	const locked = data?.status === 200 ? data.data : false;

	return (
		<Space.Compact>
			<BrowseButton ds={ds} active={active} onClick={onBrowse} />
			{children}
			<LockButton locked={locked} onClick={() => onToggleLock(locked)} />
		</Space.Compact>
	);
}
