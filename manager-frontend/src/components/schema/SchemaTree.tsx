import { Collapse } from "antd";
import type { ReactNode } from "react";
import type { SchemaNode } from "../../api/model";
import { getNestedValue } from "../../utils/schema";
import { SchemaLeafDetail } from "./SchemaLeafDetail";
import { SchemaNodeLabel } from "./SchemaNodeLabel";

function renderChildren(
	name: string,
	child: SchemaNode,
	childData: unknown,
): ReactNode {
	const isLeaf = !child.children;

	if (isLeaf) {
		return <SchemaLeafDetail node={child} value={childData} />;
	}

	if (Array.isArray(childData)) {
		return (
			<Collapse
				size="small"
				items={childData.map((item: unknown, i: number) => {
					const record = item as Record<string, unknown>;
					const firstValue = Object.values(record)[0];
					return {
						key: i,
						label: (
							<span>
								{firstValue != null ? String(firstValue) : `${name}[${i}]`}
							</span>
						),
						children: <SchemaTree node={child} data={record} />,
					};
				})}
			/>
		);
	}

	return (
		<SchemaTree
			node={child}
			data={(childData ?? undefined) as Record<string, unknown>}
		/>
	);
}

export function SchemaTree({
	node,
	data,
}: {
	node: SchemaNode;
	data?: Record<string, unknown>;
}) {
	if (!node.children) return null;

	const items = Object.entries(node.children).map(([name, child]) => {
		const childData = getNestedValue(data, name);
		const isLeaf = !child.children;

		return {
			key: name,
			label: (
				<SchemaNodeLabel
					name={name}
					node={child}
					value={isLeaf ? childData : undefined}
				/>
			),
			children: renderChildren(name, child, childData),
		};
	});

	return <Collapse size="small" items={items} />;
}
