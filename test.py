from DiskCache import DiskCache
from timeit import timeit
from tqdm.auto import tqdm

disk_cache = DiskCache("cache_tmp", save_as="pickle")
for j in tqdm(range(15)):
    disk_cache[j*32] = ["b", "a", {"a": "c"}, [i**2+0.1654 for i in range(768*2*13*32)]]
for j in tqdm(range(15)):
    a = disk_cache[j*32]
print("0" in disk_cache)
print("b" in disk_cache)
