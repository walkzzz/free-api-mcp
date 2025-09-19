#!/usr/bin/env python3
"""
测试加密货币价格查询服务
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_crypto_service():
    """测试加密货币服务"""
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试加密货币价格查询服务...\n")
            
            # 测试比特币价格查询
            print("1. 测试比特币价格查询（USD）...")
            try:
                result = free_api_server.get_crypto_price("bitcoin", "usd")
                print(f"✅ 比特币价格查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 比特币价格查询异常: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # 测试以太坊价格查询
            print("2. 测试以太坊价格查询（CNY）...")
            try:
                result = free_api_server.get_crypto_price("ethereum", "cny")
                print(f"✅ 以太坊价格查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 以太坊价格查询异常: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # 测试狗狗币价格查询
            print("3. 测试狗狗币价格查询...")
            try:
                result = free_api_server.get_crypto_price("dogecoin")
                print(f"✅ 狗狗币价格查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 狗狗币价格查询异常: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # 测试无效的加密货币
            print("4. 测试无效的加密货币...")
            try:
                result = free_api_server.get_crypto_price("invalidcoin")
                print(f"⚠️ 意外成功: {result}")
            except Exception as e:
                print(f"✅ 正确处理无效货币: {str(e)[:100]}...")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 加密货币服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为WARNING以减少输出
    logging.getLogger().setLevel(logging.WARNING)
    
    success = test_crypto_service()
    
    if success:
        print("\n🎉 加密货币服务测试完成！")
    else:
        print("\n⚠️ 加密货币服务测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)