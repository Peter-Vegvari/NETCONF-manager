import { Button, Card, Collapse, Descriptions, Popconfirm, Spin, Tag, message } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { DeleteOutlined, DownloadOutlined, CloudDownloadOutlined } from "@ant-design/icons";
import { useGetModules, useDownloadModule, useDeleteModule, useDownloadAllModules, useDeleteAllModules } from "../api/modules/modules";
import { useGetModuleSchema } from "../api/schema/schema";
import type { Module, SchemaNode } from "../api/model";

const statusColor: Record<Module["status"], string> = {
  remote: "blue",
  local: "green",
};

function SchemaTree({ node }: { node: SchemaNode }) {
  if (!node.children) return null;
  return (
    <Collapse size="small" items={Object.entries(node.children).map(([name, child]) => ({
      key: name,
      label: <span>{name} <Tag>{child.kind}</Tag>{child.mandatory && <Tag color="red">required</Tag>}{child.type && <Tag color="purple">{String(child.type["base"] ?? "")}</Tag>}</span>,
      children: child.children ? <SchemaTree node={child} /> : (
        <Descriptions size="small" column={1}>
          {child.description && <Descriptions.Item label="Description">{child.description}</Descriptions.Item>}
          {child.default !== undefined && <Descriptions.Item label="Default">{String(child.default)}</Descriptions.Item>}
        </Descriptions>
      ),
    }))} />
  );
}

function ModuleSchema({ moduleName }: { moduleName: string }) {
  const { data, isLoading } = useGetModuleSchema(moduleName);

  if (isLoading) return <Spin size="small" />;
  if (!data?.data?.children || Object.keys(data.data.children).length === 0) return <span>No schema available.</span>;
  return <SchemaTree node={data.data} />;
}

export function ModulesPanel() {
  const [msg, contextHolder] = message.useMessage();
  const queryClient = useQueryClient();

  const onSuccess = (text: string) => ({ mutation: { onSuccess: () => { queryClient.invalidateQueries(); msg.success(text); }, onError: () => msg.error(`Failed: ${text}`) } });

  const { data } = useGetModules();
  const download = useDownloadModule(onSuccess("Module downloaded"));
  const remove = useDeleteModule(onSuccess("Module deleted"));

  const downloadAll = useDownloadAllModules({
    mutation: { onSuccess: () => { queryClient.invalidateQueries(); msg.success("All modules downloaded"); }, onError: () => msg.error("Failed to download all modules") },
  });

  const deleteAll = useDeleteAllModules({
    mutation: { onSuccess: () => { queryClient.invalidateQueries(); msg.success("All modules deleted"); }, onError: () => msg.error("Failed to delete all modules") },
  });

  const modules = Array.isArray(data?.data) ? data.data : [];

  return (
    <>
      {contextHolder}
      <Card title={`Modules (${modules.length})`} extra={<>
        <Button icon={<CloudDownloadOutlined />} loading={downloadAll.isPending} onClick={() => downloadAll.mutate()}>
          Download All
        </Button>
        <Popconfirm title="Delete all downloaded modules?" onConfirm={() => deleteAll.mutate()}>
          <Button danger icon={<DeleteOutlined />} loading={deleteAll.isPending} style={{ marginLeft: 8 }}>
            Delete All
          </Button>
        </Popconfirm>
      </>}>
        {modules.length === 0 ? "No modules found." : (
          <Collapse items={modules.map((m) => ({
            key: m.name,
            label: <span>{m.name} <Tag color={statusColor[m.status]}>{m.status}</Tag></span>,
            extra: m.status === "remote" ? (
              <Button type="text" size="small" icon={<DownloadOutlined />}
                loading={download.isPending && download.variables?.moduleName === m.name}
                onClick={(e) => { e.stopPropagation(); download.mutate({ moduleName: m.name }); }} />
            ) : (
              <Popconfirm title="Delete this module?" onConfirm={() => remove.mutate({ moduleName: m.name })} onPopupClick={(e) => e.stopPropagation()}>
                <Button danger type="text" size="small" icon={<DeleteOutlined />} onClick={(e) => e.stopPropagation()} />
              </Popconfirm>
            ),
            children: m.status === "local" ? <ModuleSchema moduleName={m.name} /> : <span>Download module to view schema.</span>,
          }))} />
        )}
      </Card>
    </>
  );
}
