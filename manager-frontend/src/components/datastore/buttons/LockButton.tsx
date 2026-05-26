import { LockOutlined, UnlockOutlined } from "@ant-design/icons";
import { useQueryClient } from "@tanstack/react-query";
import { Button, message } from "antd";
import {
	getGetLockQueryKey,
	useGetLock,
	useLockDatastore,
	useUnlockDatastore,
} from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";
import { useDisabled } from "@/components/DisabledTooltip";
import { useConnected } from "@/hooks/connected";

interface Props {
	ds: DataStore;
}

export function LockButton({ ds }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const queryClient = useQueryClient();
	const connected = useConnected();
	const disabled = useDisabled();
	const { data } = useGetLock(ds, { query: { enabled: connected } });
	const locked = data?.status === 200 ? data.data : false;

	const onSuccess = (label: string) => ({
		mutation: {
			onSuccess: () => {
				queryClient.invalidateQueries({ queryKey: getGetLockQueryKey(ds) });
				msg.success(label);
			},
			onError: () => msg.error(`Failed to ${label.toLowerCase()}`),
		},
	});

	const lock = useLockDatastore(onSuccess("Locked"));
	const unlock = useUnlockDatastore(onSuccess("Unlocked"));

	return (
		<>
			{contextHolder}
			<Button
				icon={locked ? <UnlockOutlined /> : <LockOutlined />}
				onClick={() => (locked ? unlock : lock).mutate({ dataStore: ds })}
				loading={lock.isPending || unlock.isPending}
				disabled={disabled}
				title={locked ? "Unlock" : "Lock"}
			/>
		</>
	);
}
