/* Supabase connection — PUBLIC anon key.
   Safe to ship: every table has RLS on, anon can only read published rows,
   and all writes go through admin_* RPCs that verify the PIN inside Postgres.
   Regenerate with: python3 tools/make_config.py                                */
window.SUPABASE_URL = "https://djtfapdhknwxpfmdegax.supabase.co";
window.SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGZhcGRoa253eHBmbWRlZ2F4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyODQxMTMsImV4cCI6MjEwMjg2MDExM30.9nQITYy8grNzqu2YdaCuC6e0p0FI0vGV1qElCue9q3c";
