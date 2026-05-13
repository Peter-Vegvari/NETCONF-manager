import { useQueryClient } from "@tanstack/react-query";
import type { message } from "antd";

export function useMutationOptions(
	msg: ReturnType<typeof message.useMessage>[0],
) {
	const queryClient = useQueryClient();
	return (text: string) => ({
		mutation: {
			onSuccess: () => {
				queryClient.invalidateQueries({ queryKey: ["/api/v1/modules/"] });
				return msg.success(text);
			},
			onError: () => msg.error(`Failed: ${text}`),
		},
	});
}
