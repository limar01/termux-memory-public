from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os
from pathlib import Path

class FileManager:
    def make_dir(self, path):
        p = Path(os.path.expanduser(path))
        p.mkdir(parents=True, exist_ok=True)
        print(f"[POGI] CREATED {p} - OK")
        return True
fm = FileManager()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>POGI BOSS Bridge Running! Type create folder citvsablay in Meta AI</h1>")
    def do_POST(self):
        if self.path == "/execute":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            try:
                data = json.loads(body)
                folder = data.get("folder", "citvsablay")
                print(f"[POGI] COMMAND RECEIVED: {data}")
                for p in [f"~/storage/shared/{folder}", f"/storage/emulated/0/{folder}", f"~/storage/shared/Download/{folder}"]:
                    fm.make_dir(p)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "folder": folder}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

print("[POGI BOSS] Listening on http://localhost:8080")
print("[POGI BOSS] Waiting for commands...")
server = HTTPServer(("127.0.0.1", 8080), Handler)
server.serve_forever()
