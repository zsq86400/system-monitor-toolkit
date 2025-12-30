"""
监控器测试
"""

import unittest
import time
from unittest.mock import patch, MagicMock
from system_monitor import SystemMonitor, MonitorLevel


class TestSystemMonitor(unittest.TestCase):
    """系统监控器测试"""

    def setUp(self):
        """测试前准备"""
        self.monitor = SystemMonitor(level=MonitorLevel.BASIC)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.monitor.level, MonitorLevel.BASIC)
        self.assertFalse(self.monitor.running)
        self.assertIsNone(self.monitor.monitor_thread)
        self.assertEqual(self.monitor.callbacks, [])

    def test_get_metrics(self):
        """测试获取指标"""
        metrics = self.monitor.get_metrics()

        # 检查指标是否存在
        self.assertIsNotNone(metrics.timestamp)
        self.assertIsInstance(metrics.cpu_percent, float)
        self.assertIsInstance(metrics.memory_percent, float)
        self.assertIsInstance(metrics.disk_usage, dict)

        # 检查值范围
        self.assertGreaterEqual(metrics.cpu_percent, 0)
        self.assertLessEqual(metrics.cpu_percent, 100)
        self.assertGreaterEqual(metrics.memory_percent, 0)
        self.assertLessEqual(metrics.memory_percent, 100)

    def test_get_system_info(self):
        """测试获取系统信息"""
        system_info = self.monitor.get_system_info()

        self.assertIn("platform", system_info)
        self.assertIn("cpu_info", system_info)
        self.assertIn("memory_info", system_info)
        self.assertIn("disk_info", system_info)
        self.assertIn("boot_time", system_info)

    @patch('threading.Thread')
    def test_start_stop_monitoring(self, mock_thread):
        """测试开始和停止监控"""
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # 测试开始监控
        self.monitor.start_monitoring(interval=0.1)
        self.assertTrue(self.monitor.running)
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()

        # 测试停止监控
        self.monitor.stop_monitoring()
        self.assertFalse(self.monitor.running)

    def test_callback_registration(self):
        """测试回调函数注册"""

        def dummy_callback(metrics):
            pass

        # 注册回调
        self.monitor.register_callback(dummy_callback)
        self.assertIn(dummy_callback, self.monitor.callbacks)
        self.assertEqual(len(self.monitor.callbacks), 1)

        # 注销回调
        self.monitor.unregister_callback(dummy_callback)
        self.assertNotIn(dummy_callback, self.monitor.callbacks)
        self.assertEqual(len(self.monitor.callbacks), 0)


class TestMonitorLevel(unittest.TestCase):
    """监控级别测试"""

    def test_level_values(self):
        """测试监控级别值"""
        self.assertEqual(MonitorLevel.BASIC.value, "basic")
        self.assertEqual(MonitorLevel.STANDARD.value, "standard")
        self.assertEqual(MonitorLevel.ADVANCED.value, "advanced")


if __name__ == "__main__":
    unittest.main()