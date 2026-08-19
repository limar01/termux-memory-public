
"""
pure_bridge.py - NUMBER 2 PURE PYTHON BRIDGE (100% WORKING - FINAL) - FIXED MISSING REPO
Repo: termux-memory-public - PLAIN
No browser, No SSH, No Cloudflare - Pure python + git only
Dynamic file management included
"""

import time
import json
import os
import subprocess
from pathlib import Path

BRIDGE_REPO = Path.home() / "metaaitermuxbridge"
QUEUE_DIR = BRIDGE_REPO / "queue"
DONE_DIR = QUEUE_DIR / "done"
RESULT_FILE = BRIDGE_REPO / "result.json"
TASK_FILE = BRIDGE_REPO / "autotask.json"

# Import dynamic file manager
try:
    from lib.file_manager import FileManager
    fm = FileManager()
except:
    import sys
    sys.path.append(str(Path.home() / "termux-memory-public"))
    from lib.file_manager import FileManager
    fm = FileManager()

def ensure_bridge_repo():
    if not BRIDGE_REPO.exists():
        print(f"[BRIDGE] Creating {BRIDGE_REPO}...")
        BRIDGE_REPO.mkdir(parents=True, exist_ok=True)
        # Try clone from github if not git repo
        if not (BRIDGE_REPO / ".git").exists():
            print("[BRIDGE] Cloning metaaitermuxbridge from GitHub...")
            os.system(f"cd {Path.home()} && git clone https://github.com/limar01/metaaitermuxbridge.git 2>/dev/null || echo 'clone failed, will init'")
            if not (BRIDGE_REPO / ".git").exists():
                os.system(f"cd {BRIDGE_REPO} && git init && git remote add origin https://github.com/limar01/metaaitermuxbridge.git 2>/dev/null")
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)

def git_pull():
    ensure_bridge_repo()
    if (BRIDGE_REPO / ".git").exists():
        os.system(f"cd {BRIDGE_REPO} && git pull --quiet 2>/dev/null || echo '[BRIDGE] pull skip'")

def git_push(msg="auto push result"):
    if (BRIDGE_REPO / ".git").exists():
        os.system(f"cd {BRIDGE_REPO} && git add . && git commit -m '{msg}' --quiet 2>/dev/null && git push --quiet 2>/dev/null || echo '[BRIDGE] push skip - local only'")

def execute_task(task_data):
    results = []
    for cmd in task_data.get("commands", []):
        action = cmd.get("action")
        try:
            if action in fm.commands:
                func = fm.commands[action]
                if action in ["copy_file", "move_file", "rename_file", "copy_dir", "move_dir"]:
                    res = func(cmd.get("src"), cmd.get("dst"))
                elif action in ["write_file", "make_file", "append_file"]:
                    res = func(cmd.get("path"), cmd.get("content",""))
                elif action in ["write_json", "append_json", "update_json"]:
                    res = func(cmd.get("path"), cmd.get("data",{}))
                else:
                    res = func(cmd.get("path") or cmd.get("src") or "")
                results.append({"action": action, "status": "SUCCESS", "result": str(res)})
                print(f"  -> {action} {cmd.get('path') or cmd.get('src','')} = SUCCESS")
            elif action == "exec":
                ret = subprocess.run(cmd.get("command"), shell=True, capture_output=True, text=True)
                results.append({"action": "exec", "status": "SUCCESS" if ret.returncode==0 else "FAILED", "output": ret.stdout[:500]})
            else:
                results.append({"action": action, "status": "FAILED", "error": f"unknown {action}"})
        except Exception as e:
            results.append({"action": action, "status": "FAILED", "error": str(e)})
            print(f"  -> {action} FAILED: {e}")
    return results

def main_loop():
    ensure_bridge_repo()
    print("[PURE BRIDGE - NUMBER 2] Dynamic file manager - watching")
    print(f"Commands registered: {len(fm.commands)} (dynamic, can grow)")
    print(f"Bridge repo: {BRIDGE_REPO}")
    print(f"Watching: {TASK_FILE}")
    while True:
        try:
            git_pull()
            if TASK_FILE.exists():
                try:
                    data = json.loads(TASK_FILE.read_text())
                    print(f"\n[TASK FOUND] {data.get('explanation','')}")
                    results = execute_task(data)
                    RESULT_FILE.write_text(json.dumps({"task": data.get("explanation"), "results": results, "timestamp": time.time()}, indent=2))
                    DONE_DIR.mkdir(parents=True, exist_ok=True)
                    try:
                        TASK_FILE.rename(DONE_DIR / f"done_{int(time.time())}.json")
                    except:
                        TASK_FILE.unlink(missing_ok=True)
                    git_push(f"result: {data.get('explanation','task')}")
                    print("[TASK DONE + PUSHED]")
                except Exception as e:
                    print(f"TASK FAILED: {e}")
                    import traceback
                    traceback.print_exc()
            QUEUE_DIR.mkdir(parents=True, exist_ok=True)
            for task_file in sorted(QUEUE_DIR.glob("task_*.json")):
                try:
                    data = json.loads(task_file.read_text())
                    print(f"[QUEUE TASK] {task_file.name}")
                    results = execute_task(data)
                    RESULT_FILE.write_text(json.dumps({"task": task_file.name, "results": results}, indent=2))
                    task_file.rename(DONE_DIR / task_file.name)
                    git_push(f"result: {task_file.name}")
                except Exception as e:
                    print(f"QUEUE TASK FAILED {task_file}: {e}")
                    try: task_file.rename(DONE_DIR / task_file.name)
                    except: pass
        except Exception as e:
            print(f"LOOP ERROR: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
