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
