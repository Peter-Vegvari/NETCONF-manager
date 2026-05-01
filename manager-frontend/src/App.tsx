import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { App as AntApp, ConfigProvider, Layout, Switch, Typography, theme } from "antd";
import { ConnectionForm } from "./components/ConnectionForm";
import { ModulesPanel } from "./components/ModulesPanel";

const queryClient = new QueryClient();

function App() {
  const [dark, setDark] = useState(window.matchMedia("(prefers-color-scheme: dark)").matches);

  return (
    <ConfigProvider theme={{ algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm }}>
      <AntApp style={{ minHeight: "100vh" }}>
        <QueryClientProvider client={queryClient}>
          <Layout style={{ minHeight: "100vh", padding: 24 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <Typography.Title level={2}>NETCONF Manager</Typography.Title>
              <Switch checkedChildren="Dark" unCheckedChildren="Light" checked={dark} onChange={setDark} />
            </div>
            <ConnectionForm />
            <ModulesPanel />
          </Layout>
          <ReactQueryDevtools />
        </QueryClientProvider>
      </AntApp>
    </ConfigProvider>
  );
}

export default App;
