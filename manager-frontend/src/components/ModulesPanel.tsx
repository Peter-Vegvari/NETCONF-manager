import { Button, Card, List, Popconfirm, Tag } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { DeleteOutlined, DownloadOutlined, ThunderboltOutlined } from "@ant-design/icons";
import { useGetModules, useDownloadModule, useDeleteModule, useGenerateModule } from "../api/modules/modules";
import type { Module } from "../api/model";

const statusColor: Record<Module["status"], string> = {
  remote: "blue",
  local: "orange",
  generated: "green",
};

export function ModulesPanel() {
  const queryClient = useQueryClient();
  const invalidate = { mutation: { onSuccess: () => queryClient.invalidateQueries() } };
  const { data } = useGetModules();
  const download = useDownloadModule(invalidate);
  const remove = useDeleteModule(invalidate);
  const generate = useGenerateModule(invalidate);

  const modules = Array.isArray(data?.data) ? data.data : [];

  return (
    <Card title={`Modules (${modules.length})`}>
      <List
        size="small"
        dataSource={modules}
        locale={{ emptyText: "No modules found." }}
        renderItem={(m) => (
          <List.Item
            actions={[
              m.status === "remote" && (
                <Button
                  key="dl"
                  type="text"
                  size="small"
                  icon={<DownloadOutlined />}
                  loading={download.isPending && download.variables?.moduleName === m.name}
                  onClick={() => download.mutate({ moduleName: m.name })}
                />
              ),
              m.status === "local" && (
                <Button
                  key="gen"
                  type="text"
                  size="small"
                  icon={<ThunderboltOutlined />}
                  loading={generate.isPending && generate.variables?.moduleName === m.name}
                  onClick={() => generate.mutate({ moduleName: m.name })}
                />
              ),
              m.status !== "remote" && (
                <Popconfirm
                  key="rm"
                  title="Delete this module?"
                  onConfirm={() => remove.mutate({ moduleName: m.name })}
                >
                  <Button danger type="text" size="small" icon={<DeleteOutlined />} />
                </Popconfirm>
              ),
            ].filter(Boolean)}
          >
            <span>
              {m.name} <Tag color={statusColor[m.status]}>{m.status}</Tag>
            </span>
          </List.Item>
        )}
      />
    </Card>
  );
}
