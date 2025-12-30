#!/usr/bin/env python
"""
打包配置文件
"""

import os
import re
from setuptools import setup, find_packages

# 读取版本号
with open(os.path.join("system_monitor", "__init__.py"), "r", encoding="utf-8") as f:
    version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    version = version_match.group(1) if version_match else "1.0.0"

# 读取README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# 读取requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    # 基础信息
    name="system-monitor-toolkit",
    version=version,
    author="System Monitor Team",
    author_email="contact@example.com",
    description="A comprehensive cross-platform system resource monitoring toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zsq86400/system-monitor-toolkit",
    license="MIT",

    # 分类信息
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="monitoring, system, resources, cpu, memory, disk, network, psutil",

    # 包配置
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*", "docs", "docs.*"]),
    include_package_data=True,
    package_data={
        "system_monitor": ["py.typed"],
    },

    # Python版本要求
    python_requires=">=3.6",

    # 依赖
    install_requires=requirements,
    extras_require={
        "gpu": ["gputil>=1.4.0"],
        "web": ["flask>=2.0.0", "dash>=2.0.0"],
        "full": [
            "gputil>=1.4.0",
            "flask>=2.0.0",
            "dash>=2.0.0",
            "plotly>=5.0.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "sphinx>=4.0.0",
            "twine>=3.4.0",
            "wheel>=0.37.0",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "pytest-mock>=3.6.0",
        ],
    },

    # 入口点
    entry_points={
        "console_scripts": [
            "sysmon=system_monitor.cli:main",
        ],
        "gui_scripts": [
            "sysmon-gui=system_monitor.gui:main [gui]",
        ],
    },

    # 其他
    zip_safe=False,
    project_urls={
        "Documentation": "https://system-monitor-toolkit.readthedocs.io/",
        "Source": "https://github.com/zsq86400/system-monitor-toolkit",
        "Tracker": "https://github.com/zsq86400/system-monitor-toolkit/issues",
        "Download": "https://github.com/zsq86400/system-monitor-toolkit/releases",
    },
)