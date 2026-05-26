import { useQueries } from "@tanstack/react-query";
import { Collapse, Empty, Spin, Tag, Typography } from "antd";
import { getGetStagedQueryOptions } from "@/api/datastore/datastore";
import { useGetModules } from "@/api/modules/modules";

export function StagedPanel() {
	const { data: modulesData } = useGetModules();
	const modules = Array.isArray(modulesData?.data) ? modulesData.data : [];

	const stagedQueries = useQueries({
		queries: modules.map((m) => ({
			...getGetStagedQueryOptions(m.name),
			enabled: modules.length > 0,
		})),
	});

	const isLoading = stagedQueries.some((q) => q.isLoading);

	if (isLoading) return <Spin />;

	const items = modules
		.map((m, i) => {
			const diff = stagedQueries[i]?.data?.data;
			if (!diff || Object.keys(diff).length === 0) return null;
			return {
				key: m.name,
				label: (
					<>
						{m.name} <Tag color="blue">{Object.keys(diff).length} changes</Tag>
					</>
				),
				children: (
					<Typography.Text>
						<pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>
							{JSON.stringify(diff, null, 2)}
						</pre>
					</Typography.Text>
				),
			};
		})
		.filter(Boolean);

	if (items.length === 0) return <Empty description="No staged changes" />;

	return <Collapse items={items} />;
}
