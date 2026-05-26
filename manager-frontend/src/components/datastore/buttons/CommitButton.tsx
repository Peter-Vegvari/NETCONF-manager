import { CheckOutlined } from "@ant-design/icons";
import { Button, message } from "antd";
import { useCommit } from "@/api/datastore/datastore";
import { useDisabled } from "@/components/DisabledTooltip";
import { useMutationOptions } from "@/hooks/useMutationOptions";

export function CommitButton() {
	const disabled = useDisabled();
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const commitMutation = useCommit(opts("Commit successful"));

	return (
		<>
			{contextHolder}
			<Button
				icon={<CheckOutlined />}
				onClick={() => commitMutation.mutate()}
				disabled={disabled}
				loading={commitMutation.isPending}
			>
				Commit
			</Button>
		</>
	);
}
