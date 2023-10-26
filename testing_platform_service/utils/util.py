import os

# 递归算法
def generate_tree(source, parent):
    tree = []
    for item in source:
        if item["parent_id"] == parent:
            item["children"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree

# 根据id查询所有下级id
def get_childer_ids(source, parent):
    ids = []
    for item in source:
        if item["parent_id"] == parent:
            ids.append(item["id"])
            get_childer_ids(source, item["id"])
    return ids

# 文件迭代器
def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data