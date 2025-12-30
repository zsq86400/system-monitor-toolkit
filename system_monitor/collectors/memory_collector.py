"""
内存信息收集器
"""

import psutil
from typing import Dict, Any


class MemoryCollector:
    """内存信息收集器"""

    def get_memory_percent(self) -> float:
        """获取内存使用百分比"""
        return psutil.virtual_memory().percent

    def get_memory_used(self) -> float:
        """获取已用内存（GB）"""
        return psutil.virtual_memory().used / (1024 ** 3)

    def get_memory_total(self) -> float:
        """获取总内存（GB）"""
        return psutil.virtual_memory().total / (1024 ** 3)

    def get_memory_available(self) -> float:
        """获取可用内存（GB）"""
        return psutil.virtual_memory().available / (1024 ** 3)

    def get_swap_percent(self) -> float:
        """获取交换空间使用百分比"""
        return psutil.swap_memory().percent

    def get_memory_info(self) -> Dict[str, Any]:
        """获取内存详细信息"""
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "virtual": {
                "total": virtual.total,
                "available": virtual.available,
                "percent": virtual.percent,
                "used": virtual.used,
                "free": virtual.free,
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
            }
        }