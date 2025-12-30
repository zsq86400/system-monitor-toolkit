import os
import sys


def create_directory_structure():
    # 定义目录结构
    structure = {
        "system_monitor": {
            "__init__.py": "",
            "monitor.py": "# 主要监控类\n",
            "collectors": {
                "__init__.py": "",
                "cpu_collector.py": "",
                "memory_collector.py": "",
                "disk_collector.py": "",
                "network_collector.py": "",
                "process_collector.py": ""
            },
            "exporters": {
                "__init__.py": "",
                "console_exporter.py": "",
                "csv_exporter.py": "",
                "json_exporter.py": ""
            },
            "utils": {
                "__init__.py": "",
                "helpers.py": ""
            },
            "examples": {
                "basic_usage.py": "",
                "continuous_monitor.py": ""
            },
            "requirements.txt": ""
        }
    }

    # 创建目录和文件
    def create_structure(base_path, struct):
        for name, content in struct.items():
            path = os.path.join(base_path, name)

            if isinstance(content, dict):
                # 这是一个目录
                os.makedirs(path, exist_ok=True)
                print(f"创建目录: {path}")
                create_structure(path, content)
            else:
                # 这是一个文件
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"创建文件: {path}")

    # 获取当前工作目录
    current_dir = os.getcwd()

    # 检查是否已存在
    if os.path.exists("system_monitor"):
        response = input("目录 'system_monitor' 已存在。是否要覆盖？(y/n): ")
        if response.lower() != 'y':
            print("操作已取消。")
            sys.exit(0)
        else:
            # 删除现有目录
            import shutil
            shutil.rmtree("system_monitor")

    # 创建目录结构
    print("正在创建目录结构...")
    create_structure(current_dir, structure)

    # 创建更完整的示例文件内容
    examples_dir = os.path.join(current_dir, "system_monitor", "examples")

    # 基本使用示例
    basic_usage_content = """#!/usr/bin/env python3
"""
    basic_usage_content += '"""基本使用示例"""\n\n'
    basic_usage_content += "from system_monitor.monitor import SystemMonitor\nfrom system_monitor.exporters.console_exporter import ConsoleExporter\n\n"
    basic_usage_content += "def main():\n    monitor = SystemMonitor()\n    exporter = ConsoleExporter()\n    \n    # 收集一次系统数据\n    data = monitor.collect()\n    \n    # 导出到控制台\n    exporter.export(data)\n\nif __name__ == \"__main__\":\n    main()\n"

    with open(os.path.join(examples_dir, "basic_usage.py"), 'w', encoding='utf-8') as f:
        f.write(basic_usage_content)

    # 连续监控示例
    continuous_monitor_content = """#!/usr/bin/env python3
"""
    continuous_monitor_content += '"""连续监控示例"""\n\n'
    continuous_monitor_content += "import time\nfrom system_monitor.monitor import SystemMonitor\nfrom system_monitor.exporters.csv_exporter import CSVExporter\n\n"
    continuous_monitor_content += "def main():\n    monitor = SystemMonitor()\n    exporter = CSVExporter('system_metrics.csv')\n    \n    print(\"开始系统监控，按Ctrl+C停止...\")\n    try:\n        while True:\n            data = monitor.collect()\n            exporter.export(data)\n            time.sleep(5)  # 每5秒收集一次\n    except KeyboardInterrupt:\n        print(\"\\n监控已停止\")\n\nif __name__ == \"__main__\":\n    main()\n"

    with open(os.path.join(examples_dir, "continuous_monitor.py"), 'w', encoding='utf-8') as f:
        f.write(continuous_monitor_content)

    # 创建requirements.txt内容
    requirements_content = "psutil>=5.8.0\n"

    with open(os.path.join(current_dir, "system_monitor", "requirements.txt"), 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    print(f"\n目录结构创建完成！")
    print(f"位置: {os.path.join(current_dir, 'system_monitor')}")
    print("\n目录结构:")
    print_tree(os.path.join(current_dir, "system_monitor"))


def print_tree(startpath, prefix=""):
    """打印目录树结构"""
    contents = os.listdir(startpath)
    pointers = ["├── "] * (len(contents) - 1) + ["└── "]

    for pointer, path in zip(pointers, contents):
        full_path = os.path.join(startpath, path)
        print(prefix + pointer + path)
        if os.path.isdir(full_path):
            extension = "│   " if pointer == "├── " else "    "
            print_tree(full_path, prefix + extension)


if __name__ == "__main__":
    create_directory_structure()