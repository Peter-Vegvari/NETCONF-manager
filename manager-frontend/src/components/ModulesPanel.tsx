import { Button, Card, Flex, Popconfirm, Typography } from "antd";
import { useQueryClient } from "@tanstack/react-query";
import {
  useGetAvailableModules,
  useGetModules,
  useDownloadModule,
  useDeleteModule,
} from "../api/default/default";

export function ModulesPanel() {
  const queryClient = useQueryClient();
  const available = useGetAvailableModules();
  const downloaded = useGetModules();
  const download = useDownloadModule({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });
  const remove = useDeleteModule({
    mutation: { onSuccess: () => queryClient.invalidateQueries() },
  });

  const downloadedSet = new Set(downloaded.data?.data ?? []);
  const availableModules = Array.isArray(available.data?.data) ? available.data.data : null;
  const downloadedModules = Array.isArray(downloaded.data?.data) ? downloaded.data.data : [];

  return (
    <Flex vertical gap={16}>
      <Card title="Available Modules" loading={available.isLoading}>
        {!availableModules ? (
          <Typography.Text type="secondary">Connect to a device first.</Typography.Text>
        ) : (
          <Flex vertical gap={8}>
            {availableModules.map((name) => (
              <Flex key={name} justify="space-between" align="center">
                <span>{name}</span>
                <Button
                  size="small"
                  disabled={downloadedSet.has(`${name}.yang`)}
                  loading={download.isPending && download.variables?.moduleName === name}
                  onClick={() => download.mutate({ moduleName: name })}
                >
                  {downloadedSet.has(`${name}.yang`) ? "Downloaded" : "Download"}
                </Button>
              </Flex>
            ))}
          </Flex>
        )}
      </Card>

      <Card title="Downloaded Modules" loading={downloaded.isLoading}>
        <Flex vertical gap={8}>
          {downloadedModules.map((name) => (
            <Flex key={name} justify="space-between" align="center">
              <Typography.Text code>{name}</Typography.Text>
              <Popconfirm
                title="Delete this module?"
                onConfirm={() => remove.mutate({ moduleName: name.replace(/\.yang$/, "") })}
              >
                <Button danger size="small">Delete</Button>
              </Popconfirm>
            </Flex>
          ))}
        </Flex>
      </Card>
    </Flex>
  );
}
