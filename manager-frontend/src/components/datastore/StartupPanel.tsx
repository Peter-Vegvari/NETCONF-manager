import { message } from "antd";
import {
	useCopyConfigTo,
	useDeleteConfig,
	useLockDatastore,
	useUnlockDatastore,
} from "@/api/datastore/datastore";
import { useMutationOptions } from "@/hooks/useMutationOptions";
import { CopyButton } from "./buttons/CopyButton";
import { DeleteConfigButton } from "./buttons/DeleteConfigButton";
import { DatastorePanelBase } from "./DatastorePanelBase";

interface Props {
	active: boolean;
	onBrowse: () => void;
}

export function StartupPanel({ active, onBrowse }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const mutOpts = useMutationOptions(msg);

	const copyConfig = useCopyConfigTo(mutOpts("copy-config"));
	const deleteConfig = useDeleteConfig(mutOpts("delete-config"));
	const lock = useLockDatastore(mutOpts("lock"));
	const unlock = useUnlockDatastore(mutOpts("unlock"));

	return (
		<>
			{contextHolder}
			<DatastorePanelBase
				ds="startup"
				active={active}
				onBrowse={onBrowse}
				onToggleLock={(locked) =>
					(locked ? unlock : lock).mutate({ dataStore: "startup" })
				}
			>
				<CopyButton
					onClick={() =>
						copyConfig.mutate({ source: "startup", target: "running" })
					}
				/>
				<DeleteConfigButton
					onClick={() => deleteConfig.mutate({ dataStore: "startup" })}
				/>
			</DatastorePanelBase>
		</>
	);
}
