import { DeleteOutlined } from "@ant-design/icons";
import { Button } from "antd";

interface Props {
	onClick: () => void;
}

export function DeleteConfigButton({ onClick }: Props) {
	return (
		<Button icon={<DeleteOutlined />} onClick={onClick} title="Delete config" />
	);
}
