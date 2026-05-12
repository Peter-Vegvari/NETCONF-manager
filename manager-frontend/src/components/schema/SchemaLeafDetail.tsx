import { Descriptions } from "antd";
import type { SchemaNode } from "../../api/model";

interface Props {
	node: SchemaNode;
	value?: unknown;
}

export function SchemaLeafDetail({ node, value }: Props) {
	return (
		<Descriptions size="small" column={1}>
			{node.description && (
				<Descriptions.Item label="Description">
					{node.description}
				</Descriptions.Item>
			)}
			{node.default !== undefined && (
				<Descriptions.Item label="Default">
					{String(node.default)}
				</Descriptions.Item>
			)}
			{value !== undefined && (
				<Descriptions.Item label="Value">{String(value)}</Descriptions.Item>
			)}
		</Descriptions>
	);
}
