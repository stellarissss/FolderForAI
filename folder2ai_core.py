import os

SEPARATOR = "=" * 40
LEVEL_NAMES = {
    0: "第零层", 1: "第一层", 2: "第二层", 3: "第三层",
    4: "第四层", 5: "第五层", 6: "第六层", 7: "第七层",
    8: "第八层", 9: "第九层", 10: "第十层",
}


def get_level_name(depth):
    return LEVEL_NAMES.get(depth, f"第{depth}层")


def sorted_entries(path):
    try:
        entries = os.listdir(path)
    except PermissionError:
        return [], []
    dirs = sorted([e for e in entries if os.path.isdir(os.path.join(path, e))])
    files = sorted([e for e in entries if os.path.isfile(os.path.join(path, e))])
    return dirs, files


def try_read_text(filepath):
    # 尝试多种编码读取文本文件
    for enc in ["utf-8", "gbk", "latin-1"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read(), True
        except (UnicodeDecodeError, ValueError):
            continue
    return None, False


def generate_tree(root_dir):
    lines = []
    dirs, files = sorted_entries(root_dir)
    for d in dirs:
        lines.append(d + "/")
        _build_subtree(os.path.join(root_dir, d), lines, "")
    for f in files:
        lines.append(f)
    return "\n".join(lines)


def _build_subtree(dir_path, lines, prefix):
    dirs, files = sorted_entries(dir_path)
    all_items = dirs + files
    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        is_dir = os.path.isdir(os.path.join(dir_path, item))
        lines.append(prefix + connector + item + ("/" if is_dir else ""))
        if is_dir:
            new_prefix = prefix + ("    " if is_last else "│   ")
            _build_subtree(os.path.join(dir_path, item), lines, new_prefix)


def process_directory(root_dir, depth=0):
    result = []
    level_name = get_level_name(depth)
    dirs, files = sorted_entries(root_dir)

    # 先处理子文件夹
    for dirname in dirs:
        dirpath = os.path.join(root_dir, dirname)
        sub_dirs, sub_files = sorted_entries(dirpath)

        result.append(f"\n{SEPARATOR} {level_name} 子文件夹: {dirname} {SEPARATOR}\n")

        # 列出该文件夹的直接子文件
        for filename in sub_files:
            filepath = os.path.join(dirpath, filename)
            content, is_text = try_read_text(filepath)
            if is_text:
                result.append(f"[{filename}]\n{content}\n")
        if not sub_dirs and not sub_files:
            result.append("[空文件夹]\n")

        # 递归处理子文件夹
        if sub_dirs:
            result.extend(process_directory(dirpath, depth + 1))

    # 再处理文件
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        content, is_text = try_read_text(filepath)

        result.append(f"\n{SEPARATOR} {level_name} 文件: {filename} {SEPARATOR}\n")
        # 仿照示例：二进制文件(如photo.jpg)只有标题，没有[文件名]和内容块
        if is_text:
            result.append(f"[{filename}]\n{content}\n")

    return result


def generate_output(folder_path):
    folder_name = os.path.basename(folder_path)
    tree_str = generate_tree(folder_path)
    content_str = "".join(process_directory(folder_path))

    return f"文件夹名: {folder_name}\n{SEPARATOR} 结构总览 {SEPARATOR}\n{tree_str}\n{content_str}"
