import { Space } from "antd";
import type { DataStore } from "@/api/model";
import { CandidatePanel } from "./CandidatePanel";
import { RunningPanel } from "./RunningPanel";
import { StartupPanel } from "./StartupPanel";

export function DatastoreMenu({
	dataStore,
	setDataStore,
}: {
	dataStore: DataStore;
	setDataStore: (ds: DataStore) => void;
}) {
	return (
		<Space style={{ flexShrink: 0 }}>
			<RunningPanel
				active={dataStore === "running"}
				onBrowse={() => setDataStore("running")}
			/>
			<CandidatePanel
				active={dataStore === "candidate"}
				onBrowse={() => setDataStore("candidate")}
			/>
			<StartupPanel
				active={dataStore === "startup"}
				onBrowse={() => setDataStore("startup")}
			/>
		</Space>
	);
}
