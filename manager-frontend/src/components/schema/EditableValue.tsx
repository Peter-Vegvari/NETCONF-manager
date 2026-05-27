import { useQueryClient } from "@tanstack/react-query";
import { App, Button, Input, Space, Typography } from "antd";
import { useState } from "react";
import {
	getGetDataQueryKey,
	getGetModuleDataQueryKey,
	useEditConfig,
} from "@/api/datastore/datastore";
import type { DataStore } from "@/api/model";

interface Props {
	value: string;
	dataStore: DataStore;
	moduleName: string;
	path: string;
}

export function EditableValue({ value, dataStore, moduleName, path }: Props) {
	const [editing, setEditing] = useState(false);
	const [inputValue, setInputValue] = useState(value);
	const queryClient = useQueryClient();
	const { message } = App.useApp();

	const mutation = useEditConfig({
		mutation: {
			onSuccess: () => {
				message.success("Configuration updated");
				setEditing(false);
				queryClient.invalidateQueries({
					queryKey: getGetModuleDataQueryKey(dataStore, moduleName),
				});
				queryClient.invalidateQueries({
					queryKey: getGetDataQueryKey(dataStore, moduleName, path),
				});
			},
			onError: (err) => {
				message.error(`Edit failed: ${err}`);
			},
		},
	});

	if (!editing) {
		return (
			<Typography.Text
				code
				style={{ cursor: "pointer" }}
				onClick={() => {
					setInputValue(value);
					setEditing(true);
				}}
			>
				{value || <em>empty</em>}
			</Typography.Text>
		);
	}

	return (
		<Space.Compact>
			<Input
				size="small"
				value={inputValue}
				onChange={(e) => setInputValue(e.target.value)}
				onPressEnter={() =>
					mutation.mutate({
						dataStore,
						data: { module_name: moduleName, path, value: inputValue },
					})
				}
				autoFocus
				style={{ width: 200 }}
			/>
			<Button
				size="small"
				type="primary"
				loading={mutation.isPending}
				onClick={() =>
					mutation.mutate({
						dataStore,
						data: { module_name: moduleName, path, value: inputValue },
					})
				}
			>
				Save
			</Button>
			<Button size="small" onClick={() => setEditing(false)}>
				Cancel
			</Button>
		</Space.Compact>
	);
}
