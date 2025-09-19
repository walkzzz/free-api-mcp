#!/usr/bin/env python3
"""
重置并测试汇率查询服务
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主测试函数"""
    # 设置日志级别
    logging.getLogger().setLevel(logging.WARNING)
    
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("重置失败端点并测试汇率查询服务...\n")
            
            # 重置失败端点
            reset_result = free_api_server.reset_failed_endpoints("exchange_rate")
            print(f"重置结果: {reset_result}\n")
            
            # 测试多种货币对
            test_cases = [
                ("USD", "CNY", 100),
                ("EUR", "JPY", 50),
                ("GBP", "USD", 75),
                ("CNY", "EUR", 1000),
            ]
            
            for i, (from_curr, to_curr, amount) in enumerate(test_cases, 1):
                print(f"{i}. 测试 {from_curr} 到 {to_curr} 汇率查询...")
                try:
                    result = free_api_server.get_exchange_rate(from_curr, to_curr, amount)
                    print(f"✅ 成功:\n{result}")
                except Exception as e:
                    print(f"❌ 失败: {e}")
                print()
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)