import { Descriptions } from "antd";
import type { DataStore, SchemaNode } from "@/api/model";
import { EditableValue } from "./EditableValue";
import { LeafMetadata } from "./LeafMetadata";

interface Props {
	node: SchemaNode;
	value?: unknown;
	dataStore?: DataStore;
	moduleName?: string;
	path?: string;
}

export function SchemaLeafDetail({
	node,
	value,
	dataStore,
	moduleName,
	path,
}: Props) {
	const canEdit = node.config !== false && dataStore && moduleName && path;

	return (
		<Descriptions size="small" column={1}>
			<LeafMetadata
				description={node.description}
				defaultValue={node.default}
			/>
			{value !== undefined && (
				<Descriptions.Item label="Value">{String(value)}</Descriptions.Item>
			)}
			{canEdit && (
				<Descriptions.Item label="Edit">
					<EditableValue
						value={value != null ? String(value) : ""}
						dataStore={dataStore}
						moduleName={moduleName}
						path={path}
					/>
				</Descriptions.Item>
			)}
		</Descriptions>
	);
}
