import { useQueryClient } from "@tanstack/react-query";
import { message, Space } from "antd";
import {
	getGetLockQueryKey,
	useCopyConfigTo,
	useDeleteConfig,
	useLockDatastore,
	useUnlockDatastore,
} from "../../api/datastore/datastore";
import type { DataStore } from "../../api/model";
import { DatastoreButton } from "./DatastoreButton";

const DATASTORES: DataStore[] = ["running", "candidate", "startup"];

export function DatastoreMenu({
	dataStore,
	setDataStore,
}: {
	dataStore: DataStore;
	setDataStore: (ds: DataStore) => void;
}) {
	const [msg, contextHolder] = message.useMessage();
	const queryClient = useQueryClient();

	const invalidateLocks = () => {
		for (const ds of DATASTORES) {
			queryClient.invalidateQueries({ queryKey: getGetLockQueryKey(ds) });
		}
	};

	const mutOpts = (label: string) => ({
		mutation: {
			onSuccess: () => {
				msg.success(`${label} succeeded`);
				invalidateLocks();
			},
			onError: () => msg.error(`${label} failed`),
		},
	});

	const copyConfig = useCopyConfigTo(mutOpts("copy-config"));
	const deleteConfig = useDeleteConfig(mutOpts("delete-config"));
	const lock = useLockDatastore(mutOpts("lock"));
	const unlock = useUnlockDatastore(mutOpts("unlock"));

	return (
		<>
			{contextHolder}
			<Space orientation="vertical" style={{ width: 200, flexShrink: 0 }}>
				{DATASTORES.map((ds) => (
					<DatastoreButton
						key={ds}
						ds={ds}
						active={dataStore === ds}
						onBrowse={() => setDataStore(ds)}
						onCopy={() =>
							copyConfig.mutate({
								source: ds,
								target: ds === "running" ? "startup" : "running",
							})
						}
						onDelete={
							ds !== "running"
								? () => deleteConfig.mutate({ dataStore: ds })
								: undefined
						}
						onToggleLock={(locked) =>
							(locked ? unlock : lock).mutate({ dataStore: ds })
						}
					/>
				))}
			</Space>
		</>
	);
}
