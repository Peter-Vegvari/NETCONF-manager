import { Space } from "antd";
import { BrowseButton } from "./buttons/BrowseButton";
import { CopyButton } from "./buttons/CopyButton";
import { LockButton } from "./buttons/LockButton";

interface Props {
	active: boolean;
	onBrowse: () => void;
}

export function RunningPanel({ active, onBrowse }: Props) {
	return (
		<Space.Compact>
			<BrowseButton ds="running" active={active} onClick={onBrowse} />
			<CopyButton ds="running" />
			<LockButton ds="running" />
		</Space.Compact>
	);
}
