"""
控制台输出器
"""

from tabulate import tabulate
from datetime import datetime
from typing import Dict, Any

from system_monitor import SystemMetrics


class ConsoleExporter:
    """控制台输出器"""

    @staticmethod
    def export_single(metrics: SystemMetrics):
        """导出单次监控数据"""
        print(f"\n{'='*50}")
        print(f"系统监控报告 - {metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")

        # CPU信息
        print(f"\n📊 CPU使用率: {metrics.cpu_percent:.1f}%")
        print(f"   核心使用率: {', '.join([f'{p:.1f}%' for p in metrics.cpu_per_core])}")
        #
        # 内存信息
        print(f"\n💾 内存使用: {metrics.memory_percent:.1f}%")
        print(f"   已用/总量: {metrics.memory_used:.2f}GB / {metrics.memory_total:.2f}GB")

        # 磁盘信息
        print(f"\n💽 磁盘使用:")
        for mount, percent in metrics.disk_usage.items():
            print(f"   {mount}: {percent:.1f}%")

        # 网络信息
        print(f"\n🌐 网络传输:")
        print(f"   发送: {metrics.network_sent:.2f}MB")
        print(f"   接收: {metrics.network_recv:.2f}MB")
        print(f"   连接数: {metrics.network_connections}")

        # 进程信息
        if metrics.top_processes:
            print(f"\n📋 占用资源最多的进程:")
            headers = ["PID", "名称", "CPU%", "内存%"]
            rows = []
            for proc in metrics.top_processes[:5]:
                rows.append([
                    proc.get('pid', 'N/A'),
                    proc.get('name', 'N/A')[:20],
                    f"{proc.get('cpu_percent', 0):.1f}",
                    f"{proc.get('memory_percent', 0):.1f}"
                ])
            print(tabulate(rows, headers=headers, tablefmt="simple"))

    @staticmethod
    def export_summary(system_info: Dict[str, Any]):
        """导出系统信息摘要"""
        print(f"\n{'='*50}")
        print("系统信息摘要")
        print(f"{'='*50}")

        # 平台信息
        print(f"\n🖥️  系统平台:")
        print(f"   操作系统: {system_info['platform']['system']} {system_info['platform']['release']}")
        print(f"   架构: {system_info['platform']['machine']}")

        # CPU信息
        print(f"\n⚡ CPU信息:")
        cpu_info = system_info['cpu_info']
        print(f"   处理器: {cpu_info['model']}")
        print(f"   逻辑核心: {cpu_info['logical_cores']}")
        print(f"   物理核心: {cpu_info['physical_cores']}")

        # 内存信息
        print(f"\n💾 内存信息:")
        mem_info = system_info['memory_info']['virtual']
        total_gb = mem_info['total'] / (1024**3)
        print(f"   总内存: {total_gb:.2f} GB")

        # 磁盘信息
        print(f"\n💽 磁盘信息:")
        for disk in system_info['disk_info'][:3]:  # 显示前3个分区
            total_gb = disk['total'] / (1024**3)
            print(f"   {disk['mountpoint']}: {total_gb:.2f} GB ({disk['fstype']})")