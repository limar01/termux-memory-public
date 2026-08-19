"""
zero_touch_bridge.py - ZERO COPY-PASTE BRIDGE - FINAL
Utos lang si boss sa chat, auto execute sa Termux - NO COPY PASTE!
"""
import time, json, os, subprocess
from pathlib import Path
MEMORY_REPO = Path.home() / "termux-memory-public"
TASK_FILE_MEMORY = MEMORY_REPO / "autotask.json"
RESULT_FILE = MEMORY_REPO / "result.json"
DONE_DIR = MEMORY_REPO / "done_tasks"
try:
    from lib.file_manager import FileManager
    fm = FileManager()
except:
    import sys
    sys.path.append(str(MEMORY_REPO))
    from lib.file_manager import FileManager
    fm = FileManager()
def git_pull_memory():
    if MEMORY_REPO.exists() and (MEMORY_REPO / ".git").exists():
        os.system(f"cd {MEMORY_REPO} && git pull --quiet 2>/dev/null")
        return True
    return False
def execute_task(task_data):
    print(f"\n[ZERO-TOUCH TASK] {task_data.get('explanation','')}")
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
                print(f" ✅ {action} {cmd.get('path') or cmd.get('src','')} = SUCCESS")
            elif action == "exec":
                ret = subprocess.run(cmd.get("command"), shell=True, capture_output=True, text=True)
                results.append({"action": "exec", "status": "SUCCESS" if ret.returncode==0 else "FAILED", "output": ret.stdout[:500]})
            else:
                results.append({"action": action, "status": "FAILED", "error": f"unknown {action}"})
        except Exception as e:
            results.append({"action": action, "status": "FAILED", "error": str(e)})
            print(f" ❌ {action} FAILED: {e}")
    return results
def main_loop():
    MEMORY_REPO.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    print("[ZERO-TOUCH BRIDGE] - UTOS LANG SI BOSS, NO COPY-PASTE!")
    print(f"Commands registered: {len(fm.commands)} (47 FINAL)")
    print(f"Watching: {TASK_FILE_MEMORY}")
    last_task_mtime = 0
    while True:
        try:
            git_pull_memory()
            if TASK_FILE_MEMORY.exists():
                mtime = TASK_FILE_MEMORY.stat().st_mtime
                if mtime!= last_task_mtime:
                    last_task_mtime = mtime
                    try:
                        data = json.loads(TASK_FILE_MEMORY.read_text())
                        if not data.get("executed"):
                            results = execute_task(data)
                            data["executed"] = True
                            data["executed_at"] = time.time()
                            RESULT_FILE.write_text(json.dumps({"task": data.get("explanation"), "results": results, "timestamp": time.time()}, indent=2))
                            done_file = DONE_DIR / f"done_{int(time.time())}.json"
                            TASK_FILE_MEMORY.rename(done_file)
                            if (MEMORY_REPO / ".git").exists():
                                os.system(f"cd {MEMORY_REPO} && git add. && git commit -m 'executed: {data.get('explanation','task')}' --quiet 2>/dev/null && git push --quiet 2>/dev/null")
                            print(f"\n[✅ TASK DONE] {data.get('explanation')}")
                            print("Waiting for next utos...\n")
                    except Exception as e:
                        print(f"[ERROR] {e}")
        except Exception as e:
            print(f"LOOP ERROR: {e}")
        time.sleep(5)
if __name__ == "__main__":
    main_loop()
