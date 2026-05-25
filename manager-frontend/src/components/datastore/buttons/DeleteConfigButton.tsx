import { DeleteOutlined } from "@ant-design/icons";
import { Button, message, Popconfirm } from "antd";
import { useDeleteConfig } from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";
import { useDisabled } from "@/components/DisabledTooltip";
import { useMutationOptions } from "@/hooks/useMutationOptions";

interface Props {
	ds: DataStore;
}

export function DeleteConfigButton({ ds }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const disabled = useDisabled();
	const deleteConfig = useDeleteConfig(opts("delete-config"));

	return (
		<>
			{contextHolder}
			<Popconfirm
				title="Delete this config?"
				onConfirm={() => deleteConfig.mutate({ dataStore: ds })}
			>
				<Button
					icon={<DeleteOutlined />}
					loading={deleteConfig.isPending}
					disabled={disabled}
					danger
					title="Delete config"
				/>
			</Popconfirm>
		</>
	);
}
