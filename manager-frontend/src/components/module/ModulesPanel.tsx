import { CloudDownloadOutlined, DeleteOutlined } from "@ant-design/icons";
import { Button, Card, message, Popconfirm, Space } from "antd";
import { useMemo, useState } from "react";
import type { DataStore } from "@/api/model";
import {
	useDeleteAllModules,
	useDeleteModule,
	useDownloadAllModules,
	useDownloadModule,
	useGetModules,
} from "@/api/modules/modules";
import { DisabledTooltip, useDisabled } from "@/components/DisabledTooltip";
import { DatastoreMenu } from "@/components/datastore/DatastoreMenu";
import { useMutationOptions } from "@/hooks/useMutationOptions";
import { ModuleList } from "./ModuleList";

export function ModulesPanel() {
	const [msg, contextHolder] = message.useMessage();
	const opts = useMutationOptions(msg);
	const disabled = useDisabled();
	const [dataStore, setDataStore] = useState<DataStore>("running");

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
				title={
					<Space>
						{`Modules (${modules.length})`}
						<DatastoreMenu dataStore={dataStore} setDataStore={setDataStore} />
					</Space>
				}
				extra={
					<>
						<DisabledTooltip>
							<Button
								icon={<CloudDownloadOutlined />}
								loading={downloadAll.isPending}
								onClick={() => downloadAll.mutate()}
								disabled={disabled}
							>
								Download All
							</Button>
						</DisabledTooltip>
						<Popconfirm
							title="Delete all downloaded modules?"
							onConfirm={() => deleteAll.mutate()}
						>
							<DisabledTooltip>
								<Button
									danger
									icon={<DeleteOutlined />}
									loading={deleteAll.isPending}
									disabled={disabled}
									style={{ marginLeft: 8 }}
								>
									Delete All
								</Button>
							</DisabledTooltip>
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
					dataStore={dataStore}
				/>
			</Card>
		</>
	);
}
