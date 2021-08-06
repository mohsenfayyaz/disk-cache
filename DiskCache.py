from abc import ABC
from collections.abc import MutableMapping
from pathlib import Path
import json
import os
from shutil import rmtree


class DiskCache(MutableMapping, ABC):
    def __init__(self, folder_name):
        self.folder_name = folder_name
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        self.keys = dict()

    def make_path(self, key):
        return self.folder_name + "/" + str(key)

    def __setitem__(self, key, value):
        self.keys[key] = True
        file_path = self.make_path(key)
        with open(f"{file_path}.json", "w") as json_file:
            json.dump(value, json_file)

    def __getitem__(self, key):
        file_path = self.make_path(key)
        with open(f"{file_path}.json", "r") as json_file:
            return json.load(json_file)

    def __contains__(self, key):
        return self.keys.__contains__(key)

    def __delitem__(self, key):
        file_path = self.make_path(key)
        if os.path.exists(file_path):
            os.remove(file_path)
            del self.keys[key]

    def __iter__(self):
        return iter(self.keys)

    def __len__(self):
        return len(self.keys)

    def clear(self):
        self.keys = dict()
        rmtree(self.folder_name)
        Path(self.folder_name).mkdir(parents=True, exist_ok=True)
