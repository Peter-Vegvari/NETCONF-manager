import { Descriptions } from "antd";

interface Props {
	description?: string | null;
	defaultValue?: unknown;
}

export function LeafMetadata({ description, defaultValue }: Props) {
	if (!description && defaultValue === undefined) return null;

	return (
		<>
			{description && (
				<Descriptions.Item label="Description">{description}</Descriptions.Item>
			)}
			{defaultValue !== undefined && (
				<Descriptions.Item label="Default">
					{String(defaultValue)}
				</Descriptions.Item>
			)}
		</>
	);
}
