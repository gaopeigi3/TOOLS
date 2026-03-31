import os
import hashlib
from collections import defaultdict

# 👉 输入路径
root_dir = input("请输入扫描路径（例如 F:\\Movies）：").strip()

# 👉 自动处理引号（防止你粘贴带引号）
root_dir = root_dir.strip('"').strip("'")

# 👉 检查路径是否存在
if not os.path.exists(root_dir):
    print("❌ 路径不存在，请检查！")
    exit()

print(f"扫描路径：{root_dir}")

VIDEO_EXT = ('.mkv', '.mp4', '.avi')

# def file_hash(path):
#     h = hashlib.md5()
#     with open(path, 'rb') as f:
#         for chunk in iter(lambda: f.read(8192), b''):
#             h.update(chunk)
#     return h.hexdigest()
def file_hash(path, chunk_size=1024*1024*4):  # 4MB
    h = hashlib.md5()
    with open(path, 'rb') as f:
        data = f.read(chunk_size)
        h.update(data)
    return h.hexdigest()
# Step 1：按大小分组
size_dict = defaultdict(list)

print("Scanning sizes...")

for root, dirs, files in os.walk(root_dir):
    for f in files:
        if not f.lower().endswith(VIDEO_EXT):
            continue

        path = os.path.join(root, f)

        try:
            size = os.path.getsize(path)
            size_dict[size].append(path)
        except Exception as e:
            print(f"Skip: {path} -> {e}")

# Step 2：筛选候选
candidates = [v for v in size_dict.values() if len(v) > 1]

print(f"Potential duplicate groups: {len(candidates)}")

# Step 3：hash
hash_dict = defaultdict(list)

print("Hashing...")

for group in candidates:
    for path in group:
        try:
            h = file_hash(path)
            hash_dict[h].append(path)
        except Exception as e:
            print(f"Hash error: {path} -> {e}")

# Step 4：输出
print("\n==== 重复电影 ====\n")

for h, files in hash_dict.items():
    if len(files) > 1:
        print("----")
        for f in files:
            print(f)