import hashlib

def get_paging_info(row_total=0, page=0, page_size=20):
    if row_total % page_size == 0:
        page_total = row_total / page_size
    else:
        page_total = row_total / page_size + 1
    result = {
        "row_total": row_total,
        "page": 1 if row_total == 0 else page,
        "page_size": page_size,
        "page_total": page_total,
        "page_previous": page if page <= 1 else page - 1,
        "page_next": page_total if page >= page_total else page + 1,
        "row_start": (page - 1) * page_size + 1
    }
    return result


def sha1(text):
    sha = hashlib.sha1()
    sha.update(text.encode("utf8"))
    return sha.hexdigest()


def file_hash(file_path, t="sha1"):
    if t == "sha1":
        lib = hashlib.sha1()
    elif t == "sha256":
        lib = hashlib.sha256()
    else:
        lib = hashlib.md5()

    with open(file_path, "rb") as f:
        lib.update(f.read())

    return lib.hexdigest()


def check_hash_dir(root, h):
    import os
    grade_one = h[0:2]
    grade_two = h[2:4]

    path_grade_one = os.path.join(root, grade_one)
    path_grade_two = os.path.join(path_grade_one, grade_two)

    if not os.path.exists(path_grade_one):
        os.mkdir(path_grade_one)

    if not os.path.exists(path_grade_two):
        os.mkdir(path_grade_two)

    return path_grade_two
