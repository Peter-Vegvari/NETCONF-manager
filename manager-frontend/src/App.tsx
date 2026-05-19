import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import {
	App as AntApp,
	ConfigProvider,
	Layout,
	Switch,
	Typography,
	theme,
} from "antd";
import { useState } from "react";
import type { DataStore } from "./api/model";
import { ConnectionForm } from "./components/connection/ConnectionForm";
import { DatastoreMenu } from "./components/datastore/DatastoreMenu";
import { ModulesPanel } from "./components/module/ModulesPanel";

const queryClient = new QueryClient({
	defaultOptions: { queries: { staleTime: 30_000 } },
});

function App() {
	const [dark, setDark] = useState(
		window.matchMedia("(prefers-color-scheme: dark)").matches,
	);
	const [dataStore, setDataStore] = useState<DataStore>("running");

	return (
		<ConfigProvider
			theme={{ algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm }}
		>
			<AntApp style={{ minHeight: "100vh" }}>
				<QueryClientProvider client={queryClient}>
					<Layout style={{ minHeight: "100vh", padding: 24 }}>
						<div
							style={{
								display: "flex",
								justifyContent: "space-between",
								alignItems: "center",
							}}
						>
							<Typography.Title level={2}>NETCONF Manager</Typography.Title>
							<Switch
								checkedChildren="Dark"
								unCheckedChildren="Light"
								checked={dark}
								onChange={setDark}
							/>
						</div>
						<ConnectionForm />
						<div style={{ display: "flex", gap: 16 }}>
							<DatastoreMenu
								dataStore={dataStore}
								setDataStore={setDataStore}
							/>
							<div style={{ flex: 1, minWidth: 0 }}>
								<ModulesPanel dataStore={dataStore} />
							</div>
						</div>
					</Layout>
					<ReactQueryDevtools />
				</QueryClientProvider>
			</AntApp>
		</ConfigProvider>
	);
}

export default App;
