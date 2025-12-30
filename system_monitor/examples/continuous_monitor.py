"""
持续监控并保存数据示例
"""

import json
from datetime import datetime

from system_monitor import SystemMonitor, ConsoleExporter


# from system_monitor import SystemMonitor, ConsoleExporter


class DataLogger:
    """数据记录器"""

    def __init__(self, filename="system_monitor_log.json"):
        self.filename = filename
        self.data = []

    def log_data(self, metrics):
        """记录数据"""
        metrics_dict = {
            "timestamp": metrics.timestamp.isoformat(),
            "cpu_percent": metrics.cpu_percent,
            "memory_percent": metrics.memory_percent,
            "disk_usage": metrics.disk_usage,
        }
        self.data.append(metrics_dict)

        # 每10条数据保存一次
        if len(self.data) % 10 == 0:
            self.save_to_file()

    def save_to_file(self):
        """保存到文件"""
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"\n数据已保存到 {self.filename}")


def main():
    # 创建监控器和数据记录器
    monitor = SystemMonitor()
    logger = DataLogger()

    # 同时注册多个回调
    monitor.register_callback(ConsoleExporter.export_single)
    monitor.register_callback(logger.log_data)

    print("开始系统监控，数据将实时显示并保存...")
    print("按Ctrl+C停止监控")

    try:
        # 直接运行监控循环
        monitor.start_monitoring(interval=0.01)

        # 主线程等待
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止监控...")
    finally:
        monitor.stop_monitoring()
        logger.save_to_file()


if __name__ == "__main__":
    main()