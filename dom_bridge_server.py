from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, shutil, time, threading
from pathlib import Path

class FileManager:
    def make_dir(self, p):
        Path(os.path.expanduser(p)).mkdir(parents=True, exist_ok=True)
        print(f"[POGI] CREATED {p}")
        return True
    def move_dir(self, src, dst):
        s = Path(os.path.expanduser(src))
        d = Path(os.path.expanduser(dst))
        if not s.exists():
            print(f"[POGI] SKIP {s} not exists")
            return False
        d.parent.mkdir(parents=True, exist_ok=True)
        if d.exists(): shutil.rmtree(str(d), ignore_errors=True)
        shutil.move(str(s), str(d))
        print(f"[POGI] RENAMED {s} -> {d} OK")
        return True

fm = FileManager()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): return
    def do_POST(self):
        if self.path == "/execute":
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))).decode())
            print(f"[POGI] {data}")
            if data.get("action")=="rename":
                src, dst = data.get("src","citvsablay"), data.get("dst","weroa")
                for sp, dp in [(f"~/storage/shared/{src}", f"~/storage/shared/{dst}"), (f"/storage/emulated/0/{src}", f"/storage/emulated/0/{dst}"), (f"~/storage/shared/Download/{src}", f"~/storage/shared/Download/{dst}")]:
                    fm.move_dir(sp, dp)
                self.send_response(200)
                self.send_header("Content-type","application/json")
                self.send_header("Access-Control-Allow-Origin","*")
                self.end_headers()
                self.wfile.write(json.dumps({"status":"SUCCESS","src":src,"dst":dst}).encode())
            else:
                folder=data.get("folder","weroa")
                for p in [f"~/storage/shared/{folder}", f"/storage/emulated/0/{folder}"]: fm.make_dir(p)
                self.send_response(200)
                self.send_header("Content-type","application/json")
                self.send_header("Access-Control-Allow-Origin","*")
                self.end_headers()
                self.wfile.write(json.dumps({"status":"SUCCESS"}).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(b"V4 RENAME FIXED")

def watcher():
    while True:
        for p in [Path.home()/"termux-memory-public"/"autotask.json", Path.home()/"metaaitermuxbridge"/"autotask.json"]:
            if p.exists():
                try:
                    d=json.loads(p.read_text())
                    if not d.get("executed"):
                        print(f"[WATCHER] {d.get('explanation')}")
                        for c in d.get("commands",[]):
                            if c.get("action")=="make_dir": fm.make_dir(c.get("path"))
                            elif c.get("action") in ["move_dir","rename_file"]: fm.move_dir(c.get("src"),c.get("dst"))
                        d["executed"]=True
                        p.write_text(json.dumps(d,indent=2))
                        print("[WATCHER] DONE NO CURL!")
                except: pass
        time.sleep(2)

print("V4 RENAME FIXED - NO CURL NEEDED!")
threading.Thread(target=watcher,daemon=True).start()
HTTPServer(("127.0.0.1",8080),Handler).serve_forever()
