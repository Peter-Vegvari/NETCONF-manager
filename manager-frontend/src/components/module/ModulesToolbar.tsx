import { Input, Select, Space } from "antd";

interface Props {
  onSearchChange: (value: string) => void;
  onStatusChange: (value: string | undefined) => void;
  sort: "name" | "status";
  onSortChange: (value: "name" | "status") => void;
}

export function ModulesToolbar({ onSearchChange, onStatusChange, sort, onSortChange }: Props) {
  return (
    <Space style={{ marginBottom: 16, width: "100%" }}>
      <Input.Search placeholder="Filter by name" allowClear onChange={(e) => onSearchChange(e.target.value)} style={{ width: 250 }} />
      <Select placeholder="Status" allowClear onChange={onStatusChange} style={{ width: 120 }}
        options={[{ value: "local", label: "Local" }, { value: "remote", label: "Remote" }]} />
      <Select value={sort} onChange={onSortChange} style={{ width: 140 }}
        options={[{ value: "name", label: "Sort: Name" }, { value: "status", label: "Sort: Status" }]} />
    </Space>
  );
}
