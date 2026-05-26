import { useQueryClient } from "@tanstack/react-query";
import { Badge, Button, Card, Form, Input, InputNumber, Space } from "antd";
import type { Connection } from "@/api/model";
import { ConnectionButton } from "@/components/connection/ConnectionButton";
import { DisabledTooltip } from "@/components/DisabledTooltip";
import { useConnected } from "@/hooks/connected";

export function ConnectionForm() {
	const [form] = Form.useForm<Connection>();
	const queryClient = useQueryClient();
	const connected = useConnected();

	return (
		<Card
			title={
				<Space>
					Device Connection{" "}
					<Badge
						status={connected ? "success" : "default"}
						text={connected ? "Connected" : "Disconnected"}
					/>
				</Space>
			}
			style={{ marginBottom: 16 }}
		>
			<Form
				form={form}
				layout="inline"
				initialValues={{
					host: "notconf",
					port: 830,
					user_name: "admin",
					password: "admin",
				}}
			>
				<Form.Item name="host" label="Host">
					<Input />
				</Form.Item>
				<Form.Item name="port" label="Port">
					<InputNumber />
				</Form.Item>
				<Form.Item name="user_name" label="User">
					<Input />
				</Form.Item>
				<Form.Item name="password" label="Password">
					<Input.Password />
				</Form.Item>
				<Space>
					<ConnectionButton form={form} />
					<DisabledTooltip>
						<Button
							onClick={() => queryClient.refetchQueries()}
							disabled={!connected}
						>
							Refresh
						</Button>
					</DisabledTooltip>
				</Space>
			</Form>
		</Card>
	);
}
