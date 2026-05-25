import { useState } from "react";
import type { DataStore } from "@/api/model";
import { ModuleList } from "./ModuleList";

export function ModulesPanel() {
	const [dataStore] = useState<DataStore>("running");

	return <ModuleList dataStore={dataStore} />;
}
