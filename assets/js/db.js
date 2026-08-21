/* ============================================================
   Tiny Supabase REST client (no SDK, no CDN — just fetch).
   Requires supabase-config.js to be loaded first.
   ============================================================ */
(function () {
  "use strict";

  var URL_ = window.SUPABASE_URL || "";
  var KEY = window.SUPABASE_ANON_KEY || "";

  function headers(extra) {
    var h = {
      apikey: KEY,
      Authorization: "Bearer " + KEY,
      "Content-Type": "application/json"
    };
    for (var k in extra) h[k] = extra[k];
    return h;
  }

  async function request(path, options) {
    var res = await fetch(URL_ + path, options);
    var text = await res.text();
    var body = null;
    if (text) { try { body = JSON.parse(text); } catch (e) { body = text; } }
    if (!res.ok) {
      var msg = (body && (body.message || body.hint || body.error)) || ("HTTP " + res.status);
      var err = new Error(msg);
      err.status = res.status;
      err.body = body;
      throw err;
    }
    return body;
  }

  window.DB = {
    /** true when a Supabase project is configured */
    ready: !!(URL_ && KEY),

    /** public read of a table, e.g. DB.select("site_lessons", "order=sort.asc") */
    select: function (table, query) {
      return request("/rest/v1/" + table + "?" + (query || "select=*"), {
        headers: headers()
      });
    },

    /** call a Postgres function, e.g. DB.rpc("admin_list", {p_pin: pin, p_table: t}) */
    rpc: function (fn, args) {
      return request("/rest/v1/rpc/" + fn, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(args || {})
      });
    },

    /* ---------------- video storage ---------------- */

    BUCKET: "lesson-videos",
    MAX_UPLOAD: 50 * 1024 * 1024,          // Supabase free plan caps a file at 50 MB

    /** public playback URL for an object inside the video bucket */
    publicUrl: function (path) {
      return URL_ + "/storage/v1/object/public/" + this.BUCKET + "/" + path;
    },

    /** object path if this URL points into our own bucket, otherwise null */
    pathFromUrl: function (url) {
      if (!url) return null;
      var marker = "/storage/v1/object/public/" + this.BUCKET + "/";
      var at = url.indexOf(marker);
      return at === -1 ? null : decodeURIComponent(url.slice(at + marker.length));
    },

    /** true for a file we can play inline (rather than a YouTube/Vimeo page) */
    isPlayable: function (url) {
      return !!url && /\.(mp4|webm|mov|m4v)(\?.*)?$/i.test(url);
    },

    /** upload a video file — the PIN is checked by Postgres, not by this code */
    uploadVideo: function (file, pin, onProgress) {
      var self = this;
      // Supabase Storage keys must be ASCII — Thai filenames are transliterated away
      var clean = (file.name || "video")
        .replace(/\.[^.]+$/, "")
        .replace(/[^a-zA-Z0-9_-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .slice(0, 48) || "video";
      var ext = (file.name.match(/\.[^.]+$/) || [".mp4"])[0].toLowerCase();
      var path = clean + "-" + Math.random().toString(36).slice(2, 8) + ext;

      return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", URL_ + "/storage/v1/object/" + self.BUCKET + "/" + encodeURIComponent(path));
        xhr.setRequestHeader("apikey", KEY);
        xhr.setRequestHeader("Authorization", "Bearer " + KEY);
        xhr.setRequestHeader("x-admin-pin", pin);
        xhr.setRequestHeader("Content-Type", file.type || "video/mp4");
        xhr.upload.onprogress = function (e) {
          if (onProgress && e.lengthComputable) onProgress(e.loaded / e.total);
        };
        xhr.onload = function () {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve({ path: path, url: self.publicUrl(encodeURIComponent(path)) });
          } else {
            var m = "อัปโหลดไม่สำเร็จ (" + xhr.status + ")";
            try { m = JSON.parse(xhr.responseText).message || m; } catch (e) {}
            reject(new Error(m));
          }
        };
        xhr.onerror = function () { reject(new Error("เชื่อมต่อไม่ได้ระหว่างอัปโหลด")); };
        xhr.send(file);
      });
    },

    /** remove an uploaded video (PIN enforced by storage RLS) */
    deleteVideo: function (path, pin) {
      // no Content-Type here: the storage API rejects a JSON content-type with an empty body
      return request("/storage/v1/object/" + this.BUCKET + "/" + encodeURIComponent(path), {
        method: "DELETE",
        headers: { apikey: KEY, Authorization: "Bearer " + KEY, "x-admin-pin": pin }
      });
    }
  };
})();
