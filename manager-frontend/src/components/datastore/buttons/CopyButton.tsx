import { CopyOutlined } from "@ant-design/icons";
import { Button, Dropdown, message } from "antd";
import { useCopyConfigTo } from "@/api/datastore/datastore";
import { DataStore } from "@/api/model";
import { useDisabled } from "@/components/DisabledTooltip";
import { useMutationOptions } from "@/hooks/useMutationOptions";

interface Props {
	ds: DataStore;
}

export function CopyButton({ ds }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const disabled = useDisabled();
	const copyConfig = useCopyConfigTo(opts("copy-config"));

	const items = Object.values(DataStore)
		.filter((d) => d !== ds)
		.map((d) => ({ key: d, label: d }));

	return (
		<>
			{contextHolder}
			<Dropdown
				menu={{
					items,
					onClick: ({ key }) =>
						copyConfig.mutate({ source: ds, target: key as DataStore }),
				}}
				trigger={["click"]}
				disabled={disabled}
			>
				<Button
					icon={<CopyOutlined />}
					loading={copyConfig.isPending}
					disabled={disabled}
					title="Copy config"
				/>
			</Dropdown>
		</>
	);
}
