from DiskCache import DiskCache
from timeit import timeit
from tqdm.auto import tqdm
import torch

disk_cache = DiskCache("cache_tmp", save_as="torch")
for j in tqdm(range(10)):
    disk_cache[j*32] = ["b", "a", {"a": "c"}, torch.tensor([i**2*0.1651875423 for i in range(768*4*13*32)])]
for _ in range(10):
    for j in tqdm(range(10)):
        if j*32 in disk_cache:
            a = disk_cache[j*32]
print("0" in disk_cache)
print("b" in disk_cache)