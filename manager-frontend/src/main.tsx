import { StrictMode } from "react";
import { CookiesProvider } from "react-cookie";
import { createRoot } from "react-dom/client";
import "@/index.css";
import App from "@/App.tsx";

createRoot(document.getElementById("root") as HTMLElement).render(
	<StrictMode>
		<CookiesProvider>
			<App />
		</CookiesProvider>
	</StrictMode>,
);
