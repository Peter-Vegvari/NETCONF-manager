import { Collapse } from "antd";
import type { ReactNode } from "react";
import type { DataStore, SchemaNode } from "@/api/model";
import { getNestedValue } from "@/utils/schema";
import { SchemaLeafDetail } from "./SchemaLeafDetail";
import { SchemaNodeLabel } from "./SchemaNodeLabel";

function localName(name: string): string {
	return name.includes(":") ? name.split(":")[1] : name;
}

function renderChildren(
	name: string,
	child: SchemaNode,
	childData: unknown,
	dataStore?: DataStore,
	moduleName?: string,
	path?: string,
): ReactNode {
	const isLeaf = !child.children;
	const childPath = path ? `${path}/${localName(name)}` : localName(name);

	if (isLeaf) {
		return (
			<SchemaLeafDetail
				node={child}
				value={childData}
				dataStore={dataStore}
				moduleName={moduleName}
				path={childPath}
			/>
		);
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
						children: (
							<SchemaTree
								node={child}
								data={record}
								dataStore={dataStore}
								moduleName={moduleName}
								path={childPath}
							/>
						),
					};
				})}
			/>
		);
	}

	return (
		<SchemaTree
			node={child}
			data={(childData ?? undefined) as Record<string, unknown>}
			dataStore={dataStore}
			moduleName={moduleName}
			path={childPath}
		/>
	);
}

export function SchemaTree({
	node,
	data,
	dataStore,
	moduleName,
	path,
}: {
	node: SchemaNode;
	data?: Record<string, unknown>;
	dataStore?: DataStore;
	moduleName?: string;
	path?: string;
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
			children: renderChildren(
				name,
				child,
				childData,
				dataStore,
				moduleName,
				path,
			),
		};
	});

	return <Collapse size="small" items={items} />;
}
