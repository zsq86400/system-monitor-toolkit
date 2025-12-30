"""
工具函数
"""

import platform
from typing import Optional, Dict, Any
from datetime import datetime


def format_bytes(bytes_num: float) -> str:
    """
    格式化字节数为可读格式

    Args:
        bytes_num: 字节数

    Returns:
        格式化后的字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"


def format_timestamp(timestamp: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化时间戳

    Args:
        timestamp: 时间戳
        format_str: 格式字符串

    Returns:
        格式化后的时间字符串
    """
    return timestamp.strftime(format_str)


def get_gpu_info() -> Optional[Dict[str, Any]]:
    """
    获取GPU信息（如果可用）

    Returns:
        GPU信息字典，如果不可用则返回None
    """
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()

        if not gpus:
            return None

        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load * 100,  # 转换为百分比
                "memory_used": gpu.memoryUsed,
                "memory_total": gpu.memoryTotal,
                "temperature": gpu.temperature,
                "driver": gpu.driver,
            })

        return {
            "count": len(gpus),
            "gpus": gpu_info
        }
    except ImportError:
        return None
    except Exception:
        return None


def is_windows() -> bool:
    """检查是否是Windows系统"""
    return platform.system() == "Windows"


def is_linux() -> bool:
    """检查是否是Linux系统"""
    return platform.system() == "Linux"


def is_mac() -> bool:
    """检查是否是macOS系统"""
    return platform.system() == "Darwin"


def get_platform_name() -> str:
    """获取平台名称"""
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "macOS"
    else:
        return system