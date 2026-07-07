# Checklist

- [x] `is_garbled_text()` 函数已实现并能正确检测中文乱码
- [x] `is_garbled_text()` 函数能正确检测英文乱码（高比例不可打印字符）
- [x] 乱码检测阈值设置为15%并正常工作
- [x] `try_read_text()` 函数已增加 `clean_data` 参数
- [x] 文件内容被正确替换为 `[无法识别]` 标记
- [x] `process_directory()` 函数已增加 `clean_data` 参数
- [x] `generate_output()` 函数已增加 `clean_data` 参数
- [x] GUI界面已添加数据清洗复选框控件
- [x] 复选框默认为勾选状态
- [x] 关闭清洗选项时文件内容正常输出
- [x] 正常文本文件不会被误判为乱码
- [x] 包含乱码的文件内容被正确替换