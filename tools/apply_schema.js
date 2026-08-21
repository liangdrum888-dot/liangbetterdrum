/* Applies supabase/schema.sql (and optionally seed.sql) to the Postgres database
   whose connection string lives in the local credentials file.

   Needs the pg driver:   npm install pg
   Run:                   node tools/apply_schema.js          (schema only)
                          node tools/apply_schema.js --seed   (schema + starting content)

   The connection string is read straight from the credentials file and is never
   printed or copied anywhere else.                                              */
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { Client } = require("pg");

const SECRETS = "/Users/apple/Desktop/Claude2026/Secret token.rtf";
const ROOT = path.join(__dirname, "..");

function credentials() {
  const raw = execFileSync("textutil", ["-convert", "txt", "-stdout", SECRETS], { encoding: "utf8" });
  const m = raw.match(/postgresql:\/\/\S+/);
  if (!m) throw new Error("no postgresql:// connection string found in the credentials file");
  const url = new URL(m[0].trim());
  const ref = (m[0].match(/db\.([a-z0-9]+)\.supabase\.co/) || [])[1];
  return { password: decodeURIComponent(url.password), ref, direct: m[0].trim() };
}

/* Supabase no longer resolves db.<ref>.supabase.co over IPv4 for new projects,
   so fall back to the Supavisor pooler (session mode, port 5432 — DDL works). */
async function connect() {
  const { password, ref, direct } = credentials();
  const attempts = [{ connectionString: direct, ssl: { rejectUnauthorized: false } }];
  for (const region of ["ap-southeast-1", "us-east-1", "eu-central-1", "ap-northeast-1", "us-west-1", "ap-southeast-2"]) {
    for (const prefix of ["aws-0", "aws-1"]) {
      attempts.push({
        host: `${prefix}-${region}.pooler.supabase.com`, port: 5432,
        user: `postgres.${ref}`, password, database: "postgres",
        ssl: { rejectUnauthorized: false }, connectionTimeoutMillis: 8000
      });
    }
  }
  let lastError;
  for (const cfg of attempts) {
    const client = new Client(cfg);
    try {
      await client.connect();
      console.log("connected via", cfg.host || "direct connection");
      return client;
    } catch (e) {
      lastError = e;
      try { await client.end(); } catch (_) {}
    }
  }
  throw lastError;
}

(async () => {
  const client = await connect();

  const files = ["supabase/schema.sql", "supabase/storage.sql"];
  if (process.argv.includes("--seed")) files.push("supabase/seed.sql");

  for (const f of files) {
    const sql = fs.readFileSync(path.join(ROOT, f), "utf8");
    await client.query(sql);
    console.log("applied", f);
  }

  const { rows } = await client.query(`
    select table_name, (xpath('/row/c/text()',
      query_to_xml(format('select count(*) c from public.%I', table_name), false, true, '')))[1]::text::int as rows
    from information_schema.tables
    where table_schema = 'public' and table_name like 'site\\_%'
    order by table_name`);
  console.table(rows);

  await client.end();
  console.log("done");
})().catch((e) => {
  console.error("FAILED:", e.message);
  process.exit(1);
});
