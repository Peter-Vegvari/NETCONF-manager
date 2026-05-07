import { message } from "antd";
import { useQueryClient } from "@tanstack/react-query";

export function useMutationOptions(msg: ReturnType<typeof message.useMessage>[0]) {
  const queryClient = useQueryClient();
  return (text: string) => ({
    mutation: {
      onSuccess: () => { queryClient.invalidateQueries(); return msg.success(text); },
      onError: () => msg.error(`Failed: ${text}`),
    },
  });
}
