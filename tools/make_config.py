# -*- coding: utf-8 -*-
"""Generates assets/js/supabase-config.js from the local credentials file.

Only the *anon* (public) key is written into the site — that key is designed to be
exposed in a browser and is safe ONLY because Row Level Security is enabled on every
table (see supabase/schema.sql). The service_role key and the Postgres connection
string are never written anywhere inside drumsite/.
"""
import base64
import json
import os
import re
import subprocess
import sys

SECRETS = "/Users/apple/Desktop/Claude2026/Secret token.rtf"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "js", "supabase-config.js")

raw = subprocess.run(["textutil", "-convert", "txt", "-stdout", SECRETS],
                     capture_output=True, text=True).stdout

def jwt_role(token):
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(payload)).get("role")
    except Exception:
        return None

tokens = re.findall(r"ey[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", raw)
by_role = {jwt_role(t): t for t in tokens}
anon = by_role.get("anon")

ref = re.search(r"db\.([a-z0-9]+)\.supabase\.co", raw)
if not anon or not ref:
    sys.exit("could not find an anon key / project ref in the credentials file")

with open(OUT, "w") as f:
    f.write(
        "/* Supabase connection — PUBLIC anon key.\n"
        "   Safe to ship: every table has RLS on, anon can only read published rows,\n"
        "   and all writes go through admin_* RPCs that verify the PIN inside Postgres.\n"
        "   Regenerate with: python3 tools/make_config.py                                */\n"
        "window.SUPABASE_URL = %s;\n"
        "window.SUPABASE_ANON_KEY = %s;\n" % (json.dumps("https://%s.supabase.co" % ref.group(1)),
                                              json.dumps(anon))
    )

print("wrote", OUT)
print("project ref:", ref.group(1))
print("roles present in credentials file:", sorted(r for r in by_role if r))
print("service_role key was NOT written into the site")
