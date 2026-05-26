import { Space } from "antd";
import { BrowseButton } from "@/components/datastore/buttons/BrowseButton";
import { CopyButton } from "@/components/datastore/buttons/CopyButton";
import { DeleteConfigButton } from "@/components/datastore/buttons/DeleteConfigButton";
import { LockButton } from "@/components/datastore/buttons/LockButton";

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
