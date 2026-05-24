import { Card } from "antd";
import { useState } from "react";
import type { DataStore } from "../../api/model";
import { ModuleList } from "../module/ModuleList";
import { DatastoreMenu } from "./DatastoreMenu";

export function DatastoresPanel() {
	const [dataStore, setDataStore] = useState<DataStore>("running");

	return (
		<Card
			title={
				<DatastoreMenu dataStore={dataStore} setDataStore={setDataStore} />
			}
		>
			<ModuleList dataStore={dataStore} />
		</Card>
	);
}
