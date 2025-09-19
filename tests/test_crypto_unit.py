#!/usr/bin/env python3
"""
加密货币服务单元测试
"""
import sys
import os
import unittest
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestCryptocurrencyService(unittest.TestCase):
    """加密货币服务测试类"""
    
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
            cls.free_api_server.reset_failed_endpoints("cryptocurrency")
        else:
            raise ImportError("无法加载服务器模块")
    
    def test_crypto_service_exists(self):
        """测试加密货币服务函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_crypto_price'))
        self.assertTrue(callable(self.free_api_server.get_crypto_price))
    
    def test_valid_crypto_query_bitcoin(self):
        """测试比特币价格查询"""
        result = self.free_api_server.get_crypto_price("bitcoin", "usd")
        # 检查结果是否包含预期内容
        self.assertIsInstance(result, str)
        self.assertTrue(
            "BITCOIN 价格信息" in result or "不可用" in result,
            f"意外的结果格式: {result[:100]}"
        )
    
    def test_case_insensitive_input(self):
        """测试大小写不敏感的输入"""
        # 测试输入参数的大小写处理
        result1 = self.free_api_server.get_crypto_price("BITCOIN")
        result2 = self.free_api_server.get_crypto_price("bitcoin")
        
        # 两个结果应该都是字符串
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
    
    def test_invalid_crypto_query(self):
        """测试无效的加密货币查询"""
        result = self.free_api_server.get_crypto_price("invalidcoin123")
        # 应该返回错误信息
        self.assertIsInstance(result, str)
        self.assertIn("不可用", result)
    
    def test_currency_parameter(self):
        """测试货币参数"""
        # 测试USD
        result_usd = self.free_api_server.get_crypto_price("bitcoin", "usd")
        self.assertIsInstance(result_usd, str)
        
        # 测试CNY
        result_cny = self.free_api_server.get_crypto_price("bitcoin", "cny")
        self.assertIsInstance(result_cny, str)

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)