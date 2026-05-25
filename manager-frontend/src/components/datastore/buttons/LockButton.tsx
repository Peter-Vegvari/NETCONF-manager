import { LockOutlined, UnlockOutlined } from "@ant-design/icons";
import { Button, message } from "antd";
import {
	useGetLock,
	useLockDatastore,
	useUnlockDatastore,
} from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";
import { useConnected } from "@/hooks/connected";
import { useMutationOptions } from "@/hooks/useMutationOptions";

interface Props {
	ds: DataStore;
}

export function LockButton({ ds }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const connected = useConnected();
	const disabled = useDisabled();
	const { data } = useGetLock(ds, { query: { enabled: connected } });
	const locked = data?.status === 200 ? data.data : false;

	const lock = useLockDatastore(opts("lock"));
	const unlock = useUnlockDatastore(opts("unlock"));

	return (
		<>
			{contextHolder}
			<DisabledTooltip>
				<Button
					icon={locked ? <UnlockOutlined /> : <LockOutlined />}
					onClick={() => (locked ? unlock : lock).mutate({ dataStore: ds })}
					loading={lock.isPending || unlock.isPending}
					disabled={disabled}
					title={locked ? "Unlock" : "Lock"}
				/>
			</DisabledTooltip>
		</>
	);
}
