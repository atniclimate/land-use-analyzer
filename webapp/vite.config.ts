import { fileURLToPath, URL } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// base is "/land-use-analyzer/" in production so the GitHub Pages project site
// resolves assets correctly. The router reads import.meta.env.BASE_URL to match.
export default defineConfig(({ command }) => ({
  base: command === "build" ? "/land-use-analyzer/" : "/",
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
  },
}));
