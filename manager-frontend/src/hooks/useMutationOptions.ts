import { useQueryClient } from "@tanstack/react-query";
import type { message } from "antd";

export function useMutationOptions(
	msg: ReturnType<typeof message.useMessage>[0],
) {
	const queryClient = useQueryClient();
	return (text: string) => ({
		mutation: {
			onSuccess: (response: { status: number }) => {
				if (response.status >= 400) return msg.error(`Failed: ${text}`);
				queryClient.invalidateQueries({ queryKey: ["/api/v1/modules/"] });
				return msg.success(text);
			},
		},
	});
}
