#!/bin/bash
# 打包脚本

set -e  # 出错时退出

echo "清理旧的构建文件..."
rm -rf build/ dist/ *.egg-info/ __pycache__/ system_monitor/__pycache__/

echo "运行测试..."
python -m pytest tests/ -v

echo "代码检查..."
python -m flake8 system_monitor/ tests/

echo "类型检查..."
python -m mypy system_monitor/

echo "构建分发包..."
python -m build

echo "检查打包文件..."
twine check dist/*

echo "打包完成！"
echo "生成的包:"
ls -la dist/

echo ""
echo "安装测试:"
echo "  pip install dist/system_monitor_toolkit-*.whl"
echo ""
echo "上传到PyPI测试:"
echo "  twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
echo ""
echo "上传到PyPI正式:"
echo "  twine upload dist/*"