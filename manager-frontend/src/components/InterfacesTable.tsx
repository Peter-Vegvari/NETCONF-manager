import { Button, Card, Switch, Table, Popconfirm } from "antd";
import { useGetInterfaces, usePutInterface, useDeleteInterface } from "../api/default/default";

export function InterfacesTable() {
  const { data, isLoading, error } = useGetInterfaces();
  const update = usePutInterface();
  const remove = useDeleteInterface();

  if (error) return <Card>Connect to a device first.</Card>;

  const raw = data?.data?.data?.interfaces?.interface ?? data?.data?.interfaces?.interface ?? [];
  const interfaces = Array.isArray(raw) ? raw : [raw];

  const columns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Type", dataIndex: "type", key: "type" },
    {
      title: "Enabled",
      dataIndex: "enabled",
      key: "enabled",
      render: (val: string, record: Record<string, string>) => (
        <Switch
          checked={val === "true"}
          onChange={() => update.mutate({ name: record.name })}
        />
      ),
    },
    {
      title: "Actions",
      key: "actions",
      render: (_: unknown, record: Record<string, string>) => (
        <Popconfirm title="Delete this interface?" onConfirm={() => remove.mutate({ name: record.name })}>
          <Button danger size="small">Delete</Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <Card title="ietf-interfaces:interfaces">
      <Table
        dataSource={interfaces}
        columns={columns}
        rowKey="name"
        loading={isLoading}
        pagination={false}
      />
    </Card>
  );
}
