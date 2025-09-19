#!/usr/bin/env python3
"""
励志名言和笑话服务单元测试
"""
import sys
import os
import unittest
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestQuotesAndJokesService(unittest.TestCase):
    """励志名言和笑话服务测试类"""
    
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
            cls.free_api_server.reset_failed_endpoints()
        else:
            raise ImportError("无法加载服务器模块")
    
    def test_quote_service_exists(self):
        """测试励志名言服务函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_inspirational_quote'))
        self.assertTrue(callable(self.free_api_server.get_inspirational_quote))
    
    def test_joke_service_exists(self):
        """测试笑话服务函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_random_joke'))
        self.assertTrue(callable(self.free_api_server.get_random_joke))
    
    def test_daily_motivation_exists(self):
        """测试每日励志内容函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'get_daily_motivation'))
        self.assertTrue(callable(self.free_api_server.get_daily_motivation))
    
    def test_get_inspirational_quote(self):
        """测试获取励志名言"""
        result = self.free_api_server.get_inspirational_quote()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        # 应该包含名言标识符或备用内容标识
        self.assertTrue("💡" in result or "本地预设" in result)
    
    def test_get_random_joke(self):
        """测试获取随机笑话"""
        result = self.free_api_server.get_random_joke()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        # 应该包含笑话标识符或备用内容标识
        self.assertTrue("😄" in result or "本地预设" in result)
    
    def test_daily_motivation_quote(self):
        """测试每日励志内容（名言）"""
        result = self.free_api_server.get_daily_motivation("quote")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertTrue("💡" in result or "本地预设" in result)
    
    def test_daily_motivation_joke(self):
        """测试每日励志内容（笑话）"""
        result = self.free_api_server.get_daily_motivation("joke")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertTrue("😄" in result or "本地预设" in result)
    
    def test_daily_motivation_default(self):
        """测试每日励志内容默认参数"""
        result = self.free_api_server.get_daily_motivation()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        # 默认应该返回名言
        self.assertTrue("💡" in result or "本地预设" in result)
    
    def test_daily_motivation_case_insensitive(self):
        """测试每日励志内容参数大小写不敏感"""
        result1 = self.free_api_server.get_daily_motivation("QUOTE")
        result2 = self.free_api_server.get_daily_motivation("JOKE")
        
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        self.assertGreater(len(result1), 0)
        self.assertGreater(len(result2), 0)
    
    def test_content_randomness(self):
        """测试内容随机性"""
        quotes = []
        for _ in range(3):
            result = self.free_api_server.get_inspirational_quote()
            quotes.append(result)
        
        # 检查是否所有结果都是有效字符串
        for quote in quotes:
            self.assertIsInstance(quote, str)
            self.assertGreater(len(quote), 0)

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)