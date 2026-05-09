import { Tag } from "antd";
import type { SchemaNode } from "../../api/model";

interface Props {
  name: string;
  node: SchemaNode;
  value?: unknown;
}

export function SchemaNodeLabel({ name, node, value }: Props) {
  const isLeaf = !node.children;
  return (
    <span>
      {name}
      <Tag>{node.kind}</Tag>
      {node.mandatory && <Tag color="red">required</Tag>}
      {node.type && <Tag color="purple">{String(node.type["base"] ?? "")}</Tag>}
      {node.config === false && <Tag color="orange">read-only</Tag>}
      {isLeaf && value !== undefined && <Tag color="green">{String(value)}</Tag>}
    </span>
  );
}
