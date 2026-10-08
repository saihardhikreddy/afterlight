// Screenshot every demo at desktop and phone size, and fail on console errors,
// page errors or failed requests. Usage: node scripts/verify.mjs [demo-dir ...]
import { createRequire } from "node:module";
import { createServer } from "node:http";
import { readFile, readdir, mkdir } from "node:fs/promises";
import { extname, join, resolve, relative } from "node:path";

// createRequire so a global/NODE_PATH install works as well as a local one.
const { chromium } = createRequire(import.meta.url)("playwright");
const root = resolve(new URL("..", import.meta.url).pathname);
const outDir = join(root, ".verify");
const types = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css",
  ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml",
  ".woff2": "font/woff2", ".glb": "model/gltf-binary", ".mp4": "video/mp4" };

async function findDemos(dir) {
  const found = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") || e.name === "node_modules") continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) found.push(...await findDemos(p));
    else if (e.name === "index.html" && dir.endsWith("demo")) found.push(dir);
  }
  return found;
}

const server = createServer(async (req, res) => {
  let path = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (path.endsWith("/")) path += "index.html";
  const file = join(root, path);
  if (!file.startsWith(root)) { res.writeHead(403).end(); return; }
  try { res.writeHead(200, { "content-type": types[extname(file)] || "application/octet-stream" }).end(await readFile(file)); }
  catch { res.writeHead(404).end(); }
}).listen(0, "127.0.0.1");
await new Promise(r => server.once("listening", r));
const base = `http://127.0.0.1:${server.address().port}`;

const demos = process.argv.length > 2 ? process.argv.slice(2).map(d => resolve(d)) : await findDemos(join(root, "skills"));
const viewports = [{ name: "desktop", width: 1280, height: 720 }, { name: "phone", width: 390, height: 844 }];
const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
await mkdir(outDir, { recursive: true });
let failed = 0;

for (const demo of demos) {
  const rel = relative(root, demo);
  for (const vp of viewports) {
    const page = await browser.newPage({ viewport: vp });
    const problems = [];
    page.on("console", m => { if (m.type() === "error") problems.push(`console: ${m.text()}`); });
    page.on("pageerror", e => problems.push(`pageerror: ${e.message}`));
    page.on("response", r => { if (r.status() >= 400) problems.push(`${r.status()} ${r.url()}`); });
    await page.goto(`${base}/${rel}/`, { waitUntil: "load" });
    await page.waitForTimeout(Number(process.env.SETTLE_MS || 3500));
    const shot = join(outDir, `${rel.replaceAll("/", "__")}--${vp.name}.png`);
    await page.screenshot({ path: shot });
    const status = problems.length ? "FAIL" : "ok";
    if (problems.length) failed++;
    console.log(`${status.padEnd(4)} ${rel} @ ${vp.name} -> ${relative(root, shot)}`);
    for (const p of problems) console.log(`     ${p}`);
    await page.close();
  }
}
await browser.close();
server.close();
process.exit(failed ? 1 : 0);
