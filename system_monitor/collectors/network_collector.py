"""
网络信息收集器
"""

import psutil
import socket
from typing import Dict, Any, List


class NetworkCollector:
    """网络信息收集器"""

    def __init__(self):
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0

    def get_bytes_sent(self) -> float:
        """获取发送的字节数（MB）"""
        counters = psutil.net_io_counters()
        return counters.bytes_sent / (1024 ** 2)

    def get_bytes_recv(self) -> float:
        """获取接收的字节数（MB）"""
        counters = psutil.net_io_counters()
        return counters.bytes_recv / (1024 ** 2)

    def get_network_speed(self) -> Dict[str, float]:
        """获取网络速度"""
        current_counters = psutil.net_io_counters()

        sent_speed = current_counters.bytes_sent - self.last_bytes_sent
        recv_speed = current_counters.bytes_recv - self.last_bytes_recv

        self.last_bytes_sent = current_counters.bytes_sent
        self.last_bytes_recv = current_counters.bytes_recv

        return {
            "sent_speed": sent_speed,
            "recv_speed": recv_speed,
        }

    def get_connections_count(self, kind: str = 'all') -> int:
        """获取连接数"""
        return len(psutil.net_connections(kind=kind))

    def get_interface_info(self) -> Dict[str, Any]:
        """获取网络接口信息"""
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        interface_info = {}
        for interface, addrs in interfaces.items():
            interface_info[interface] = {
                "addresses": [
                    {
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask if hasattr(addr, 'netmask') else None,
                    }
                    for addr in addrs
                ],
                "stats": {
                    "isup": stats[interface].isup if interface in stats else False,
                    "speed": stats[interface].speed if interface in stats else 0,
                }
            }

        return interface_info

    def get_hostname(self) -> str:
        """获取主机名"""
        return socket.gethostname()