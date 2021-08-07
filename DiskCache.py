from abc import ABC
from collections.abc import MutableMapping
from pathlib import Path
import json
import os
from shutil import rmtree
import pickle
import _pickle as cPickle
import gc
import marshal
import shelve
import torch


class DiskCache(MutableMapping, ABC):
    def __init__(self, folder_name, save_as="torch"):
        self.folder_name = folder_name
        self.save_as = save_as
        self.clear()
        self.shelve_cache = shelve.open("cache_tmp/shelve.shelve")

    def make_path(self, key):
        return self.folder_name + "/" + str(key)

    def __setitem__(self, key, value):
        gc.disable()
        self.keys[key] = True
        file_path = self.make_path(key)
        if self.save_as == "json":
            with open(f"{file_path}.json", "w") as f:
                json.dump(value, f)
        elif self.save_as == "pickle":
            with open(f"{file_path}.pickle", "wb") as f:
                cPickle.dump(value, f, protocol=pickle.HIGHEST_PROTOCOL)
        elif self.save_as == "marshal":
            with open(f"{file_path}.marshal", "wb") as f:
                marshal.dump(value, f)
        elif self.save_as == "shelve":
            self.shelve_cache[str(key)] = value
        elif self.save_as == "torch":
            torch.save(value, f"{file_path}.pt")

        gc.enable()
        # else:
        #     with bz2.BZ2File(f"{file_path}.pbz2", 'w') as f:
        #         cPickle.dump(value, f)

    def __getitem__(self, key):
        gc.disable()
        file_path = self.make_path(key)
        if self.save_as == "json":
            with open(f"{file_path}.json", "r") as f:
                data = json.load(f)
        elif self.save_as == "pickle":
            with open(f"{file_path}.pickle", "rb") as f:
                data = cPickle.load(f)
        elif self.save_as == "marshal":
            with open(f"{file_path}.marshal", "rb") as f:
                data = marshal.load(f)
        elif self.save_as == "shelve":
            data = self.shelve_cache[str(key)]
        elif self.save_as == "torch":
            data = torch.load(f"{file_path}.pt")
        gc.enable()
        return data

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
