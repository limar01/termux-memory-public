# Dynamic File Manager - NOT FIXED 47, CAN GROW
# Repo: termux-memory-public - PLAIN
# This is the complete file management memory

import os
import shutil
import json
import hashlib
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self):
        self.commands = {}
        self._register_all()
    
    def register(self, name, func):
        # Dynamic add - kung may kulang, dagdag lang dito
        self.commands[name] = func
        setattr(self, name, func)
    
    def _register_all(self):
        # 1-12 Basic
        self.register("list_dir", self.list_dir)
        self.register("list_recursive", self.list_recursive)
        self.register("make_dir", self.make_dir)
        self.register("remove_dir", self.remove_dir)
        self.register("make_file", self.make_file)
        self.register("read_file", self.read_file)
        self.register("write_file", self.write_file)
        self.register("append_file", self.append_file)
        self.register("delete_file", self.delete_file)
        self.register("copy_file", self.copy_file)
        self.register("move_file", self.move_file)
        self.register("rename_file", self.rename_file)
        
        # 13-22 Check
        self.register("file_exists", self.file_exists)
        self.register("dir_exists", self.dir_exists)
        self.register("is_file", self.is_file)
        self.register("is_dir", self.is_dir)
        self.register("get_size", self.get_size)
        self.register("get_mtime", self.get_mtime)
        self.register("get_ctime", self.get_ctime)
        self.register("get_file_info", self.get_file_info)
        self.register("list_hidden", self.list_hidden)
        self.register("ensure_dir", self.ensure_dir)
        
        # 23-33 Content & Search
        self.register("read_lines", self.read_lines)
        self.register("write_lines", self.write_lines)
        self.register("search_files", self.search_files)
        self.register("find_ext", self.find_ext)
        self.register("count_files", self.count_files)
        self.register("count_dirs", self.count_dirs)
        self.register("clean_dir", self.clean_dir)
        self.register("copy_dir", self.copy_dir)
        self.register("move_dir", self.move_dir)
        self.register("read_json", self.read_json)
        self.register("write_json", self.write_json)
        
        # 34-47 JSON, Archive, Backup, System
        self.register("append_json", self.append_json)
        self.register("update_json", self.update_json)
        self.register("zip_files", self.zip_files)
        self.register("unzip_files", self.unzip_files)
        self.register("tar_files", self.tar_files)
        self.register("untar_files", self.untar_files)
        self.register("get_hash", self.get_hash)
        self.register("get_checksum", self.get_checksum)
        self.register("backup_file", self.backup_file)
        self.register("restore_file", self.restore_file)
        self.register("get_disk_usage", self.get_disk_usage)
        self.register("get_free_space", self.get_free_space)
        self.register("clean_temp", self.clean_temp)
        self.register("touch_file", self.touch_file)

    # === IMPLEMENTATIONS ===
    def list_dir(self, path): return os.listdir(os.path.expanduser(path))
    def list_recursive(self, path): return [str(p) for p in Path(os.path.expanduser(path)).rglob("*")]
    def make_dir(self, path): Path(os.path.expanduser(path)).mkdir(parents=True, exist_ok=True); return True
    def remove_dir(self, path): shutil.rmtree(os.path.expanduser(path), ignore_errors=True); return True
    def make_file(self, path, content=""): Path(os.path.expanduser(path)).parent.mkdir(parents=True, exist_ok=True); Path(os.path.expanduser(path)).write_text(content); return True
    def read_file(self, path): return Path(os.path.expanduser(path)).read_text()
    def write_file(self, path, content): Path(os.path.expanduser(path)).parent.mkdir(parents=True, exist_ok=True); Path(os.path.expanduser(path)).write_text(content); return True
    def append_file(self, path, content): Path(os.path.expanduser(path)).parent.mkdir(parents=True, exist_ok=True); open(os.path.expanduser(path), "a").write(content); return True
    def delete_file(self, path): Path(os.path.expanduser(path)).unlink(missing_ok=True); return True
    def copy_file(self, src, dst): Path(os.path.expanduser(dst)).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(os.path.expanduser(src), os.path.expanduser(dst)); return True
    def move_file(self, src, dst): Path(os.path.expanduser(dst)).parent.mkdir(parents=True, exist_ok=True); shutil.move(os.path.expanduser(src), os.path.expanduser(dst)); return True
    def rename_file(self, src, dst): return self.move_file(src, dst)
    def file_exists(self, path): return Path(os.path.expanduser(path)).exists()
    def dir_exists(self, path): return Path(os.path.expanduser(path)).is_dir()
    def is_file(self, path): return Path(os.path.expanduser(path)).is_file()
    def is_dir(self, path): return Path(os.path.expanduser(path)).is_dir()
    def get_size(self, path): return Path(os.path.expanduser(path)).stat().st_size if Path(os.path.expanduser(path)).exists() else 0
    def get_mtime(self, path): return datetime.fromtimestamp(Path(os.path.expanduser(path)).stat().st_mtime) if Path(os.path.expanduser(path)).exists() else None
    def get_ctime(self, path): return datetime.fromtimestamp(Path(os.path.expanduser(path)).stat().st_ctime) if Path(os.path.expanduser(path)).exists() else None
    def get_file_info(self, path): p=Path(os.path.expanduser(path)); return {"exists":p.exists(),"is_file":p.is_file(),"size":p.stat().st_size if p.exists() else 0,"mtime":str(self.get_mtime(path))} if p.exists() else {"exists":False}
    def list_hidden(self, path): return [f for f in os.listdir(os.path.expanduser(path)) if f.startswith(".")]
    def ensure_dir(self, path): Path(os.path.expanduser(path)).mkdir(parents=True, exist_ok=True); return True
    def read_lines(self, path): return Path(os.path.expanduser(path)).read_text().splitlines()
    def write_lines(self, path, lines): Path(os.path.expanduser(path)).write_text("\n".join(lines)); return True
    def search_files(self, path, keyword): return [str(p) for p in Path(os.path.expanduser(path)).rglob("*") if keyword in p.name]
    def find_ext(self, path, ext): return [str(p) for p in Path(os.path.expanduser(path)).rglob(f"*{ext}")]
    def count_files(self, path): return len([p for p in Path(os.path.expanduser(path)).rglob("*") if p.is_file()])
    def count_dirs(self, path): return len([p for p in Path(os.path.expanduser(path)).rglob("*") if p.is_dir()])
    def clean_dir(self, path): [shutil.rmtree(str(p), ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True) for p in Path(os.path.expanduser(path)).iterdir()]; return True
    def copy_dir(self, src, dst): shutil.copytree(os.path.expanduser(src), os.path.expanduser(dst), dirs_exist_ok=True); return True
    def move_dir(self, src, dst): shutil.move(os.path.expanduser(src), os.path.expanduser(dst)); return True
    def read_json(self, path): return json.loads(Path(os.path.expanduser(path)).read_text())
    def write_json(self, path, data): Path(os.path.expanduser(path)).parent.mkdir(parents=True, exist_ok=True); Path(os.path.expanduser(path)).write_text(json.dumps(data, indent=2)); return True
    def append_json(self, path, data): cur=self.read_json(path) if Path(os.path.expanduser(path)).exists() else []; cur.append(data) if isinstance(cur,list) else cur.update(data); self.write_json(path,cur); return True
    def update_json(self, path, data): cur=self.read_json(path) if Path(os.path.expanduser(path)).exists() else {}; cur.update(data); self.write_json(path,cur); return True
    def zip_files(self, src, dst): 
        with zipfile.ZipFile(os.path.expanduser(dst), 'w') as z: 
            for p in Path(os.path.expanduser(src)).rglob("*"): 
                if p.is_file(): z.write(p, p.relative_to(Path(os.path.expanduser(src))))
        return True
    def unzip_files(self, src, dst): Path(os.path.expanduser(dst)).mkdir(parents=True, exist_ok=True); zipfile.ZipFile(os.path.expanduser(src)).extractall(os.path.expanduser(dst)); return True
    def tar_files(self, src, dst):
        with tarfile.open(os.path.expanduser(dst), 'w') as t: t.add(os.path.expanduser(src), arcname=Path(os.path.expanduser(src)).name)
        return True
    def untar_files(self, src, dst): Path(os.path.expanduser(dst)).mkdir(parents=True, exist_ok=True); tarfile.open(os.path.expanduser(src)).extractall(os.path.expanduser(dst)); return True
    def get_hash(self, path): return hashlib.md5(Path(os.path.expanduser(path)).read_bytes()).hexdigest() if Path(os.path.expanduser(path)).exists() else None
    def get_checksum(self, path): return self.get_hash(path)
    def backup_file(self, path): dst=str(Path(os.path.expanduser(path)))+".bak"; shutil.copy2(os.path.expanduser(path), dst); return dst
    def restore_file(self, backup_path, original_path): shutil.copy2(os.path.expanduser(backup_path), os.path.expanduser(original_path)); return True
    def get_disk_usage(self, path): return shutil.disk_usage(os.path.expanduser(path))
    def get_free_space(self, path): return shutil.disk_usage(os.path.expanduser(path)).free
    def clean_temp(self): [Path(p).unlink(missing_ok=True) for p in ["/tmp/tempfile", os.path.expanduser("~/tmp")]]; return True
    def touch_file(self, path): Path(os.path.expanduser(path)).parent.mkdir(parents=True, exist_ok=True); Path(os.path.expanduser(path)).touch(exist_ok=True); return True

# Dynamic add example - kung may kulang, dagdag lang:
# fm = FileManager()
# fm.register("my_new_command", lambda path: print(f"new {path}"))
# Now fm has 48, 49, 50... dynamic!

fm = FileManager()
