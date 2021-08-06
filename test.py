from DiskCache import DiskCache
from timeit import timeit

disk_cache = DiskCache("cache_tmp")
disk_cache["a"] = ["b", "a", {"a": "c"}, [i**2+0.1 for i in range(768*2*13*32)]]
disk_cache["bbasdfasdfdasf"] = ["b", "a", {"a": "c"}, [i**2+0.1 for i in range(768*2*13*32)]]
print(disk_cache["a"])
print("a" in disk_cache)
print("b" in disk_cache)
