import { CloudDownloadOutlined, DeleteOutlined } from "@ant-design/icons";
import { Button, Card, message, Popconfirm } from "antd";
import { useMemo } from "react";
import {
	useDeleteAllModules,
	useDeleteModule,
	useDownloadAllModules,
	useDownloadModule,
	useGetModules,
} from "../../api/modules/modules";
import { useMutationOptions } from "../../hooks/useMutationOptions";
import { ModuleList } from "./ModuleList";

export function ModulesPanel() {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);

	const { data } = useGetModules();
	const download = useDownloadModule(opts("Module downloaded"));
	const remove = useDeleteModule(opts("Module deleted"));
	const downloadAll = useDownloadAllModules(opts("All modules downloaded"));
	const deleteAll = useDeleteAllModules(opts("All modules deleted"));

	const modules = useMemo(
		() => (Array.isArray(data?.data) ? data.data : []),
		[data],
	);

	return (
		<>
			{contextHolder}
			<Card
				title={`Modules (${modules.length})`}
				extra={
					<>
						<Button
							icon={<CloudDownloadOutlined />}
							loading={downloadAll.isPending}
							onClick={() => downloadAll.mutate()}
						>
							Download All
						</Button>
						<Popconfirm
							title="Delete all downloaded modules?"
							onConfirm={() => deleteAll.mutate()}
						>
							<Button
								danger
								icon={<DeleteOutlined />}
								loading={deleteAll.isPending}
								style={{ marginLeft: 8 }}
							>
								Delete All
							</Button>
						</Popconfirm>
					</>
				}
			>
				<ModuleList
					modules={modules}
					onDownload={(name) => download.mutate({ moduleName: name })}
					onDelete={(name) => remove.mutate({ moduleName: name })}
					downloadPending={download.isPending}
					downloadingName={download.variables?.moduleName}
				/>
			</Card>
		</>
	);
}
