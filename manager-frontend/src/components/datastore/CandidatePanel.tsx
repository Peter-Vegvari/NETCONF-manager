import { Space } from "antd";
import { BrowseButton } from "./buttons/BrowseButton";
import { CopyButton } from "./buttons/CopyButton";
import { DeleteConfigButton } from "./buttons/DeleteConfigButton";
import { LockButton } from "./buttons/LockButton";

interface Props {
	active: boolean;
	onBrowse: () => void;
}

export function CandidatePanel({ active, onBrowse }: Props) {
	return (
		<Space.Compact>
			<BrowseButton ds="candidate" active={active} onClick={onBrowse} />
			<CopyButton ds="candidate" />
			<LockButton ds="candidate" />
			<DeleteConfigButton ds="candidate" />
		</Space.Compact>
	);
}
