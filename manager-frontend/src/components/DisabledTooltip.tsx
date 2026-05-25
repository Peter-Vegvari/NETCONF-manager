import { Tooltip } from "antd";
import type { ReactNode } from "react";
import { useConnected } from "@/hooks/connected";

export function DisabledTooltip({ children }: { children: ReactNode }) {
	const connected = useConnected();
	if (connected) return children;
	return (
		<Tooltip title="Connect first to a NETCONF device">{children}</Tooltip>
	);
}

export function useDisabled() {
	return !useConnected();
}
