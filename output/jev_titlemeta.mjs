// Run jev title + meta checks over top30_pages.json through the kev-jev-seo MCP server.
import fs from "node:fs"; import os from "node:os";
const TOOL = "C:/Users/tvural.REPKON/tools/kev-jev-seo";
const SDK = "file:///" + TOOL + "/node_modules/@modelcontextprotocol/sdk/dist/esm/client/";
const { Client } = await import(SDK + "index.js"); const { StdioClientTransport } = await import(SDK + "stdio.js");
const cfg = JSON.parse(fs.readFileSync(os.homedir() + "/.claude.json", "utf8")).mcpServers["kev-jev-seo"];
const transport = new StdioClientTransport({ command: "node", args: cfg.args, env: { ...process.env, ...cfg.env } });
const client = new Client({ name: "ub-audit", version: "1" }); await client.connect(transport);
const call = async (name, args) => { const r = await client.callTool({ name, arguments: args }); const t = r.content.map((c) => c.text).join(""); try { return JSON.parse(t); } catch { return { raw: t, err: !!r.isError }; } };
const pages = JSON.parse(fs.readFileSync(process.argv[2] || "top30_pages.json", "utf8"));
const out = [];
await Promise.all(pages.map(async (p, i) => {
  const kw = p.queries?.[0]?.[0];
  const content = `${p.h1}\n${p.content}`;
  const [title, meta] = await Promise.all([
    call("jev_seo_title_check", { title: p.title, h1: p.h1, content, ...(kw && { focus_keyword: kw }) }),
    call("jev_seo_meta_check", { title: p.title, content, meta_description: p.meta, ...(kw && { focus_keyword: kw }) }),
  ]);
  out[i] = { page: p.page, impressions: p.impressions, ctr: p.ctr, position: p.position, title: p.title, meta: p.meta, title_check: title, meta_check: meta };
}));
fs.writeFileSync(process.argv[3] || "jev_results.json", JSON.stringify(out, null, 1));
await client.close();
console.log("done", out.length);
