"""
CPU信息收集器
"""

import psutil
import platform
from datetime import datetime
from typing import Dict, Any, List


class CPUCollector:
    """CPU信息收集器"""

    def __init__(self):
        self.cpu_count_logical = psutil.cpu_count()
        self.cpu_count_physical = psutil.cpu_count(logical=False)
        self.cpu_freq = psutil.cpu_freq()

    def get_cpu_percent(self, interval: float = 0.1) -> float:
        """获取CPU使用率"""
        return psutil.cpu_percent(interval=interval)

    def get_cpu_per_core(self) -> List[float]:
        """获取每个核心的使用率"""
        return psutil.cpu_percent(percpu=True)

    def get_cpu_frequency(self) -> Dict[str, float]:
        """获取CPU频率"""
        if self.cpu_freq:
            return {
                "current": self.cpu_freq.current,
                "min": self.cpu_freq.min,
                "max": self.cpu_freq.max
            }
        return {}

    def get_cpu_times(self) -> Dict[str, float]:
        """获取CPU时间信息"""
        times = psutil.cpu_times()
        return {
            "user": times.user,
            "system": times.system,
            "idle": times.idle,
            "nice": getattr(times, 'nice', 0),
            "iowait": getattr(times, 'iowait', 0),
            "irq": getattr(times, 'irq', 0),
            "softirq": getattr(times, 'softirq', 0),
            "steal": getattr(times, 'steal', 0),
        }

    def get_cpu_info(self) -> Dict[str, Any]:
        """获取CPU详细信息"""
        return {
            "logical_cores": self.cpu_count_logical,
            "physical_cores": self.cpu_count_physical,
            "frequency": self.get_cpu_frequency(),
            "model": platform.processor(),
            "architecture": platform.machine(),
        }

    def get_platform_info(self) -> Dict[str, str]:
        """获取平台信息"""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def get_boot_time(self) -> datetime:
        """获取系统启动时间"""
        return datetime.fromtimestamp(psutil.boot_time())