@echo off
REM Windows打包脚本

echo 清理旧的构建文件...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q *.egg-info 2>nul
del /q *.pyc 2>nul

echo 运行测试...
python -m pytest tests/ -v

echo 构建分发包...
python -m build

echo 检查打包文件...
python -m twine check dist/*

echo 打包完成！
echo 生成的包:
dir dist\

echo.
echo 安装测试:
echo   pip install dist\system_monitor_toolkit-*.whl
echo.
echo 上传到PyPI测试:
echo   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
echo.
echo 上传到PyPI正式:
echo   python -m twine upload dist/*