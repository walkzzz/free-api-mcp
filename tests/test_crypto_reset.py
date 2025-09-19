#!/usr/bin/env python3
"""
重置并测试加密货币服务
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
            
            print("重置失败端点并测试加密货币服务...\n")
            
            # 重置失败端点
            reset_result = free_api_server.reset_failed_endpoints("cryptocurrency")
            print(f"重置结果: {reset_result}\n")
            
            # 测试比特币价格查询
            print("测试比特币价格查询...")
            try:
                result = free_api_server.get_crypto_price("bitcoin", "usd")
                print(f"✅ 成功:\n{result}")
                return True
            except Exception as e:
                print(f"❌ 失败: {e}")
                return False
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)