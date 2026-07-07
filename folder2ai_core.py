#这是本项目的核心功能代码
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


def try_read_text(filepath, clean_data=True):
    # 尝试多种编码读取文本文件
    for enc in ["utf-8", "gbk", "latin-1"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
                # 如果启用清洗且检测到乱码，返回标记
                if clean_data and is_garbled_text(content):
                    return "[无法识别]", True
                return content, True
        except (UnicodeDecodeError, ValueError):
            continue
    return None, False


def is_garbled_text(content):
    """
    检测文本内容是否为乱码。

    检测逻辑包括：
    1. 检测常见中文乱码模式（如连续的替代字符、重复的无效字节序列）
    2. 检测高比例的不可打印字符
    3. 检测无效的Unicode序列

    当乱码字符占比超过15%时返回True，否则返回False。

    Args:
        content: 待检测的文本内容

    Returns:
        bool: 如果检测为乱码返回True，否则返回False
    """
    if not content or len(content) == 0:
        return False

    total_chars = len(content)
    garbled_count = 0

    # 1. 检测常见中文乱码模式
    # 常见乱码字符组合（不包括\ufffd，在步骤2单独处理）
    garbled_patterns = [
        '锟斤拷',   # 经典GBK/UTF-8编码转换乱码
        '烫烫烫',   # Visual Studio未初始化内存模式
        '屯屯屯',   # Visual Studio堆内存模式
    ]

    # 统计乱码模式出现次数
    for pattern in garbled_patterns:
        garbled_count += content.count(pattern) * len(pattern)

    # 2. 检测连续出现的Unicode替代字符
    # 替代字符连续出现通常表示编码错误
    consecutive_replacement = 0
    i = 0
    while i < len(content):
        if content[i] == '\ufffd':
            # 统计连续替代字符的长度
            start = i
            while i < len(content) and content[i] == '\ufffd':
                i += 1
            length = i - start
            # 连续2个或以上替代字符更可能是乱码
            if length >= 2:
                consecutive_replacement += length
        else:
            i += 1

    garbled_count += consecutive_replacement

    # 3. 检测高频重复的无效字节序列
    # 某些特定字符重复出现可能是内存模式
    repeat_patterns = ['□', '◇', '◆']
    for pattern in repeat_patterns:
        count = content.count(pattern)
        if count >= 3:  # 同一字符重复3次以上
            garbled_count += count

    # 4. 检测不可打印字符比例
    # 不可打印字符包括控制字符(0x00-0x1F, 0x7F)和无效字符
    # 注意：\ufffd已在步骤1和2中统计，此处不再重复计算
    unprintable_chars = 0
    for char in content:
        code = ord(char)
        # 控制字符范围（排除常用的空白字符如\t, \n, \r）
        if code < 0x20 and char not in '\t\n\r':
            unprintable_chars += 1
        # DEL字符和其他控制字符
        elif code == 0x7F:
            unprintable_chars += 1
        # 私用区字符（通常是无效显示）
        elif 0xE000 <= code <= 0xF8FF:
            unprintable_chars += 1

    garbled_count += unprintable_chars

    # 5. 计算乱码字符占比
    ratio = garbled_count / total_chars if total_chars > 0 else 0

    # 超过15%判定为乱码
    return ratio > 0.15


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


def process_directory(root_dir, depth=0, clean_data=True):
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
            content, is_text = try_read_text(filepath, clean_data)
            if is_text:
                result.append(f"[{filename}]\n{content}\n")
        if not sub_dirs and not sub_files:
            result.append("[空文件夹]\n")

        # 递归处理子文件夹
        if sub_dirs:
            result.extend(process_directory(dirpath, depth + 1, clean_data))

    # 再处理文件
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        content, is_text = try_read_text(filepath, clean_data)

        result.append(f"\n{SEPARATOR} {level_name} 文件: {filename} {SEPARATOR}\n")
        # 仿照示例：二进制文件(如photo.jpg)只有标题，没有[文件名]和内容块
        if is_text:
            result.append(f"[{filename}]\n{content}\n")

    return result


def generate_output(folder_path, clean_data=True):
    folder_name = os.path.basename(folder_path)
    tree_str = generate_tree(folder_path)
    content_str = "".join(process_directory(folder_path, clean_data=clean_data))

    return f"文件夹名: {folder_name}\n{SEPARATOR} 结构总览 {SEPARATOR}\n{tree_str}\n{content_str}"
