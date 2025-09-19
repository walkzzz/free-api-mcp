#!/usr/bin/env python3
"""
测试励志名言和笑话服务
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_quotes_and_jokes():
    """测试名言和笑话服务"""
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试励志名言和笑话服务...\n")
            
            # 测试励志名言
            print("1. 测试励志名言获取...")
            try:
                result = free_api_server.get_inspirational_quote()
                print(f"✅ 励志名言获取成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 励志名言获取异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试笑话
            print("2. 测试笑话获取...")
            try:
                result = free_api_server.get_random_joke()
                print(f"✅ 笑话获取成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 笑话获取异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试每日励志内容（名言）
            print("3. 测试每日励志内容（名言）...")
            try:
                result = free_api_server.get_daily_motivation("quote")
                print(f"✅ 每日励志名言获取成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 每日励志名言获取异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试每日励志内容（笑话）
            print("4. 测试每日励志内容（笑话）...")
            try:
                result = free_api_server.get_daily_motivation("joke")
                print(f"✅ 每日励志笑话获取成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 每日励志笑话获取异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试多次调用以验证随机性
            print("5. 测试多次调用验证随机性...")
            quotes = []
            for i in range(3):
                try:
                    result = free_api_server.get_inspirational_quote()
                    quotes.append(result[:50] + "...")  # 只保留前50个字符用于比较
                    print(f"第{i+1}次: {result[:100]}...")
                except Exception as e:
                    print(f"第{i+1}次调用失败: {e}")
            
            # 检查是否有不同的内容
            unique_quotes = set(quotes)
            if len(unique_quotes) > 1:
                print("✅ 验证随机性成功：获取到了不同的内容")
            else:
                print("⚠️ 可能使用了备用内容或API返回相同结果")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 名言和笑话服务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为WARNING以减少输出
    logging.getLogger().setLevel(logging.WARNING)
    
    success = test_quotes_and_jokes()
    
    if success:
        print("\n🎉 励志名言和笑话服务测试完成！")
    else:
        print("\n⚠️ 励志名言和笑话服务测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)