import { CopyOutlined } from "@ant-design/icons";
import { Button } from "antd";

interface Props {
	onClick: () => void;
}

export function CopyButton({ onClick }: Props) {
	return (
		<Button icon={<CopyOutlined />} onClick={onClick} title="Copy config" />
	);
}
