from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, shutil, time, threading
from pathlib import Path

class FM:
    def make_dir(self, p):
        Path(os.path.expanduser(p)).mkdir(parents=True, exist_ok=True)
        print(f"[POGI] CREATED {p}")
    def move_dir(self, s, d):
        sp, dp = Path(os.path.expanduser(s)), Path(os.path.expanduser(d))
        if not sp.exists(): print(f"[SKIP] {sp}"); return
        dp.parent.mkdir(parents=True, exist_ok=True)
        if dp.exists(): shutil.rmtree(str(dp), ignore_errors=True)
        shutil.move(str(sp), str(dp))
        print(f"[POGI] RENAMED {sp} -> {dp} OK")

fm = FM()

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): return
    def do_POST(self):
        if self.path=="/execute":
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))).decode())
            print(f"[HTTP] {data}")
            if data.get("action")=="rename":
                for a,b in [(f"~/storage/shared/{data.get('src')}", f"~/storage/shared/{data.get('dst')}"), (f"/storage/emulated/0/{data.get('src')}", f"/storage/emulated/0/{data.get('dst')}")]: fm.move_dir(a,b)
            else:
                f=data.get("folder","weroa")
                for p in [f"~/storage/shared/{f}", f"/storage/emulated/0/{f}", f"~/storage/shared/Download/{f}"]: fm.make_dir(p)
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(b'{"status":"SUCCESS"}')
    def do_OPTIONS(self):
        self.send_response(200); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Methods","POST, GET, OPTIONS"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.end_headers()
    def do_GET(self):
        self.send_response(200); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers(); self.wfile.write(b"V4 OK")

def watcher():
    print("[WATCHER] Watching autotask.json - NO EXTENSION NEEDED!")
    while True:
        for p in [Path.home()/"termux-memory-public"/"autotask.json"]:
            if p.exists():
                try:
                    d=json.loads(p.read_text())
                    if not d.get("executed"):
                        print(f"[WATCHER] TASK: {d.get('explanation')}")
                        for c in d.get("commands",[]):
                            if c.get("action")=="make_dir": fm.make_dir(c.get("path"))
                            elif c.get("action") in ["move_dir","rename_file"]: fm.move_dir(c.get("src"),c.get("dst"))
                        d["executed"]=True
                        p.write_text(json.dumps(d,indent=2))
                        print("[WATCHER] DONE!")
                except Exception as e: print(e)
        time.sleep(2)

print("POGI BOSS V4 - CHROME ANDROID READY!")
print("HTTP: http://localhost:8080")
print("WATCHER: autotask.json")
import threading
threading.Thread(target=watcher,daemon=True).start()
HTTPServer(("127.0.0.1",8080),H).serve_forever()
