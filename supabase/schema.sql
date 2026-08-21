-- =============================================================
--  ครูเลี้ยง Drum Academy — Supabase schema
--  วิธีใช้: เปิด Supabase Dashboard → SQL Editor → วางไฟล์นี้ทั้งไฟล์ → Run
--  รันซ้ำได้ ไม่พัง (idempotent)
--
--  หลักความปลอดภัย
--   • ทุกตารางเปิด RLS
--   • anon key (ที่ฝังอยู่ในหน้าเว็บ) อ่านได้เฉพาะแถวที่ published = true
--   • anon เขียน/ลบตรง ๆ ไม่ได้เลย — ต้องผ่านฟังก์ชัน admin_* ที่ตรวจ PIN ใน Postgres
--   • PIN ไม่เคยถูกฝังในโค้ดหน้าเว็บ เก็บเป็น sha256 hash ในตาราง admin_config
-- =============================================================

-- ใช้ sha256() ที่มีมากับ Postgres อยู่แล้ว ไม่ต้องพึ่ง extension เพิ่ม

-- ---------- 1. ตารางเนื้อหา ----------

create table if not exists public.site_lessons (
  id          uuid primary key default gen_random_uuid(),
  sort        int  not null default 0,
  level       text not null default 'beginner',   -- beginner | intermediate | advanced
  category    text not null default 'groove',     -- groove | technique | reading
  duration    text default '',
  title_en    text default '',
  title_th    text default '',
  desc_en     text default '',
  desc_th     text default '',
  video_url   text default '',
  published   boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.site_packages (
  id          uuid primary key default gen_random_uuid(),
  sort        int  not null default 0,
  name        text default '',                    -- เช่น "10 Lessons"
  sub_en      text default '',
  sub_th      text default '',
  price       text default '',                    -- เช่น "9,000฿"
  price_was   text default '',                    -- ราคาก่อนลด เว้นว่างได้
  save_en     text default '',
  save_th     text default '',
  is_best     boolean not null default false,     -- ติดป้าย "คุ้มสุด"
  published   boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.site_faq (
  id          uuid primary key default gen_random_uuid(),
  sort        int  not null default 0,
  q_en        text default '',
  q_th        text default '',
  a_en        text default '',
  a_th        text default '',
  published   boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.site_testimonials (
  id          uuid primary key default gen_random_uuid(),
  sort        int  not null default 0,
  person      text default '',
  role_en     text default '',
  role_th     text default '',
  quote_en    text default '',
  quote_th    text default '',
  published   boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.site_timeline (
  id          uuid primary key default gen_random_uuid(),
  sort        int  not null default 0,
  year        text default '',
  title_en    text default '',
  title_th    text default '',
  desc_en     text default '',
  desc_th     text default '',
  published   boolean not null default true,
  created_at  timestamptz not null default now()
);

-- ข้อความเดี่ยว ๆ ที่ไม่ได้เป็นรายการ (hero, ข้อมูลติดต่อ ฯลฯ)
create table if not exists public.site_settings (
  key         text primary key,
  label       text default '',                    -- ชื่อที่โชว์ในหลังบ้าน
  value_en    text default '',
  value_th    text default '',
  updated_at  timestamptz not null default now()
);

-- ---------- 2. ตารางระบบหลังบ้าน (anon แตะไม่ได้เลย) ----------

create table if not exists public.admin_config (
  id       int primary key default 1,
  pin_hash text not null,
  constraint admin_config_single_row check (id = 1)
);

create table if not exists public.admin_attempts (
  id  bigserial primary key,
  ok  boolean not null,
  at  timestamptz not null default now()
);

-- ตั้ง PIN เริ่มต้น = 646644  (เปลี่ยนได้จากหน้าหลังบ้าน หรือรัน admin_set_pin)
insert into public.admin_config (id, pin_hash)
values (1, encode(sha256('646644'::bytea), 'hex'))
on conflict (id) do nothing;

-- ---------- 3. RLS ----------

alter table public.site_lessons      enable row level security;
alter table public.site_packages     enable row level security;
alter table public.site_faq          enable row level security;
alter table public.site_testimonials enable row level security;
alter table public.site_timeline     enable row level security;
alter table public.site_settings     enable row level security;
alter table public.admin_config      enable row level security;
alter table public.admin_attempts    enable row level security;

-- อ่านได้เฉพาะแถวที่เผยแพร่แล้ว / ไม่มี policy insert-update-delete = เขียนตรงไม่ได้
do $$
declare t text;
begin
  foreach t in array array['site_lessons','site_packages','site_faq',
                           'site_testimonials','site_timeline']
  loop
    execute format('drop policy if exists "read published" on public.%I', t);
    execute format($f$create policy "read published" on public.%I
                     for select to anon, authenticated using (published)$f$, t);
  end loop;
end$$;

drop policy if exists "read settings" on public.site_settings;
create policy "read settings" on public.site_settings
  for select to anon, authenticated using (true);

-- admin_config / admin_attempts: เปิด RLS แต่ไม่มี policy เลย → anon อ่านไม่ได้ เขียนไม่ได้

-- ---------- 4. ฟังก์ชันหลังบ้าน ----------

-- ตรวจ PIN แบบเงียบ (ใช้ภายใน ไม่นับ attempt)
create or replace function public.admin_pin_ok(p_pin text)
returns boolean
language sql
security definer
set search_path = public
as $$
  select coalesce(
    (select pin_hash = encode(sha256(coalesce(p_pin, '')::bytea), 'hex')
       from public.admin_config where id = 1), false);
$$;

-- ตรวจ PIN ตอนล็อกอิน + กันเดารหัส (ผิดเกิน 10 ครั้งใน 15 นาที = ล็อก)
create or replace function public.admin_check_pin(p_pin text)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  v_fails int;
  v_ok    boolean;
begin
  select count(*) into v_fails
    from public.admin_attempts
   where ok = false and at > now() - interval '15 minutes';

  if v_fails >= 10 then
    raise exception 'LOCKED: ใส่รหัสผิดหลายครั้งเกินไป รอ 15 นาทีแล้วลองใหม่';
  end if;

  v_ok := public.admin_pin_ok(p_pin);
  insert into public.admin_attempts (ok) values (v_ok);
  return v_ok;
end;
$$;

-- ตารางที่หลังบ้านแก้ไขได้ (whitelist กันสั่งแก้ตารางอื่น)
create or replace function public.admin_allowed_table(p_table text)
returns boolean
language sql
immutable
as $$
  select p_table in ('site_lessons','site_packages','site_faq',
                     'site_testimonials','site_timeline');
$$;

-- อ่านทุกแถว รวมที่ยังไม่เผยแพร่ (สำหรับหลังบ้าน)
create or replace function public.admin_list(p_pin text, p_table text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_rows jsonb;
begin
  if not public.admin_pin_ok(p_pin) then raise exception 'FORBIDDEN'; end if;
  if not public.admin_allowed_table(p_table) then raise exception 'BAD_TABLE'; end if;

  execute format(
    'select coalesce(jsonb_agg(to_jsonb(t) order by t.sort, t.created_at), ''[]''::jsonb)
       from public.%I t', p_table)
  into v_rows;

  return v_rows;
end;
$$;

-- เพิ่ม/แก้ไขแถว — ส่งเฉพาะคอลัมน์ที่ต้องการแก้มาใน p_row ได้
create or replace function public.admin_save(p_pin text, p_table text, p_row jsonb)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_cols   text;
  v_sets   text;
  v_result jsonb;
begin
  if not public.admin_pin_ok(p_pin) then raise exception 'FORBIDDEN'; end if;
  if not public.admin_allowed_table(p_table) then raise exception 'BAD_TABLE'; end if;

  if p_row ? 'id' and nullif(p_row->>'id', '') is null then
    p_row := p_row - 'id';                         -- แถวใหม่: ปล่อยให้ default สร้าง uuid
  end if;

  select string_agg(quote_ident(c.column_name), ', '),
         string_agg(format('%I = excluded.%I', c.column_name, c.column_name), ', ')
           filter (where c.column_name <> 'id')
    into v_cols, v_sets
    from information_schema.columns c
   where c.table_schema = 'public'
     and c.table_name   = p_table
     and c.column_name  in (select jsonb_object_keys(p_row));

  if v_cols is null then raise exception 'NO_FIELDS'; end if;

  execute format(
    'insert into public.%I (%s) select %s from jsonb_populate_record(null::public.%I, $1)
       on conflict (id) do update set %s
       returning to_jsonb(public.%I.*)',
    p_table, v_cols, v_cols, p_table,
    coalesce(v_sets, 'sort = public.' || quote_ident(p_table) || '.sort'), p_table)
  using p_row
  into v_result;

  return v_result;
end;
$$;

-- ลบแถว
create or replace function public.admin_delete(p_pin text, p_table text, p_id uuid)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
begin
  if not public.admin_pin_ok(p_pin) then raise exception 'FORBIDDEN'; end if;
  if not public.admin_allowed_table(p_table) then raise exception 'BAD_TABLE'; end if;

  execute format('delete from public.%I where id = $1', p_table) using p_id;
  return true;
end;
$$;

-- แก้ข้อความเดี่ยว (site_settings)
create or replace function public.admin_save_setting(
  p_pin text, p_key text, p_label text, p_en text, p_th text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare v_row jsonb;
begin
  if not public.admin_pin_ok(p_pin) then raise exception 'FORBIDDEN'; end if;

  insert into public.site_settings (key, label, value_en, value_th, updated_at)
  values (p_key, coalesce(p_label, ''), coalesce(p_en, ''), coalesce(p_th, ''), now())
  on conflict (key) do update
    set label      = excluded.label,
        value_en   = excluded.value_en,
        value_th   = excluded.value_th,
        updated_at = now()
  returning to_jsonb(site_settings.*) into v_row;

  return v_row;
end;
$$;

-- เปลี่ยน PIN (ต้องรู้ PIN เดิม)
create or replace function public.admin_set_pin(p_pin text, p_new_pin text)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
begin
  if not public.admin_pin_ok(p_pin) then raise exception 'FORBIDDEN'; end if;
  if p_new_pin !~ '^[0-9]{6}$' then raise exception 'PIN ต้องเป็นตัวเลข 6 หลัก'; end if;

  update public.admin_config
     set pin_hash = encode(sha256(p_new_pin::bytea), 'hex')
   where id = 1;
  return true;
end;
$$;

-- ให้เว็บเรียกฟังก์ชันเหล่านี้ได้ (ตัวฟังก์ชันเช็ค PIN เองอยู่แล้ว)
grant execute on function public.admin_check_pin(text)                        to anon, authenticated;
grant execute on function public.admin_list(text, text)                       to anon, authenticated;
grant execute on function public.admin_save(text, text, jsonb)                to anon, authenticated;
grant execute on function public.admin_delete(text, text, uuid)               to anon, authenticated;
grant execute on function public.admin_save_setting(text,text,text,text,text) to anon, authenticated;
grant execute on function public.admin_set_pin(text, text)                    to anon, authenticated;
revoke execute on function public.admin_pin_ok(text)          from anon, authenticated;
revoke execute on function public.admin_allowed_table(text)   from anon, authenticated;
