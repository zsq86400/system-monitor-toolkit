"""
磁盘信息收集器
"""

import psutil
from typing import Dict, Any, List


class DiskCollector:
    """磁盘信息收集器"""

    def get_disk_usage(self, path: str = "/") -> float:
        """获取磁盘使用率"""
        return psutil.disk_usage(path).percent

    def get_all_disk_usage(self) -> Dict[str, float]:
        """获取所有磁盘分区的使用率"""
        partitions = psutil.disk_partitions()
        disk_usage = {}

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = usage.percent
            except Exception:
                continue

        return disk_usage

    def get_disk_io_counters(self) -> Dict[str, Any]:
        """获取磁盘IO统计"""
        counters = psutil.disk_io_counters()
        if counters:
            return {
                "read_count": counters.read_count,
                "write_count": counters.write_count,
                "read_bytes": counters.read_bytes,
                "write_bytes": counters.write_bytes,
                "read_time": counters.read_time,
                "write_time": counters.write_time,
            }
        return {}

    def get_disk_info(self) -> List[Dict[str, Any]]:
        """获取磁盘详细信息"""
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except Exception:
                continue

        return disk_info