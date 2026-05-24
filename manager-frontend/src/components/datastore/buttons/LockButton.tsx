import { LockOutlined, UnlockOutlined } from "@ant-design/icons";
import { Button } from "antd";

interface Props {
	locked: boolean;
	onClick: () => void;
}

export function LockButton({ locked, onClick }: Props) {
	return (
		<Button
			icon={locked ? <UnlockOutlined /> : <LockOutlined />}
			onClick={onClick}
			title={locked ? "Unlock" : "Lock"}
		/>
	);
}
