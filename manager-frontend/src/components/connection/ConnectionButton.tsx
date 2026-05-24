import { useQueryClient } from "@tanstack/react-query";
import { Button, type FormInstance, message } from "antd";
import { useConnect, useDisconnect } from "@/api/connection/connection";
import type { Connection } from "@/api/model";
import { useConnected } from "@/hooks/connected";

export function ConnectionButton({ form }: { form: FormInstance<Connection> }) {
	const queryClient = useQueryClient();
	const connected = useConnected();

	const [msg, contextHolder] = message.useMessage();

	const connect = useConnect();
	const disconnect = useDisconnect();

	const handleConnect = async () => {
		const values = await form.validateFields();
		connect.mutate(
			{ data: values },
			{
				onSuccess: () => {
					msg.success("Connected");
					queryClient.refetchQueries();
				},
				onError: () => msg.error("Connection failed"),
			},
		);
	};

	const handleDisconnect = () => {
		disconnect.mutate(undefined, {
			onSuccess: () => {
				msg.success("Disconnected");
				queryClient.refetchQueries();
			},
			onError: () => msg.error("Disconnect failed"),
		});
	};

	if (connected)
		return (
			<>
				{contextHolder}
				<Button
					type="primary"
					danger
					onClick={handleDisconnect}
					loading={disconnect.isPending}
				>
					Disconnect
				</Button>
			</>
		);

	return (
		<>
			{contextHolder}
			<Button
				type="primary"
				onClick={handleConnect}
				loading={connect.isPending}
			>
				Connect
			</Button>
		</>
	);
}
