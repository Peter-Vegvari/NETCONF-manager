import { Button, Card, List, Popconfirm, Tag } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import { DeleteOutlined, DownloadOutlined } from "@ant-design/icons";
import { useGetModules, useDownloadModule, useDeleteModule } from "../api/modules/modules";

export function ModulesPanel() {
  const queryClient = useQueryClient();
  const { data } = useGetModules();
  const download = useDownloadModule({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });
  const remove = useDeleteModule({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });

  const modules = Array.isArray(data?.data) ? data.data : [];

  return (
    <Card title={`Modules (${modules.length})`}>
      <List
        size="small"
        dataSource={modules}
        locale={{ emptyText: "Connect to a device first." }}
        renderItem={(m) => (
          <List.Item
            actions={[
              m.downloadable ? (
                <Button
                  key="dl"
                  type="text"
                  size="small"
                  icon={<DownloadOutlined />}
                  loading={download.isPending && download.variables?.moduleName === m.name}
                  onClick={() => download.mutate({ moduleName: m.name })}
                />
              ) : (
                <Popconfirm
                  key="rm"
                  title="Delete this module?"
                  onConfirm={() => remove.mutate({ moduleName: m.name })}
                >
                  <Button danger type="text" size="small" icon={<DeleteOutlined />} />
                </Popconfirm>
              ),
            ]}
          >
            <span>
              {m.name} {m.downloadable && <Tag color="blue">available</Tag>}
            </span>
          </List.Item>
        )}
      />
    </Card>
  );
}
