"""
系统监控工具包
"""

__version__ = "1.0.0"
__author__ = "System Monitor Team"
__license__ = "MIT"

from .monitor import SystemMonitor, MonitorLevel, SystemMetrics
from .exporters.console_exporter import ConsoleExporter

# 导出主要类
__all__ = [
    "SystemMonitor",
    "MonitorLevel",
    "SystemMetrics",
    "ConsoleExporter",
]

# 尝试导入可选模块
try:
    from .exporters.csv_exporter import CSVExporter
    from .exporters.json_exporter import JSONExporter
    __all__.extend(["CSVExporter", "JSONExporter"])
except ImportError:
    pass

try:
    from .utils.helpers import get_gpu_info
    __all__.append("get_gpu_info")
except ImportError:
    pass