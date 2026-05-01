import { Card, Collapse, Descriptions, Tag } from "antd";
import { useGetSchema } from "../api/schema/schema";
import type { SchemaNode } from "../api/model";

function SchemaTree({ node }: { node: SchemaNode }) {
  if (!node.children) return null;
  return (
    <Collapse size="small" items={Object.entries(node.children).map(([name, child]) => ({
      key: name,
      label: <span>{name} <Tag>{child.kind}</Tag>{child.mandatory && <Tag color="red">required</Tag>}{child.type && <Tag color="purple">{String(child.type["base"] ?? "")}</Tag>}</span>,
      children: child.children ? <SchemaTree node={child} /> : (
        <Descriptions size="small" column={1}>
          {child.description && <Descriptions.Item label="Description">{child.description}</Descriptions.Item>}
          {child.default !== undefined && <Descriptions.Item label="Default">{String(child.default)}</Descriptions.Item>}
        </Descriptions>
      ),
    }))} />
  );
}

export function SchemaPanel() {
  const { data } = useGetSchema();

  return (
    <Card title="Schema">
      {data?.data?.children ? <SchemaTree node={data.data} /> : "No schema available."}
    </Card>
  );
}
