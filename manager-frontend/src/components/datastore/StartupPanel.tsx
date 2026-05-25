import { Space } from "antd";
import { BrowseButton } from "./buttons/BrowseButton";
import { CopyButton } from "./buttons/CopyButton";
import { DeleteConfigButton } from "./buttons/DeleteConfigButton";
import { LockButton } from "./buttons/LockButton";

interface Props {
	active: boolean;
	onBrowse: () => void;
}

export function StartupPanel({ active, onBrowse }: Props) {
	return (
		<Space.Compact>
			<BrowseButton ds="startup" active={active} onClick={onBrowse} />
			<CopyButton ds="startup" />
			<LockButton ds="startup" />
			<DeleteConfigButton ds="startup" />
		</Space.Compact>
	);
}
