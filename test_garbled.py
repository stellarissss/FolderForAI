#!/usr/bin/env python3
"""
测试 folder2ai_core 模块的乱码检测和清洗功能
"""
import os
import sys
import folder2ai_core

# 测试文件路径
TEST_DIR = "/workspace/test_data"
TEST_FILES = {
    "normal.txt": False,  # 预期：不是乱码
    "chinese_garbled.txt": True,  # 预期：是乱码
    "english_garbled.txt": True,  # 预期：是乱码
    "mixed.txt": True,  # 预期：是乱码（因为乱码比例超过15%）
}

def test_is_garbled_text():
    """测试 is_garbled_text() 函数"""
    print("=" * 60)
    print("测试 1: is_garbled_text() 函数")
    print("=" * 60)

    all_passed = True
    for filename, expected in TEST_FILES.items():
        filepath = os.path.join(TEST_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        result = folder2ai_core.is_garbled_text(content)
        status = "✓ PASS" if result == expected else "✗ FAIL"

        print(f"\n文件: {filename}")
        print(f"  预期结果: {'乱码' if expected else '正常'}")
        print(f"  实际结果: {'乱码' if result else '正常'}")
        print(f"  状态: {status}")

        if result != expected:
            all_passed = False
            # 打印详细分析
            print(f"  详细分析:")
            print(f"    文件长度: {len(content)} 字符")

    return all_passed


def test_clean_data_true():
    """测试启用清洗功能时的输出"""
    print("\n" + "=" * 60)
    print("测试 2: generate_output() 启用清洗功能 (clean_data=True)")
    print("=" * 60)

    output = folder2ai_core.generate_output(TEST_DIR, clean_data=True)
    print("\n输出结果:")
    print("-" * 60)
    print(output)
    print("-" * 60)

    # 检查乱码文件是否被标记为 [无法识别]
    all_passed = True
    for filename, is_garbled in TEST_FILES.items():
        if is_garbled:
            # 乱码文件应该被标记为 [无法识别]
            if "[无法识别]" in output:
                # 检查该文件对应的标记
                lines = output.split("\n")
                found = False
                for i, line in enumerate(lines):
                    if filename in line:
                        # 检查接下来的几行是否有 [无法识别]
                        for j in range(i, min(i+5, len(lines))):
                            if "[无法识别]" in lines[j]:
                                found = True
                                break
                if found:
                    print(f"✓ {filename}: 正确标记为 [无法识别]")
                else:
                    print(f"✗ {filename}: 未找到 [无法识别] 标记")
                    all_passed = False
            else:
                print(f"✗ {filename}: 输出中未找到 [无法识别]")
                all_passed = False
        else:
            # 正常文件应该显示内容
            if "这是正常的文本文件" in output or "normal" in output.lower():
                print(f"✓ {filename}: 正常显示内容")
            else:
                print(f"✗ {filename}: 未正常显示内容")
                all_passed = False

    return all_passed


def test_clean_data_false():
    """测试关闭清洗功能时的输出"""
    print("\n" + "=" * 60)
    print("测试 3: generate_output() 关闭清洗功能 (clean_data=False)")
    print("=" * 60)

    output = folder2ai_core.generate_output(TEST_DIR, clean_data=False)
    print("\n输出结果:")
    print("-" * 60)
    print(output)
    print("-" * 60)

    # 检查乱码内容是否正常显示
    all_passed = True

    # 检查是否包含乱码字符（应该显示原始内容）
    if "锟斤拷" in output or "烫烫烫" in output or "屯屯屯" in output:
        print("✓ 乱码文件内容正常显示（未被清洗）")
    else:
        print("✗ 乱码文件内容未正确显示")
        all_passed = False

    # 检查是否不应该出现 [无法识别]
    if "[无法识别]" not in output:
        print("✓ 未出现 [无法识别] 标记")
    else:
        print("✗ 出现了 [无法识别] 标记（不应该出现）")
        all_passed = False

    return all_passed


def test_try_read_text():
    """测试 try_read_text() 函数"""
    print("\n" + "=" * 60)
    print("测试 4: try_read_text() 函数详细测试")
    print("=" * 60)

    all_passed = True

    # 测试正常文件
    print("\n--- 测试 normal.txt ---")
    content, is_text = folder2ai_core.try_read_text(
        os.path.join(TEST_DIR, "normal.txt"), clean_data=True
    )
    print(f"是否为文本文件: {is_text}")
    has_normal_content = "这是一个正常的文本文件" in content if content else False
    print(f"是否包含正常内容: {has_normal_content}")
    print(f"是否标记为无法识别: {content == '[无法识别]'}")

    if is_text and content != "[无法识别]" and has_normal_content:
        print("✓ PASS")
    else:
        print("✗ FAIL")
        all_passed = False

    # 测试乱码文件
    print("\n--- 测试 chinese_garbled.txt (clean_data=True) ---")
    content, is_text = folder2ai_core.try_read_text(
        os.path.join(TEST_DIR, "chinese_garbled.txt"), clean_data=True
    )
    print(f"是否为文本文件: {is_text}")
    print(f"内容: {content[:50] if content else None}")
    print(f"是否标记为无法识别: {content == '[无法识别]'}")

    if is_text and content == "[无法识别]":
        print("✓ PASS")
    else:
        print("✗ FAIL")
        all_passed = False

    # 测试乱码文件但不清洗
    print("\n--- 测试 chinese_garbled.txt (clean_data=False) ---")
    content, is_text = folder2ai_core.try_read_text(
        os.path.join(TEST_DIR, "chinese_garbled.txt"), clean_data=False
    )
    print(f"是否为文本文件: {is_text}")
    print(f"内容前50字符: {content[:50] if content else None}")
    print(f"是否包含乱码字符: {'锟斤拷' in content if content else False}")

    if is_text and "锟斤拷" in content:
        print("✓ PASS")
    else:
        print("✗ FAIL")
        all_passed = False

    return all_passed


def main():
    """运行所有测试"""
    print("=" * 60)
    print("开始测试 folder2ai_core 模块的乱码检测和清洗功能")
    print("=" * 60)

    results = {}

    # 运行所有测试
    results["is_garbled_text"] = test_is_garbled_text()
    results["clean_data_true"] = test_clean_data_true()
    results["clean_data_false"] = test_clean_data_false()
    results["try_read_text"] = test_try_read_text()

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过！")
        return 0
    else:
        print("部分测试失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())