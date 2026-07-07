# Tasks

- [x] Task 1: 实现乱码检测模块
  - [x] SubTask 1.1: 在 folder2ai_core.py 中添加 `is_garbled_text()` 函数，实现乱码检测逻辑
  - [x] SubTask 1.2: 实现中文乱码模式检测（锟斤拷、烫烫烫等）
  - [x] SubTask 1.3: 实现不可打印字符比例检测
  - [x] SubTask 1.4: 实现乱码字符占比阈值判断（15%）

- [x] Task 2: 修改文件读取逻辑集成乱码检测
  - [x] SubTask 2.1: 修改 `try_read_text()` 函数，增加 `clean_data` 参数
  - [x] SubTask 2.2: 在读取成功后调用乱码检测函数
  - [x] SubTask 2.3: 根据检测结果返回 `[无法识别]` 或原始内容

- [x] Task 3: 更新核心函数接口传递清洗参数
  - [x] SubTask 3.1: 修改 `process_directory()` 函数，增加 `clean_data` 参数
  - [x] SubTask 3.2: 修改 `generate_output()` 函数，增加 `clean_data` 参数
  - [x] SubTask 3.3: 确保参数正确传递到所有相关函数调用

- [x] Task 4: 更新GUI界面增加数据清洗选项
  - [x] SubTask 4.1: 在GUI界面添加复选框控件用于控制数据清洗功能
  - [x] SubTask 4.2: 将复选框状态与核心函数参数绑定
  - [x] SubTask 4.3: 设置默认勾选状态

- [x] Task 5: 测试验证
  - [x] SubTask 5.1: 创建包含中文乱码的测试文件验证检测功能
  - [x] SubTask 5.2: 创建包含英文乱码的测试文件验证检测功能
  - [x] SubTask 5.3: 验证正常文件不会被误判
  - [x] SubTask 5.4: 验证GUI选项开关功能正常

# Task Dependencies
- Task 2 依赖 Task 1
- Task 3 依赖 Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 1-4