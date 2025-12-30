"""
CSV文件导出器
"""

import csv
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from system_monitor import SystemMetrics


class CSVExporter:
    """CSV文件导出器"""

    def __init__(self, filename: str = "system_metrics.csv"):
        """
        初始化CSV导出器

        Args:
            filename: CSV文件名
        """
        self.filename = filename
        self.filepath = Path(filename)

        # 初始化文件，写入表头
        if not self.filepath.exists():
            self._write_header()

    def _write_header(self):
        """写入CSV表头"""
        headers = [
            'timestamp',
            'cpu_percent',
            'memory_percent',
            'memory_used_gb',
            'memory_total_gb',
            'disk_usage_root',
            'network_sent_mb',
            'network_recv_mb',
            'network_connections',
        ]

        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def export_single(self, metrics: SystemMetrics):
        """导出单次监控数据"""
        # 获取根目录的磁盘使用率
        disk_root = metrics.disk_usage.get('/', 0.0) if metrics.disk_usage else 0.0

        row = [
            metrics.timestamp.isoformat(),
            f"{metrics.cpu_percent:.2f}",
            f"{metrics.memory_percent:.2f}",
            f"{metrics.memory_used:.2f}",
            f"{metrics.memory_total:.2f}",
            f"{disk_root:.2f}",
            f"{metrics.network_sent:.2f}",
            f"{metrics.network_recv:.2f}",
            metrics.network_connections,
        ]

        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def export_batch(self, metrics_list: List[SystemMetrics]):
        """批量导出监控数据"""
        for metrics in metrics_list:
            self.export_single(metrics)