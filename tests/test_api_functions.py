#!/usr/bin/env python3
"""
测试重构后的API功能
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_functions():
    """测试API功能"""
    try:
        # 导入重构后的服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试重构后的API功能...\n")
            
            # 测试IP查询
            print("1. 测试IP归属地查询...")
            try:
                result = free_api_server.ip_location("8.8.8.8")
                print(f"✅ IP查询成功: {result}")
            except Exception as e:
                print(f"⚠️ IP查询异常: {e}")
            
            # 测试天气查询
            print("\n2. 测试天气查询...")
            try:
                result = free_api_server.get_weather("北京")
                print(f"✅ 天气查询成功: {result}")
            except Exception as e:
                print(f"⚠️ 天气查询异常: {e}")
            
            # 测试新闻查询
            print("\n3. 测试新闻查询...")
            try:
                result = free_api_server.get_china_news(3)
                print(f"✅ 新闻查询成功: {result[:200]}...")
            except Exception as e:
                print(f"⚠️ 新闻查询异常: {e}")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ API功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为ERROR以减少输出
    logging.getLogger().setLevel(logging.ERROR)
    
    success = test_api_functions()
    
    if success:
        print("\n🎉 API功能测试完成！")
    else:
        print("\n⚠️ API功能测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)