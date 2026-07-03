@echo off
echo ======================================
echo  正在打包 Folder2AI 应用...
echo ======================================

pip install pyinstaller -q
pyinstaller --noconsole --onefile --name Folder2AI folder2ai_gui.py

echo.
echo ======================================
echo  打包完成！可执行文件在 dist 文件夹中。
echo ======================================
pause
