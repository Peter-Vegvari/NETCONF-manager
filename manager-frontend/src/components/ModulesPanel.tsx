import { useMemo, useState } from "react";
import { Button, Card, Collapse, Descriptions, Input, Popconfirm, Select, Space, Tag, message } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { DeleteOutlined, DownloadOutlined, CloudDownloadOutlined } from "@ant-design/icons";
import { useGetModules, useDownloadModule, useDeleteModule, useDownloadAllModules, useDeleteAllModules, useGetData } from "../api/modules/modules";
import type { Module, SchemaNode } from "../api/model";

const statusColor: Record<Module["status"], string> = {
  remote: "blue",
  local: "green",
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function getNestedValue(data: any, key: string): any {
  if (!data || typeof data !== "object") return undefined;
  // key may be "module:name", strip prefix
  const localName = key.includes(":") ? key.split(":")[1] : key;
  // Try both prefixed and local
  return data[key] ?? data[localName];
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function SchemaTree({ node, data }: { node: SchemaNode; data?: any }) {
  if (!node.children) return null;
  const entries = Object.entries(node.children);
  return (
    <Collapse size="small" items={entries.map(([name, child]) => {
      const childData = getNestedValue(data, name);
      const isLeaf = !child.children;
      const isArray = Array.isArray(childData);
      return {
        key: name,
        label: (
          <span>
            {name} <Tag>{child.kind}</Tag>
            {child.mandatory && <Tag color="red">required</Tag>}
            {child.type && <Tag color="purple">{String(child.type["base"] ?? "")}</Tag>}
            {isLeaf && childData !== undefined && <Tag color="green">{String(childData)}</Tag>}
          </span>
        ),
        children: isLeaf ? (
          <Descriptions size="small" column={1}>
            {child.description && <Descriptions.Item label="Description">{child.description}</Descriptions.Item>}
            {child.default !== undefined && <Descriptions.Item label="Default">{String(child.default)}</Descriptions.Item>}
            {childData !== undefined && <Descriptions.Item label="Value">{String(childData)}</Descriptions.Item>}
          </Descriptions>
        ) : isArray ? (
          <Collapse size="small" items={childData.map((item: unknown, i: number) => ({
            key: i,
            label: <span>{name}[{i}]</span>,
            children: <SchemaTree node={child} data={item as Record<string, unknown>} />,
          }))} />
        ) : (
          <SchemaTree node={child} data={childData ?? data} />
        ),
      };
    })} />
  );
}

function ModuleContent({ module }: { module: Module }) {
  if (module.status !== "local") return <span>Download module to view schema.</span>;
  const children = module.schema_node?.children;
  if (!children) return <span>No schema available.</span>;
  const firstKey = Object.keys(children)[0];
  const topContainer = firstKey?.split(":")[1] ?? firstKey ?? "";

  return <ModuleSchemaWithData module={module} topContainer={topContainer} />;
}

function ModuleSchemaWithData({ module, topContainer }: { module: Module; topContainer: string }) {
  const { data, isLoading } = useGetData(module.name, topContainer, { query: { enabled: !!topContainer } });
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawData = data?.data as any;
  const dataObj = rawData?.[`${module.name}:${topContainer}`] ?? rawData?.[topContainer];

  if (isLoading) return <span>Loading...</span>;
  return <SchemaTree node={module.schema_node} data={rawData} />;
}

export function ModulesPanel() {
  const [msg, contextHolder] = message.useMessage();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [sort, setSort] = useState<"name" | "status">("name");

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

  const modules = useMemo(() => Array.isArray(data?.data) ? data.data : [], [data]);

  const filtered = useMemo(() => {
    let result = modules.filter((m) => m.name.toLowerCase().includes(search.toLowerCase()));
    if (statusFilter) result = result.filter((m) => m.status === statusFilter);
    result.sort((a, b) => sort === "name" ? a.name.localeCompare(b.name) : a.status.localeCompare(b.status));
    return result;
  }, [modules, search, statusFilter, sort]);

  return (
    <>
      {contextHolder}
      <Card title={`Modules (${filtered.length}/${modules.length})`} extra={<>
        <Button icon={<CloudDownloadOutlined />} loading={downloadAll.isPending} onClick={() => downloadAll.mutate()}>
          Download All
        </Button>
        <Popconfirm title="Delete all downloaded modules?" onConfirm={() => deleteAll.mutate()}>
          <Button danger icon={<DeleteOutlined />} loading={deleteAll.isPending} style={{ marginLeft: 8 }}>
            Delete All
          </Button>
        </Popconfirm>
      </>}>
        <Space style={{ marginBottom: 16, width: "100%" }}>
          <Input.Search placeholder="Filter by name" allowClear onChange={(e) => setSearch(e.target.value)} style={{ width: 250 }} />
          <Select placeholder="Status" allowClear onChange={setStatusFilter} style={{ width: 120 }}
            options={[{ value: "local", label: "Local" }, { value: "remote", label: "Remote" }]} />
          <Select value={sort} onChange={setSort} style={{ width: 140 }}
            options={[{ value: "name", label: "Sort: Name" }, { value: "status", label: "Sort: Status" }]} />
        </Space>
        {filtered.length === 0 ? "No modules found." : (
          <Collapse items={filtered.map((m) => ({
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
            children: <ModuleContent module={m} />,
          }))} />
        )}
      </Card>
    </>
  );
}
