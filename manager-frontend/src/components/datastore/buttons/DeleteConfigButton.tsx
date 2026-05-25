import { DeleteOutlined } from "@ant-design/icons";
import { Button, message } from "antd";
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
			<Button
				icon={<DeleteOutlined />}
				onClick={() => deleteConfig.mutate({ dataStore: ds })}
				loading={deleteConfig.isPending}
				disabled={disabled}
				danger
				title="Delete config"
			/>
		</>
	);
}
