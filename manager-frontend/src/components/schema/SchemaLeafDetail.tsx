import { Typography } from "antd";
import type { DataStore, SchemaNode } from "@/api/model";
import { EditableValue } from "@/components/schema/EditableValue";

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

	if (canEdit) {
		return (
			<EditableValue
				value={value != null ? String(value) : ""}
				dataStore={dataStore}
				moduleName={moduleName}
				path={path}
			/>
		);
	}

	if (value !== undefined) {
		return <Typography.Text code>{String(value)}</Typography.Text>;
	}

	return null;
}
