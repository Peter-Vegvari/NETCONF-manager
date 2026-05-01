import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Layout, Tabs, Typography } from "antd";
import { ConnectionForm } from "./components/ConnectionForm";
import { ModulesPanel } from "./components/ModulesPanel";
import { SchemaPanel } from "./components/SchemaPanel";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout style={{ minHeight: "100vh", padding: 24 }}>
        <Typography.Title level={2}>NETCONF Manager</Typography.Title>
        <ConnectionForm />
        <Tabs items={[
          { key: "modules", label: "Modules", children: <ModulesPanel /> },
          { key: "schemas", label: "Schemas", children: <SchemaPanel /> },
        ]} />
      </Layout>
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
}

export default App;
