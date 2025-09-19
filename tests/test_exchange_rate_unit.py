#!/usr/bin/env python3
"""
汇率查询服务单元测试
"""
import sys
import os
import unittest
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestExchangeRateService(unittest.TestCase):
    """汇率查询服务测试类"""
    
    @classmethod
    def setUpClass(cls):
        """类级别的设置"""
        # 设置日志级别以减少输出
        logging.getLogger().setLevel(logging.ERROR)
        
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            cls.free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.free_api_server)
            
            # 重置失败端点
            cls.free_api_server.reset_failed_endpoints("exchange_rate")
        else:
            raise ImportError("无法加载服务器模块")
    
    def test_exchange_rate_service_exists(self):
        """测试汇率查询服务函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_exchange_rate'))
        self.assertTrue(callable(self.free_api_server.get_exchange_rate))
    
    def test_supported_currencies_exists(self):
        """测试支持货币列表函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_supported_currencies'))
        self.assertTrue(callable(self.free_api_server.get_supported_currencies))
    
    def test_valid_currency_conversion(self):
        """测试有效的货币转换"""
        result = self.free_api_server.get_exchange_rate("USD", "CNY", 100)
        self.assertIsInstance(result, str)
        self.assertIn("💱", result)
        self.assertIn("USD", result)
        self.assertIn("CNY", result)
    
    def test_same_currency_conversion(self):
        """测试相同货币转换"""
        result = self.free_api_server.get_exchange_rate("USD", "USD", 50)
        self.assertIsInstance(result, str)
        self.assertIn("50 USD = 50 USD", result)
        self.assertIn("相同货币", result)
    
    def test_invalid_source_currency(self):
        """测试无效的源货币代码"""
        result = self.free_api_server.get_exchange_rate("INVALID", "USD")
        self.assertIsInstance(result, str)
        self.assertIn("不支持的源货币代码", result)
        self.assertIn("INVALID", result)
    
    def test_invalid_target_currency(self):
        """测试无效的目标货币代码"""
        result = self.free_api_server.get_exchange_rate("USD", "INVALID")
        self.assertIsInstance(result, str)
        self.assertIn("不支持的目标货币代码", result)
        self.assertIn("INVALID", result)
    
    def test_case_insensitive_input(self):
        """测试大小写不敏感的输入"""
        result1 = self.free_api_server.get_exchange_rate("usd", "cny", 10)
        result2 = self.free_api_server.get_exchange_rate("USD", "CNY", 10)
        
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        # 两个结果应该包含相同的货币信息
        self.assertIn("USD", result1)
        self.assertIn("CNY", result1)
        self.assertIn("USD", result2)
        self.assertIn("CNY", result2)
    
    def test_default_amount(self):
        """测试默认金额（1.0）"""
        result = self.free_api_server.get_exchange_rate("USD", "EUR")
        self.assertIsInstance(result, str)
        self.assertIn("1 USD", result)
    
    def test_custom_amount(self):
        """测试自定义金额"""
        result = self.free_api_server.get_exchange_rate("EUR", "GBP", 250)
        self.assertIsInstance(result, str)
        self.assertIn("250 EUR", result)
    
    def test_supported_currencies_list(self):
        """测试支持的货币列表"""
        result = self.free_api_server.get_supported_currencies()
        self.assertIsInstance(result, str)
        self.assertIn("支持的货币代码", result)
        self.assertIn("USD - 美元", result)
        self.assertIn("CNY - 人民币", result)
        self.assertIn("EUR - 欧元", result)
        self.assertIn("使用示例", result)
    
    def test_multiple_currency_pairs(self):
        """测试多种货币对"""
        test_pairs = [
            ("USD", "CNY"),
            ("EUR", "JPY"),
            ("GBP", "USD"),
            ("CNY", "EUR")
        ]
        
        for from_curr, to_curr in test_pairs:
            with self.subTest(from_currency=from_curr, to_currency=to_curr):
                result = self.free_api_server.get_exchange_rate(from_curr, to_curr)
                self.assertIsInstance(result, str)
                self.assertIn(from_curr, result)
                self.assertIn(to_curr, result)

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)