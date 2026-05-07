import { Collapse } from "antd";
import type { SchemaNode } from "../../api/model";
import { getNestedValue } from "../../utils/schema";
import { SchemaNodeLabel } from "./SchemaNodeLabel";
import { SchemaLeafDetail } from "./SchemaLeafDetail";

export function SchemaTree({ node, data }: { node: SchemaNode; data?: Record<string, unknown> }) {
  if (!node.children) return null;
  const entries = Object.entries(node.children);
  return (
    <Collapse size="small" items={entries.map(([name, child]) => {
      const childData = getNestedValue(data, name);
      const isLeaf = !child.children;
      const isArray = Array.isArray(childData);
      return {
        key: name,
        label: <SchemaNodeLabel name={name} node={child} value={isLeaf ? childData : undefined} />,
        children: isLeaf ? (
          <SchemaLeafDetail node={child} value={childData} />
        ) : isArray ? (
          <Collapse size="small" items={childData.map((item: unknown, i: number) => ({
            key: i,
            label: <span>{name}[{i}]</span>,
            children: <SchemaTree node={child} data={item as Record<string, unknown>} />,
          }))} />
        ) : (
          <SchemaTree node={child} data={childData ?? data} />
        ),
      };
    })} />
  );
}
