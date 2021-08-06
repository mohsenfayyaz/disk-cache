from abc import ABC
from collections.abc import MutableMapping
from pathlib import Path
import json
import os
from shutil import rmtree
import bz2
import pickle
import _pickle as cPickle


class DiskCache(MutableMapping, ABC):
    def __init__(self, folder_name, save_as="pickle"):
        self.folder_name = folder_name
        self.save_as = save_as
        self.clear()

    def make_path(self, key):
        return self.folder_name + "/" + str(key)

    def __setitem__(self, key, value):
        self.keys[key] = True
        file_path = self.make_path(key)
        if self.save_as == "json":
            with open(f"{file_path}.json", "w") as f:
                json.dump(value, f)
        else:
            with open(f"{file_path}.pickle", "wb") as f:
                pickle.dump(value, f)
        # else:
        #     with bz2.BZ2File(f"{file_path}.pbz2", 'w') as f:
        #         cPickle.dump(value, f)

    def __getitem__(self, key):
        file_path = self.make_path(key)
        if self.save_as == "json":
            with open(f"{file_path}.json", "r") as f:
                return json.load(f)
        else:
            with open(f"{file_path}.pickle", "rb") as f:
                return pickle.load(f)
        # else:
        #     data = bz2.BZ2File(f"{file_path}.pbz2", "rb")
        #     return cPickle.load(data)

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
        if os.path.exists(self.folder_name):
            rmtree(self.folder_name)
        Path(self.folder_name).mkdir(parents=True)
