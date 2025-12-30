"""
进程信息收集器
"""

import psutil
from typing import Dict, Any, List


class ProcessCollector:
    """进程信息收集器"""

    def get_top_processes(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取占用资源最多的进程"""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 按CPU使用率排序
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)

        return processes[:count]

    def get_process_count(self) -> int:
        """获取进程总数"""
        return len(list(psutil.process_iter()))

    def get_process_by_name(self, name: str) -> List[Dict[str, Any]]:
        """根据进程名查找进程"""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if name.lower() in proc.info['name'].lower():
                    processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def get_process_details(self, pid: int) -> Dict[str, Any]:
        """获取进程详细信息"""
        try:
            proc = psutil.Process(pid)

            with proc.oneshot():
                info = {
                    "pid": pid,
                    "name": proc.name(),
                    "status": proc.status(),
                    "cpu_percent": proc.cpu_percent(),
                    "memory_percent": proc.memory_percent(),
                    "memory_info": proc.memory_info()._asdict(),
                    "create_time": proc.create_time(),
                    "threads": proc.num_threads(),
                    "exe": proc.exe(),
                    "cmdline": proc.cmdline(),
                    "username": proc.username(),
                }

            return info
        except psutil.NoSuchProcess:
            return {"error": f"Process {pid} not found"}