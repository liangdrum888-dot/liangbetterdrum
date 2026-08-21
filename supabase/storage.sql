-- =============================================================
--  Storage สำหรับวิดีโอบทเรียน
--  รันหลัง schema.sql — รันซ้ำได้
--
--  การอัปโหลด/ลบ ต้องส่ง header  x-admin-pin  ที่ตรงกับ PIN ในตาราง admin_config
--  (ทดสอบแล้ว: ไม่ส่ง PIN หรือส่งผิด → RLS ปฏิเสธที่ฝั่งเซิร์ฟเวอร์)
-- =============================================================

-- ---------- bucket ----------
-- public = true เพื่อให้เล่นวิดีโอบนหน้าเว็บได้โดยไม่ต้องเซ็น URL
-- file_size_limit 50 MB = เพดานของ Supabase แผนฟรี
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('lesson-videos', 'lesson-videos', true, 52428800,
        array['video/mp4','video/webm','video/quicktime','video/x-m4v'])
on conflict (id) do update
  set public             = true,
      file_size_limit    = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

-- ---------- อ่าน: ใครก็ดูได้ (ต้องเล่นวิดีโอบนเว็บ) ----------
drop policy if exists "lesson videos are public" on storage.objects;
create policy "lesson videos are public" on storage.objects
  for select to anon, authenticated
  using (bucket_id = 'lesson-videos');

-- ---------- ตัวช่วย: อ่าน PIN จาก header ของ request ----------
create or replace function public.admin_header_pin_ok()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select public.admin_pin_ok(
    nullif(current_setting('request.headers', true), '')::json ->> 'x-admin-pin');
$$;

revoke execute on function public.admin_header_pin_ok() from anon, authenticated;

-- ---------- เขียน / แก้ / ลบ: ต้องมี PIN ที่ถูกต้อง ----------
-- เพดานจำนวนไฟล์กัน storage บวมถ้า PIN หลุด
drop policy if exists "upload with pin" on storage.objects;
create policy "upload with pin" on storage.objects
  for insert to anon, authenticated
  with check (
    bucket_id = 'lesson-videos'
    and public.admin_header_pin_ok()
    and (select count(*) from storage.objects o where o.bucket_id = 'lesson-videos') < 300
  );

drop policy if exists "replace with pin" on storage.objects;
create policy "replace with pin" on storage.objects
  for update to anon, authenticated
  using (bucket_id = 'lesson-videos' and public.admin_header_pin_ok())
  with check (bucket_id = 'lesson-videos' and public.admin_header_pin_ok());

drop policy if exists "delete with pin" on storage.objects;
create policy "delete with pin" on storage.objects
  for delete to anon, authenticated
  using (bucket_id = 'lesson-videos' and public.admin_header_pin_ok());
