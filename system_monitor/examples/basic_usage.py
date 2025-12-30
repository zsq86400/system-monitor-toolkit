"""
基本使用示例
"""

import time

from system_monitor import SystemMonitor, MonitorLevel, ConsoleExporter


def main():
    # 创建监控器
    monitor = SystemMonitor(level=MonitorLevel.STANDARD)

    # 获取系统信息
    print("正在获取系统信息...")
    system_info = monitor.get_system_info()
    ConsoleExporter.export_summary(system_info)

    # 获取当前指标
    print("\n正在获取当前系统指标...")
    metrics = monitor.get_metrics()
    ConsoleExporter.export_single(metrics)

    # 持续监控示例
    print("\n开始持续监控（按Ctrl+C停止）...")

    # 定义回调函数
    def monitor_callback(metrics):
        print(f"\rCPU: {metrics.cpu_percent:5.1f}% | "
              f"内存: {metrics.memory_percent:5.1f}% | "
              f"时间: {metrics.timestamp.strftime('%H:%M:%S')}", end="")

    # 注册回调并开始监控
    monitor.register_callback(monitor_callback)
    monitor.start_monitoring(interval=1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n监控已停止")
    finally:
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()