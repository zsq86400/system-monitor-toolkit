"""
JSON文件导出器
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from system_monitor import SystemMetrics


class JSONExporter:
    """JSON文件导出器"""

    def __init__(self, filename: str = "system_metrics.json"):
        """
        初始化JSON导出器

        Args:
            filename: JSON文件名
        """
        self.filename = filename
        self.filepath = Path(filename)

        # 初始化文件
        if not self.filepath.exists():
            self._init_file()

    def _init_file(self):
        """初始化JSON文件"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump({"version": "1.0", "metrics": []}, f, indent=2)

    def export_single(self, metrics: SystemMetrics):
        """导出单次监控数据"""
        # 读取现有数据
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"version": "1.0", "metrics": []}

        # 转换为字典格式
        metrics_dict = {
            "timestamp": metrics.timestamp.isoformat(),
            "cpu": {
                "total_percent": metrics.cpu_percent,
                "per_core": metrics.cpu_per_core,
            },
            "memory": {
                "percent": metrics.memory_percent,
                "used_gb": metrics.memory_used,
                "total_gb": metrics.memory_total,
            },
            "disk": metrics.disk_usage,
            "network": {
                "sent_mb": metrics.network_sent,
                "recv_mb": metrics.network_recv,
                "connections": metrics.network_connections,
            },
            "processes": metrics.top_processes[:3]  # 只保存前3个进程
        }

        # 添加新数据
        data["metrics"].append(metrics_dict)

        # 保持最近的100条记录
        if len(data["metrics"]) > 100:
            data["metrics"] = data["metrics"][-100:]

        # 写回文件
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

    def export_batch(self, metrics_list: List[SystemMetrics]):
        """批量导出监控数据"""
        for metrics in metrics_list:
            self.export_single(metrics)

    def load_data(self) -> List[Dict[str, Any]]:
        """加载已保存的数据"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("metrics", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []