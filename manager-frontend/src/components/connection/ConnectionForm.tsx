import { Badge, Button, Card, Form, Input, InputNumber, Space, message } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { useConnect, useDisconnect, useGetConnectionStatus } from "../../api/connection/connection";
import type { Connection } from "../../api/model";

export function ConnectionForm() {
  const [form] = Form.useForm<Connection>();
  const [msg, contextHolder] = message.useMessage();
  const queryClient = useQueryClient();
  const { data: statusRes } = useGetConnectionStatus();
  const connected = statusRes?.data === true;

  const connectMutation = useConnect({
    mutation: {
      onSuccess: (res) => {
        if (res.status === 200) {
          msg.success("Connected");
          queryClient.refetchQueries();
        } else {
          msg.error("Connection failed");
        }
      },
      onError: () => msg.error("Connection failed"),
    },
  });

  const disconnect = useDisconnect({
    mutation: {
      onSuccess: () => { queryClient.refetchQueries(); msg.success("Disconnected"); },
      onError: () => { msg.error("Disconnect failed"); },
    },
  });

  const handleConnect = async () => {
    const values = await form.validateFields();
    connectMutation.mutate({ data: values });
  };

  return (
    <>
      {contextHolder}
      <Card title={<Space>Device Connection <Badge status={connected ? "success" : "default"} text={connected ? "Connected" : "Disconnected"} /></Space>} style={{ marginBottom: 16 }}>
        <Form
          form={form}
          layout="inline"
          initialValues={{ host: "10.41.104.26", port: 830, user_name: "admin_user", password: "Ericsson1234" }}
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
            <Button onClick={() => queryClient.refetchQueries()}>
              Refresh
            </Button>
          </Space>
        </Form>
      </Card>
    </>
  );
}
