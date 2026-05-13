import { DatabaseOutlined } from "@ant-design/icons";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import {
	App as AntApp,
	ConfigProvider,
	Layout,
	Menu,
	Switch,
	Typography,
	theme,
} from "antd";
import { useState } from "react";
import type { DataStore } from "./api/model";
import { ConnectionForm } from "./components/connection/ConnectionForm";
import { ModulesPanel } from "./components/module/ModulesPanel";

const queryClient = new QueryClient({
	defaultOptions: { queries: { staleTime: 30_000 } },
});

const datastoreItems = [
	{ key: "running", icon: <DatabaseOutlined />, label: "Running" },
	{ key: "candidate", icon: <DatabaseOutlined />, label: "Candidate" },
	{ key: "startup", icon: <DatabaseOutlined />, label: "Startup" },
];

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
							<Menu
								mode="vertical"
								selectedKeys={[dataStore]}
								items={datastoreItems}
								onClick={({ key }) => setDataStore(key as DataStore)}
								style={{ width: 160, flexShrink: 0 }}
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
