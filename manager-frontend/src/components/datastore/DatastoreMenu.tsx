import { Space, Typography } from "antd";
import type { DataStore } from "@/api/model";
import { CandidatePanel } from "@/components/datastore/panels/CandidatePanel";
import { RunningPanel } from "@/components/datastore/panels/RunningPanel";
import { StartupPanel } from "@/components/datastore/panels/StartupPanel";

export function DatastoreMenu({
	dataStore,
	setDataStore,
	showStaged,
	onStaged,
}: {
	dataStore: DataStore;
	setDataStore: (ds: DataStore) => void;
	showStaged: boolean;
	onStaged: () => void;
}) {
	return (
		<Space style={{ flexShrink: 0 }}>
			<Typography.Title level={5} style={{ margin: 0 }}>
				Datastores
			</Typography.Title>
			<RunningPanel
				active={dataStore === "running"}
				onBrowse={() => setDataStore("running")}
			/>
			<CandidatePanel
				active={dataStore === "candidate"}
				onBrowse={() => setDataStore("candidate")}
				showStaged={showStaged}
				onStaged={onStaged}
			/>
			<StartupPanel
				active={dataStore === "startup"}
				onBrowse={() => setDataStore("startup")}
			/>
		</Space>
	);
}
