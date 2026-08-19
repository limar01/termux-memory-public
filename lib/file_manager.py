# Dynamic File Manager - NOT FIXED 47, CAN GROW
import os, shutil, json, hashlib, zipfile, tarfile
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self):
        self.commands = {}
        self._register_all()
    def register(self, name, func):
        self.commands[name] = func
        setattr(self, name, func)
    def _register_all(self):
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
    def list_dir(self, p): return __import__("os").listdir(__import__("os.path").expanduser(p))
    def list_recursive(self, p): 
        from pathlib import Path
        return [str(x) for x in Path(__import__("os.path").expanduser(p)).rglob("*")]
    def make_dir(self, p):
        from pathlib import Path
        Path(__import__("os.path").expanduser(p)).mkdir(parents=True, exist_ok=True); return True
    def remove_dir(self, p):
        import shutil, os.path
        shutil.rmtree(os.path.expanduser(p), ignore_errors=True); return True
    def make_file(self, p, c=""):
        from pathlib import Path
        import os.path
        Path(os.path.expanduser(p)).parent.mkdir(parents=True, exist_ok=True)
        Path(os.path.expanduser(p)).write_text(c)
        return True
    def read_file(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).read_text()
    def write_file(self, p, c):
        from pathlib import Path
        import os.path
        Path(os.path.expanduser(p)).parent.mkdir(parents=True, exist_ok=True)
        Path(os.path.expanduser(p)).write_text(c)
        return True
    def append_file(self, p, c):
        from pathlib import Path
        import os.path
        Path(os.path.expanduser(p)).parent.mkdir(parents=True, exist_ok=True)
        open(os.path.expanduser(p), "a").write(c)
        return True
    def delete_file(self, p):
        from pathlib import Path
        import os.path
        Path(os.path.expanduser(p)).unlink(missing_ok=True)
        return True
    def copy_file(self, s, d):
        from pathlib import Path
        import shutil, os.path
        Path(os.path.expanduser(d)).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(os.path.expanduser(s), os.path.expanduser(d))
        return True
    def move_file(self, s, d):
        from pathlib import Path
        import shutil, os.path
        Path(os.path.expanduser(d)).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(os.path.expanduser(s), os.path.expanduser(d))
        return True
    def rename_file(self, s, d):
        return self.move_file(s, d)
    def file_exists(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).exists()
    def dir_exists(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).is_dir()
    def is_file(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).is_file()
    def is_dir(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).is_dir()
    def get_size(self, p):
        from pathlib import Path
        import os.path
        return Path(os.path.expanduser(p)).stat().st_size if Path(os.path.expanduser(p)).exists() else 0
    def get_mtime(self, p):
        from pathlib import Path
        from datetime import datetime
        import os.path
        return datetime.fromtimestamp(Path(os.path.expanduser(p)).stat().st_mtime) if Path(os.path.expanduser(p)).exists() else None
    def get_ctime(self, p):
        from pathlib import Path
        from datetime import datetime
        import os.path
        return datetime.fromtimestamp(Path(os.path.expanduser(p)).stat().st_ctime) if Path(os.path.expanduser(p)).exists() else None
