

def remove_intersection_path(path1, path2):
    str_path1 = str(path1)
    str_path2 = str(path2)

    shrt_path = str_path1 if len(str_path1) < len(str_path2) else str_path2
    long_path = str_path1 if len(str_path1) > len(str_path2) else str_path2

    shrt_idx = long_path.find(shrt_path)
    if shrt_idx == 0:
        return long_path.replace(shrt_path, "").lstrip("\\/")
    raise ValueError()
