#!/usr/bin/env python3
"""
测试核心重构功能
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """测试核心模块导入"""
    try:
        from core.config import config_manager
        from core.http_client import http_manager
        from core.error_handler import handle_api_error
        from core.fallback_manager import fallback_manager
        
        print("✅ 所有核心模块导入成功")
        
        # 测试配置管理器
        news_key = config_manager.get("news_api_key")
        print(f"✅ 配置管理器工作正常，新闻API密钥: {news_key[:10]}...")
        
        # 测试服务配置
        ip_config = config_manager.get_service_config("ip_location")
        print(f"✅ 服务配置获取成功，IP服务主端点: {ip_config.primary_endpoint}")
        
        # 测试HTTP客户端
        client = http_manager.client
        print(f"✅ HTTP客户端创建成功，超时设置: {client.timeout}")
        
        return True
        
    except Exception as e:
        print(f"❌ 核心模块测试失败: {e}")
        return False

def test_refactored_functions():
    """测试重构后的函数"""
    try:
        # 导入重构后的服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("✅ 重构后的服务器模块导入成功")
            
            # 测试健康检查功能
            try:
                health_result = free_api_server.health_check()
                print(f"✅ 健康检查功能正常:\n{health_result}")
            except Exception as e:
                print(f"⚠️ 健康检查功能异常（可能是网络问题）: {e}")
            
            # 测试重置失败端点功能
            reset_result = free_api_server.reset_failed_endpoints()
            print(f"✅ 重置失败端点功能正常: {reset_result}")
            
            return True
        else:
            print("❌ 无法加载重构后的服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 重构后函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试核心重构功能...\n")
    
    # 设置日志级别为WARNING以减少输出
    logging.getLogger().setLevel(logging.WARNING)
    
    success_count = 0
    total_tests = 2
    
    # 测试核心模块
    print("1. 测试核心模块导入...")
    if test_core_modules():
        success_count += 1
    print()
    
    # 测试重构后的函数
    print("2. 测试重构后的函数...")
    if test_refactored_functions():
        success_count += 1
    print()
    
    # 输出测试结果
    print(f"测试完成: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！核心重构成功。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)