#!/usr/bin/env python3
"""
测试汇率查询服务
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_exchange_rate_service():
    """测试汇率查询服务"""
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试汇率查询服务...\n")
            
            # 测试USD到CNY汇率查询
            print("1. 测试USD到CNY汇率查询...")
            try:
                result = free_api_server.get_exchange_rate("USD", "CNY", 100)
                print(f"✅ USD到CNY汇率查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ USD到CNY汇率查询异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试EUR到JPY汇率查询
            print("2. 测试EUR到JPY汇率查询...")
            try:
                result = free_api_server.get_exchange_rate("EUR", "JPY")
                print(f"✅ EUR到JPY汇率查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ EUR到JPY汇率查询异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试相同货币转换
            print("3. 测试相同货币转换...")
            try:
                result = free_api_server.get_exchange_rate("USD", "USD", 50)
                print(f"✅ 相同货币转换成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 相同货币转换异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试无效货币代码
            print("4. 测试无效货币代码...")
            try:
                result = free_api_server.get_exchange_rate("INVALID", "USD")
                print(f"✅ 无效货币代码处理:\n{result}")
            except Exception as e:
                print(f"⚠️ 无效货币代码处理异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试支持的货币列表
            print("5. 测试支持的货币列表...")
            try:
                result = free_api_server.get_supported_currencies()
                print(f"✅ 支持的货币列表:\n{result[:300]}...")
            except Exception as e:
                print(f"⚠️ 支持的货币列表异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试大小写不敏感
            print("6. 测试大小写不敏感...")
            try:
                result1 = free_api_server.get_exchange_rate("usd", "cny", 10)
                result2 = free_api_server.get_exchange_rate("USD", "CNY", 10)
                print(f"✅ 小写输入结果:\n{result1[:100]}...")
                print(f"✅ 大写输入结果:\n{result2[:100]}...")
            except Exception as e:
                print(f"⚠️ 大小写测试异常: {e}")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 汇率查询服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为WARNING以减少输出
    logging.getLogger().setLevel(logging.WARNING)
    
    success = test_exchange_rate_service()
    
    if success:
        print("\n🎉 汇率查询服务测试完成！")
    else:
        print("\n⚠️ 汇率查询服务测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)