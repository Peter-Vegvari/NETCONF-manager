import { DiffOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useDisabled } from "@/components/DisabledTooltip";

interface Props {
	active: boolean;
	onClick: () => void;
}

export function StagedButton({ active, onClick }: Props) {
	const disabled = useDisabled();
	return (
		<Button
			type={active ? "primary" : "default"}
			icon={<DiffOutlined />}
			onClick={onClick}
			disabled={disabled}
		>
			Staged
		</Button>
	);
}
