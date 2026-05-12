import { Collapse } from "antd";
import type { ModuleSummary } from "../../api/model";
import { ModuleContent } from "./ModuleContent";
import { ModuleItemActions, ModuleItemLabel } from "./ModuleItem";

interface Props {
	module: ModuleSummary;
	onDownload: (name: string) => void;
	onDelete: (name: string) => void;
	downloadPending: boolean;
	downloadingName?: string;
}

export function ModuleCollapseItem({
	module: m,
	onDownload,
	onDelete,
	downloadPending,
	downloadingName,
}: Props) {
	return (
		<Collapse.Panel
			key={m.name}
			header={<ModuleItemLabel module={m} />}
			extra={
				<ModuleItemActions
					module={m}
					onDownload={onDownload}
					onDelete={onDelete}
					downloadPending={downloadPending}
					downloadingName={downloadingName}
				/>
			}
		>
			<ModuleContent module={m} />
		</Collapse.Panel>
	);
}
