import { Button, Card, Form, Input, InputNumber, Space, message } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { useConnect, useDisconnect } from "../api/connection/connection";
import type { Connection } from "../api/model";

export function ConnectionForm() {
  const [form] = Form.useForm<Connection>();
  const [msg, contextHolder] = message.useMessage();
  const queryClient = useQueryClient();

  const connectMutation = useConnect({
    mutation: {
      onSuccess: (res) => {
        if (res.status === 200) {
          queryClient.invalidateQueries();
          msg.success("Connected");
        } else {
          msg.error("Connection failed");
        }
      },
      onError: () => msg.error("Connection failed"),
    },
  });

  const disconnect = useDisconnect({
    mutation: {
      onSuccess: () => { queryClient.invalidateQueries(); msg.success("Disconnected"); },
    },
  });

  const handleConnect = async () => {
    const values = await form.validateFields();
    connectMutation.mutate({ data: values });
  };

  return (
    <>
      {contextHolder}
      <Card title="Device Connection" style={{ marginBottom: 16 }}>
        <Form
          form={form}
          layout="inline"
          initialValues={{ host: "10.41.101.188", port: 830, user_name: "admin_user", password: "Ericsson1234" }}
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
            <Button type="primary" onClick={handleConnect} loading={connectMutation.isPending}>
              Connect
            </Button>
            <Button danger onClick={() => disconnect.mutate()} loading={disconnect.isPending}>
              Disconnect
            </Button>
          </Space>
        </Form>
      </Card>
    </>
  );
}
