import { GithubOutlined } from "@ant-design/icons";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import {
	App as AntApp,
	Button,
	ConfigProvider,
	Layout,
	Space,
	Switch,
	Typography,
	theme,
} from "antd";
import { useState } from "react";
import { useCookies } from "react-cookie";
import { ConnectionForm } from "@/components/connection/ConnectionForm";
import { DatastoresPanel } from "@/components/datastore/panels/DatastoresPanel";

const queryClient = new QueryClient({
	defaultOptions: { queries: { staleTime: 30_000 } },
});

function App() {
	const [cookies, setCookie] = useCookies(["theme"]);
	const [dark, setDark] = useState(
		cookies.theme != null
			? cookies.theme === "dark"
			: window.matchMedia("(prefers-color-scheme: dark)").matches,
	);

	const handleThemeChange = (value: boolean) => {
		setDark(value);
		setCookie("theme", value ? "dark" : "light", {
			path: "/",
		});
	};

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
							<Space>
								<Switch
									checkedChildren="Dark"
									unCheckedChildren="Light"
									checked={dark}
									onChange={handleThemeChange}
								/>
								<Button
									type="text"
									icon={<GithubOutlined style={{ fontSize: 24 }} />}
									href="https://github.com/Peter-Vegvari/NETCONF-manager"
									target="_blank"
								/>
							</Space>
						</div>
						<ConnectionForm />
						<DatastoresPanel />
					</Layout>
					<ReactQueryDevtools />
				</QueryClientProvider>
			</AntApp>
		</ConfigProvider>
	);
}

export default App;
