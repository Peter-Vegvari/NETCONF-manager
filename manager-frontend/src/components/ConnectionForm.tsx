import { Button, Card, Form, Input, InputNumber, Space } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { useConnect, useDisconnect } from "../api/default/default";

export function ConnectionForm() {
  const queryClient = useQueryClient();
  const connect = useConnect({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });
  const disconnect = useDisconnect({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });

  return (
    <Card title="Device Connection" style={{ marginBottom: 16 }}>
      <Form
        layout="inline"
        initialValues={{ host: "10.41.102.78", port: 830, user_name: "admin_user", password: "Ericsson1234" }}
        onFinish={(values) => connect.mutate({ data: values })}
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
          <Button type="primary" htmlType="submit" loading={connect.isPending}>
            Connect
          </Button>
          <Button danger onClick={() => disconnect.mutate()} loading={disconnect.isPending}>
            Disconnect
          </Button>
        </Space>
      </Form>
    </Card>
  );
}
