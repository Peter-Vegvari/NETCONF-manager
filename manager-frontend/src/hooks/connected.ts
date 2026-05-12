import { useGetConnectionStatus } from "../api/connection/connection";

export const useConnected = () => useGetConnectionStatus().data?.data === true;
