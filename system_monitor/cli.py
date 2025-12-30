#!/usr/bin/env python3
"""
命令行接口
"""

import argparse
import sys
import json
import time
from datetime import datetime
from typing import Optional

from . import SystemMonitor, ConsoleExporter, CSVExporter, JSONExporter


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="系统资源监控工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  sysmon info                    # 显示系统信息
  sysmon monitor                 # 实时监控
  sysmon monitor --output data.csv --interval 2  # 保存到CSV文件
  sysmon monitor --format json --quiet          # JSON格式静默输出
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # info命令
    info_parser = subparsers.add_parser("info", help="显示系统信息")

    # monitor命令
    monitor_parser = subparsers.add_parser("monitor", help="实时监控系统资源")
    monitor_parser.add_argument(
        "--interval", "-i",
        type=float,
        default=1.0,
        help="监控间隔（秒），默认1.0"
    )
    monitor_parser.add_argument(
        "--duration", "-d",
        type=float,
        default=0,
        help="监控持续时间（秒），0表示无限，默认0"
    )
    monitor_parser.add_argument(
        "--output", "-o",
        type=str,
        help="输出文件路径（支持.csv和.json格式）"
    )
    monitor_parser.add_argument(
        "--format", "-f",
        choices=["console", "csv", "json"],
        default="console",
        help="输出格式，默认console"
    )
    monitor_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，不显示实时输出"
    )
    monitor_parser.add_argument(
        "--top-processes",
        type=int,
        default=0,
        help="显示占用资源最多的进程数，默认0（不显示）"
    )

    # stats命令
    stats_parser = subparsers.add_parser("stats", help="显示统计信息")
    stats_parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="数据文件路径"
    )
    stats_parser.add_argument(
        "--summary",
        action="store_true",
        help="显示摘要统计"
    )

    return parser.parse_args()


def display_system_info():
    """显示系统信息"""
    monitor = SystemMonitor()
    system_info = monitor.get_system_info()

    print("=" * 60)
    print("系统信息摘要")
    print("=" * 60)

    # 平台信息
    platform_info = system_info["platform"]
    print(f"\n操作系统:")
    print(f"  系统: {platform_info['system']} {platform_info['release']}")
    print(f"  版本: {platform_info['version']}")
    print(f"  架构: {platform_info['machine']}")

    # CPU信息
    cpu_info = system_info["cpu_info"]
    print(f"\nCPU信息:")
    print(f"  逻辑核心: {cpu_info['logical_cores']}")
    print(f"  物理核心: {cpu_info['physical_cores']}")
    if cpu_info.get('model'):
        print(f"  型号: {cpu_info['model']}")

    # 内存信息
    mem_info = system_info["memory_info"]
    total_gb = mem_info["virtual"]["total"] / (1024 ** 3)
    print(f"\n内存信息:")
    print(f"  总内存: {total_gb:.2f} GB")

    # 磁盘信息
    disk_info = system_info["disk_info"]
    print(f"\n磁盘信息:")
    for disk in disk_info[:3]:  # 显示前3个分区
        total_gb = disk["total"] / (1024 ** 3)
        used_gb = disk["used"] / (1024 ** 3)
        print(f"  {disk['mountpoint']}: {used_gb:.1f}/{total_gb:.1f} GB ({disk['percent']:.1f}%)")

    # 启动时间
    boot_time = system_info["boot_time"]
    print(f"\n系统启动时间: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def monitor_command(args):
    """执行监控命令"""
    monitor = SystemMonitor()

    # 设置输出器
    exporters = []

    if args.format == "console" and not args.quiet:
        exporters.append(ConsoleExporter())

    if args.output:
        if args.output.endswith('.csv'):
            exporters.append(CSVExporter(args.output))
        elif args.output.endswith('.json'):
            exporters.append(JSONExporter(args.output))
        else:
            print(f"错误: 不支持的文件格式: {args.output}", file=sys.stderr)
            sys.exit(1)

    if not exporters:
        # 如果没有输出器，使用静默的JSON导出器
        exporters.append(JSONExporter("system_monitor_log.json"))

    print(f"开始监控，间隔: {args.interval}秒", file=sys.stderr)
    print("按 Ctrl+C 停止监控", file=sys.stderr)

    start_time = time.time()
    count = 0

    try:
        while True:
            # 检查持续时间
            if args.duration > 0 and (time.time() - start_time) > args.duration:
                break

            # 获取指标
            metrics = monitor.get_metrics()

            # 输出
            for exporter in exporters:
                if hasattr(exporter, 'export_single'):
                    exporter.export_single(metrics)

            count += 1

            # 等待
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(f"\n监控已停止，共收集 {count} 次数据", file=sys.stderr)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def stats_command(args):
    """显示统计信息"""
    if not args.file.endswith('.json'):
        print("错误: 目前只支持JSON格式的统计文件", file=sys.stderr)
        sys.exit(1)

    try:
        exporter = JSONExporter(args.file)
        data = exporter.load_data()

        if not data:
            print("错误: 没有找到数据", file=sys.stderr)
            sys.exit(1)

        if args.summary:
            print(f"数据记录数: {len(data)}")

            # CPU统计
            cpu_values = [item.get('cpu', {}).get('total_percent', 0) for item in data]
            if cpu_values:
                avg_cpu = sum(cpu_values) / len(cpu_values)
                max_cpu = max(cpu_values)
                print(f"CPU使用率: 平均 {avg_cpu:.1f}%, 最高 {max_cpu:.1f}%")

            # 内存统计
            mem_values = [item.get('memory', {}).get('percent', 0) for item in data]
            if mem_values:
                avg_mem = sum(mem_values) / len(mem_values)
                max_mem = max(mem_values)
                print(f"内存使用率: 平均 {avg_mem:.1f}%, 最高 {max_mem:.1f}%")

        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """主函数"""
    args = parse_args()

    if not args.command:
        # 默认显示帮助
        parse_args().print_help()
        sys.exit(0)

    try:
        if args.command == "info":
            display_system_info()
        elif args.command == "monitor":
            monitor_command(args)
        elif args.command == "stats":
            stats_command(args)
        else:
            print(f"未知命令: {args.command}", file=sys.stderr)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()