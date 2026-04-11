import { Button, Card, Form, Input, InputNumber, Space } from "antd";
import { useConnect, useDisconnect } from "../api/default/default";

export function ConnectionForm() {
  const connect = useConnect();
  const disconnect = useDisconnect();

  return (
    <Card title="Device Connection" style={{ marginBottom: 16 }}>
      <Form
        layout="inline"
        initialValues={{ host: "notconf", port: 830, user_name: "admin", password: "admin" }}
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
