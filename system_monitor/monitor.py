"""
系统监控主模块
"""

import time
import threading
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from system_monitor.collectors import CPUCollector, MemoryCollector, DiskCollector, NetworkCollector, ProcessCollector


# from collectors import CPUCollector, MemoryCollector, DiskCollector, NetworkCollector, ProcessCollector


class MonitorLevel(Enum):
    """监控级别"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"


@dataclass
class SystemMetrics:
    """系统指标数据类"""
    timestamp: datetime
    cpu_percent: float
    cpu_per_core: List[float]
    memory_percent: float
    memory_used: float
    memory_total: float
    disk_usage: Dict[str, float]
    network_sent: float
    network_recv: float
    network_connections: int
    top_processes: List[Dict[str, Any]]


class SystemMonitor:
    """系统监控器"""

    def __init__(self, level: MonitorLevel = MonitorLevel.STANDARD):
        """
        初始化系统监控器

        Args:
            level: 监控级别
        """
        self.level = level
        self.running = False
        self.monitor_thread = None
        self.callbacks = []

        # 初始化收集器
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.disk_collector = DiskCollector()
        self.network_collector = NetworkCollector()
        self.process_collector = ProcessCollector()

    def get_metrics(self) -> SystemMetrics:
        """获取当前系统指标"""
        metrics = SystemMetrics(
            timestamp=datetime.now(),
            cpu_percent=self.cpu_collector.get_cpu_percent(),
            cpu_per_core=self.cpu_collector.get_cpu_per_core(),
            memory_percent=self.memory_collector.get_memory_percent(),
            memory_used=self.memory_collector.get_memory_used(),
            memory_total=self.memory_collector.get_memory_total(),
            disk_usage=self.disk_collector.get_all_disk_usage(),
            network_sent=self.network_collector.get_bytes_sent(),
            network_recv=self.network_collector.get_bytes_recv(),
            network_connections=self.network_collector.get_connections_count(),
            top_processes=self.process_collector.get_top_processes(5)
        )

        return metrics

    def start_monitoring(self, interval: float = 1.0):
        """
        开始持续监控

        Args:
            interval: 监控间隔（秒）
        """
        if self.running:
            return

        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def _monitor_loop(self, interval: float):
        """监控循环"""
        while self.running:
            metrics = self.get_metrics()

            # 调用所有回调函数
            for callback in self.callbacks:
                try:
                    callback(metrics)
                except Exception as e:
                    print(f"Callback error: {e}")

            time.sleep(interval)

    def register_callback(self, callback: Callable[[SystemMetrics], None]):
        """注册回调函数"""
        self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[SystemMetrics], None]):
        """注销回调函数"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "platform": self.cpu_collector.get_platform_info(),
            "cpu_info": self.cpu_collector.get_cpu_info(),
            "memory_info": self.memory_collector.get_memory_info(),
            "disk_info": self.disk_collector.get_disk_info(),
            "boot_time": self.cpu_collector.get_boot_time()
        }
# 主要监控类
