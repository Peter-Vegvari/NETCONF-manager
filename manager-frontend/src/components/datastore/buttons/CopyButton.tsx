import { CopyOutlined } from "@ant-design/icons";
import { Button, message } from "antd";
import { useCopyConfigTo } from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";
import { useMutationOptions } from "@/hooks/useMutationOptions";

interface Props {
	ds: DataStore;
}

export function CopyButton({ ds }: Props) {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const disabled = useDisabled();
	const copyConfig = useCopyConfigTo(opts("copy-config"));

	const target: DataStore = ds === "running" ? "startup" : "running";

	return (
		<>
			{contextHolder}
			<DisabledTooltip>
				<Button
					icon={<CopyOutlined />}
					onClick={() => copyConfig.mutate({ source: ds, target })}
					loading={copyConfig.isPending}
					disabled={disabled}
					title="Copy config"
				/>
			</DisabledTooltip>
		</>
	);
}
