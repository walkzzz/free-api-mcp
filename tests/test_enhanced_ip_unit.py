#!/usr/bin/env python3
"""
增强IP信息查询服务单元测试
"""
import sys
import os
import unittest
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestEnhancedIPService(unittest.TestCase):
    """增强IP信息查询服务测试类"""
    
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
            cls.free_api_server.reset_failed_endpoints("ip_location")
        else:
            raise ImportError("无法加载服务器模块")
    
    def test_ip_location_exists(self):
        """测试基本IP归属地查询函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'ip_location'))
        self.assertTrue(callable(self.free_api_server.ip_location))
    
    def test_ip_detailed_info_exists(self):
        """测试详细IP信息查询函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'ip_detailed_info'))
        self.assertTrue(callable(self.free_api_server.ip_detailed_info))
    
    def test_ip_security_check_exists(self):
        """测试IP安全检查函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'ip_security_check'))
        self.assertTrue(callable(self.free_api_server.ip_security_check))
    
    def test_ip_comprehensive_analysis_exists(self):
        """测试IP综合分析函数存在"""
        self.assertTrue(hasattr(self.free_api_server, 'ip_comprehensive_analysis'))
        self.assertTrue(callable(self.free_api_server.ip_comprehensive_analysis))
    
    def test_basic_ip_location(self):
        """测试基本IP归属地查询"""
        result = self.free_api_server.ip_location("8.8.8.8")
        self.assertIsInstance(result, str)
        self.assertIn("8.8.8.8", result)
    
    def test_detailed_ip_info(self):
        """测试详细IP信息查询"""
        result = self.free_api_server.ip_detailed_info("1.1.1.1")
        self.assertIsInstance(result, str)
        self.assertIn("🌍", result)
        self.assertIn("1.1.1.1", result)
    
    def test_security_check_public_ip(self):
        """测试公共IP安全检查"""
        result = self.free_api_server.ip_security_check("8.8.8.8")
        self.assertIsInstance(result, str)
        self.assertIn("🔒", result)
        self.assertIn("8.8.8.8", result)
        self.assertIn("威胁状态", result)
    
    def test_security_check_private_ip(self):
        """测试私有IP安全检查"""
        result = self.free_api_server.ip_security_check("192.168.1.1")
        self.assertIsInstance(result, str)
        self.assertIn("私有IP地址", result)
        self.assertIn("正常", result)
    
    def test_security_check_localhost(self):
        """测试本地回环地址安全检查"""
        result = self.free_api_server.ip_security_check("127.0.0.1")
        self.assertIsInstance(result, str)
        self.assertIn("本地回环地址", result)
        self.assertIn("正常", result)
    
    def test_security_check_invalid_ip(self):
        """测试无效IP地址安全检查"""
        result = self.free_api_server.ip_security_check("999.999.999.999")
        self.assertIsInstance(result, str)
        self.assertIn("无效的IP地址", result)
    
    def test_comprehensive_analysis(self):
        """测试IP综合分析"""
        result = self.free_api_server.ip_comprehensive_analysis("1.1.1.1")
        self.assertIsInstance(result, str)
        self.assertIn("🔍", result)
        self.assertIn("综合分析报告", result)
        self.assertIn("1.1.1.1", result)
    
    def test_domain_resolution(self):
        """测试域名解析"""
        result = self.free_api_server.ip_detailed_info("google.com")
        self.assertIsInstance(result, str)
        self.assertIn("google.com", result)
    
    def test_various_ip_formats(self):
        """测试各种IP格式"""
        test_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
        
        for ip in test_ips:
            with self.subTest(ip=ip):
                result = self.free_api_server.ip_security_check(ip)
                self.assertIsInstance(result, str)
                self.assertIn(ip, result)

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)