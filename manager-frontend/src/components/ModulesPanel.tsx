import { Button, Card, List, Popconfirm, Tag, message } from "antd";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { DeleteOutlined, DownloadOutlined, CloudDownloadOutlined } from "@ant-design/icons";
import { useGetModules, useDownloadModule, useDeleteModule } from "../api/modules/modules";
import type { Module } from "../api/model";

const statusColor: Record<Module["status"], string> = {
  remote: "blue",
  local: "green",
};

export function ModulesPanel() {
  const [msg, contextHolder] = message.useMessage();
  const queryClient = useQueryClient();

  const onSuccess = (text: string) => ({ mutation: { onSuccess: () => { queryClient.invalidateQueries(); msg.success(text); }, onError: () => msg.error(`Failed: ${text}`) } });

  const { data } = useGetModules();
  const download = useDownloadModule(onSuccess("Module downloaded"));
  const remove = useDeleteModule(onSuccess("Module deleted"));

  const downloadAll = useMutation({
    mutationFn: async () => { const r = await fetch("/modules/download-all", { method: "POST" }); if (!r.ok) throw new Error(); },
    onSuccess: () => { queryClient.invalidateQueries(); msg.success("All modules downloaded"); },
    onError: () => msg.error("Failed to download all modules"),
  });

  const deleteAll = useMutation({
    mutationFn: async () => { const r = await fetch("/modules/", { method: "DELETE" }); if (!r.ok) throw new Error(); },
    onSuccess: () => { queryClient.invalidateQueries(); msg.success("All modules deleted"); },
    onError: () => msg.error("Failed to delete all modules"),
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
        <List
          size="small"
          dataSource={modules}
          locale={{ emptyText: "No modules found." }}
          renderItem={(m) => (
            <List.Item
              actions={[
                m.status === "remote" && (
                  <Button key="dl" type="text" size="small" icon={<DownloadOutlined />}
                    loading={download.isPending && download.variables?.moduleName === m.name}
                    onClick={() => download.mutate({ moduleName: m.name })} />
                ),
                m.status !== "remote" && (
                  <Popconfirm key="rm" title="Delete this module?" onConfirm={() => remove.mutate({ moduleName: m.name })}>
                    <Button danger type="text" size="small" icon={<DeleteOutlined />} />
                  </Popconfirm>
                ),
              ].filter(Boolean)}
            >
              <span>{m.name} <Tag color={statusColor[m.status]}>{m.status}</Tag></span>
            </List.Item>
          )}
        />
      </Card>
    </>
  );
}
