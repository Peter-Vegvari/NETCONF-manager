import { Card } from "antd";
import { useState } from "react";
import type { DataStore } from "@/api/model";
import { DatastoreMenu } from "@/components/datastore/DatastoreMenu";
import { ModuleList } from "@/components/module/ModuleList";

export function DatastoresPanel() {
	const [dataStore, setDataStore] = useState<DataStore>("running");
	const [showStaged, setShowStaged] = useState(false);

	const handleSetDataStore = (ds: DataStore) => {
		setShowStaged(false);
		setDataStore(ds);
	};

	return (
		<Card
			title={
				<DatastoreMenu
					dataStore={dataStore}
					setDataStore={handleSetDataStore}
					showStaged={showStaged}
					onStaged={() => setShowStaged((v) => !v)}
				/>
			}
		>
			<ModuleList
				dataStore={dataStore}
				view={showStaged ? "staged" : "browse"}
			/>
		</Card>
	);
}
