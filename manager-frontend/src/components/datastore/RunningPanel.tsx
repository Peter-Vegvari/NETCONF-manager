import { message } from "antd";
import {
	useCopyConfigTo,
	useLockDatastore,
	useUnlockDatastore,
} from "@/api/datastore/datastore";
import { useMutationOptions } from "@/hooks/useMutationOptions";
import { CopyButton } from "./buttons/CopyButton";
import { DatastorePanelBase } from "./DatastorePanelBase";

interface Props {
	active: boolean;
	onBrowse: () => void;
}

export function RunningPanel({ active, onBrowse }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const mutOpts = useMutationOptions(msg);

	const copyConfig = useCopyConfigTo(mutOpts("copy-config"));
	const lock = useLockDatastore(mutOpts("lock"));
	const unlock = useUnlockDatastore(mutOpts("unlock"));

	return (
		<>
			{contextHolder}
			<DatastorePanelBase
				ds="running"
				active={active}
				onBrowse={onBrowse}
				onToggleLock={(locked) =>
					(locked ? unlock : lock).mutate({ dataStore: "running" })
				}
			>
				<CopyButton
					onClick={() =>
						copyConfig.mutate({ source: "running", target: "startup" })
					}
				/>
			</DatastorePanelBase>
		</>
	);
}
