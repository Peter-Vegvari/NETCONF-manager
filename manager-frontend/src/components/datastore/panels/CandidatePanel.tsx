import { Space } from "antd";
import { BrowseButton } from "@/components/datastore/buttons/BrowseButton";
import { CommitButton } from "@/components/datastore/buttons/CommitButton";
import { CopyButton } from "@/components/datastore/buttons/CopyButton";
import { DeleteConfigButton } from "@/components/datastore/buttons/DeleteConfigButton";
import { LockButton } from "@/components/datastore/buttons/LockButton";
import { StagedButton } from "@/components/datastore/buttons/StagedButton";

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
