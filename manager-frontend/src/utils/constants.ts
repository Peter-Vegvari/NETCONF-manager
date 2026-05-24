import type { ModuleSummary } from "@/api/model";

export const statusColor: Record<ModuleSummary["status"], string> = {
	remote: "blue",
	local: "green",
};
