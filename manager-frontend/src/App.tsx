import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import axios from "axios"
import { DatePicker } from 'antd';
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const defaultQueryFn = async ({ queryKey }) => {
  const { data } = await axios.get(
    `http://jsonplaceholder.typicode.com${queryKey[0]}`,
  )
  return data
}

// provide the default query function to your app with defaultOptions
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: defaultQueryFn,
    },
  },
})


function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <DatePicker></DatePicker>
      </QueryClientProvider>
      <ReactQueryDevtools/>
    </>
  )
}

export default App
