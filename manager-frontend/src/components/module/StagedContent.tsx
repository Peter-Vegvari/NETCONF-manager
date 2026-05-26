import { Empty, Spin, Typography } from "antd";
import { useGetStaged } from "@/api/datastore/datastore";
import type { ModuleSummary } from "@/api/model";

export function StagedContent({ module }: { module: ModuleSummary }) {
	const { data, isLoading } = useGetStaged(module.name);

	if (isLoading) return <Spin size="small" />;

	const diff = data?.data;
	if (!diff || Object.keys(diff).length === 0)
		return <Empty description="No staged changes" />;

	return (
		<Typography.Text>
			<pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>
				{JSON.stringify(diff, null, 2)}
			</pre>
		</Typography.Text>
	);
}
