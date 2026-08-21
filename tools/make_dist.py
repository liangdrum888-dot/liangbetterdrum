# -*- coding: utf-8 -*-
"""สร้างโฟลเดอร์ dist/ ที่มีเฉพาะไฟล์ที่ต้องขึ้นเว็บจริง

ไม่เอาขึ้น: tools/ (มี path ของไฟล์ key), supabase/ (SQL ภายใน),
README.md, vercel.json และไฟล์ note ต่าง ๆ

    python3 tools/make_dist.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

PAGES = ["index.html", "profile.html", "lesson.html", "contact.html",
         "login.html", "admin.html", "404.html", "_redirects"]
ASSET_DIRS = ["assets/css", "assets/js"]
ASSET_FILES = ["assets/img/hero-kit.jpg"]
SKIP_SUFFIX = (".txt", ".md")

if os.path.isdir(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)

shipped = []

for name in PAGES:
    src = os.path.join(ROOT, name)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(DIST, name))
        shipped.append(name)

for d in ASSET_DIRS:
    dst_dir = os.path.join(DIST, d)
    os.makedirs(dst_dir, exist_ok=True)
    for f in sorted(os.listdir(os.path.join(ROOT, d))):
        if f.startswith(".") or f.endswith(SKIP_SUFFIX):
            continue
        shutil.copy2(os.path.join(ROOT, d, f), os.path.join(dst_dir, f))
        shipped.append(os.path.join(d, f))

for f in ASSET_FILES:
    src = os.path.join(ROOT, f)
    if os.path.exists(src):
        dst = os.path.join(DIST, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        shipped.append(f)

total = sum(os.path.getsize(os.path.join(dp, f))
            for dp, _, fs in os.walk(DIST) for f in fs)

print("dist/ พร้อมแล้ว — %d ไฟล์ รวม %.1f KB\n" % (len(shipped), total / 1024))
for f in shipped:
    print("  ", f)
