import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Layout, Typography } from "antd";
import { ConnectionForm } from "./components/ConnectionForm";
import { ModulesPanel } from "./components/ModulesPanel";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout style={{ minHeight: "100vh", padding: 24 }}>
        <Typography.Title level={2}>NETCONF Manager</Typography.Title>
        <ConnectionForm />
        <ModulesPanel />
      </Layout>
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
}

export default App;
