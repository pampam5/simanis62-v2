import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
// Figtree - #1 UI Design Font by Erik Kennedy (adhamdannaway.com)
// Modern, friendly, versatile - combines best parts of top typefaces
// Perfect for professional desktop applications
import "@fontsource-variable/figtree";
// Geist Mono - Professional monospace by Vercel for code/numbers
import "@fontsource-variable/geist-mono";
import "./index.css";
import { ErrorBoundary } from "./components/layout/error-boundary";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
);
