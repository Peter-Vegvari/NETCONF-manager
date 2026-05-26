import { Space } from "antd";
import { BrowseButton } from "./buttons/BrowseButton";
import { CommitButton } from "./buttons/CommitButton";
import { CopyButton } from "./buttons/CopyButton";
import { DeleteConfigButton } from "./buttons/DeleteConfigButton";
import { LockButton } from "./buttons/LockButton";
import { StagedButton } from "./buttons/StagedButton";

interface Props {
	active: boolean;
	onBrowse: () => void;
	showStaged: boolean;
	onStaged: () => void;
}

export function CandidatePanel({
	active,
	onBrowse,
	showStaged,
	onStaged,
}: Props) {
	return (
		<Space.Compact>
			<BrowseButton ds="candidate" active={active} onClick={onBrowse} />
			<StagedButton active={showStaged} onClick={onStaged} />
			<CommitButton />
			<CopyButton ds="candidate" />
			<LockButton ds="candidate" />
			<DeleteConfigButton ds="candidate" />
		</Space.Compact>
	);
}
