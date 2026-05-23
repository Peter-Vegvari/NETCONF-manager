import { useMutation, useQueryClient } from "@tanstack/react-query";
import { App, Button, Descriptions, Input, Space } from "antd";
import { useState } from "react";
import { editConfig } from "../../api/datastore/datastore";
import type { DataStore, SchemaNode } from "../../api/model";

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
	const [editing, setEditing] = useState(false);
	const [inputValue, setInputValue] = useState(
		value != null ? String(value) : "",
	);
	const queryClient = useQueryClient();
	const { message } = App.useApp();

	const canEdit = node.config !== false && dataStore && moduleName && path;

	const mutation = useMutation({
		mutationFn: () => {
			if (!canEdit) return Promise.reject("Missing edit context");
			return editConfig(dataStore, {
				module_name: moduleName,
				path: path,
				value: inputValue,
			});
		},
		onSuccess: () => {
			message.success("Configuration updated");
			setEditing(false);
			queryClient.invalidateQueries({ queryKey: ["getModuleData"] });
			queryClient.invalidateQueries({ queryKey: ["getData"] });
		},
		onError: (err) => {
			message.error(`Edit failed: ${err}`);
		},
	});

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
			{canEdit && (
				<Descriptions.Item label="Edit">
					{editing ? (
						<Space.Compact>
							<Input
								size="small"
								value={inputValue}
								onChange={(e) => setInputValue(e.target.value)}
								onPressEnter={() => mutation.mutate()}
								style={{ width: 200 }}
							/>
							<Button
								size="small"
								type="primary"
								loading={mutation.isPending}
								onClick={() => mutation.mutate()}
							>
								Save
							</Button>
							<Button size="small" onClick={() => setEditing(false)}>
								Cancel
							</Button>
						</Space.Compact>
					) : (
						<Button size="small" onClick={() => setEditing(true)}>
							Edit
						</Button>
					)}
				</Descriptions.Item>
			)}
		</Descriptions>
	);
}
