// Copy index.html to 404.html so client-side routes resolve on GitHub Pages,
// which serves 404.html for unknown paths on a static site.
import { copyFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const distDir = resolve(import.meta.dirname, "..", "dist");
const indexHtml = resolve(distDir, "index.html");
const notFoundHtml = resolve(distDir, "404.html");

if (existsSync(indexHtml)) {
  copyFileSync(indexHtml, notFoundHtml);
  console.log("postbuild: copied index.html -> 404.html for SPA routing");
} else {
  console.warn("postbuild: dist/index.html not found, skipping 404.html copy");
}
