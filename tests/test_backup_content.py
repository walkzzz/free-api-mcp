#!/usr/bin/env python3
"""
测试备用内容功能
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backup_content():
    """测试备用内容功能"""
    try:
        # 导入核心模块
        from core.fallback_manager import fallback_manager
        from core.config import config_manager
        
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试备用内容功能...\n")
            
            # 手动标记所有名言API端点为失败状态
            quotes_config = config_manager.get_service_config("quotes")
            all_quote_endpoints = [quotes_config.primary_endpoint] + quotes_config.fallback_endpoints
            
            for endpoint in all_quote_endpoints:
                fallback_manager.failed_endpoints.add(endpoint)
            
            print("已标记所有名言API端点为失败状态")
            print(f"失败端点: {fallback_manager.get_failed_endpoints()}")
            
            # 测试励志名言（应该使用备用内容）
            print("\n1. 测试励志名言（应该使用备用内容）...")
            try:
                result = free_api_server.get_inspirational_quote()
                print(f"✅ 励志名言获取成功（备用内容）:\n{result}")
                
                # 验证是否是备用内容
                if "本地预设名言库" in result:
                    print("✅ 确认使用了本地备用内容")
                else:
                    print("⚠️ 可能仍在使用API内容")
                    
            except Exception as e:
                print(f"❌ 励志名言获取失败: {e}")
            
            # 手动标记所有笑话API端点为失败状态
            jokes_config = config_manager.get_service_config("jokes")
            all_joke_endpoints = [jokes_config.primary_endpoint] + jokes_config.fallback_endpoints
            
            for endpoint in all_joke_endpoints:
                fallback_manager.failed_endpoints.add(endpoint)
            
            print(f"\n已标记所有笑话API端点为失败状态")
            
            # 测试笑话（应该使用备用内容）
            print("\n2. 测试笑话（应该使用备用内容）...")
            try:
                result = free_api_server.get_random_joke()
                print(f"✅ 笑话获取成功（备用内容）:\n{result}")
                
                # 验证是否是备用内容
                if "本地预设笑话库" in result:
                    print("✅ 确认使用了本地备用内容")
                else:
                    print("⚠️ 可能仍在使用API内容")
                    
            except Exception as e:
                print(f"❌ 笑话获取失败: {e}")
            
            # 测试多次调用备用内容的随机性
            print("\n3. 测试备用内容的随机性...")
            backup_quotes = []
            for i in range(3):
                try:
                    result = free_api_server.get_inspirational_quote()
                    backup_quotes.append(result)
                    print(f"第{i+1}次: {result.split('——')[0][:50]}...")
                except Exception as e:
                    print(f"第{i+1}次调用失败: {e}")
            
            # 检查随机性
            unique_backup_quotes = set(backup_quotes)
            if len(unique_backup_quotes) > 1:
                print("✅ 备用内容随机性验证成功")
            else:
                print("⚠️ 备用内容可能不够随机")
            
            # 重置失败端点
            print("\n4. 重置失败端点...")
            fallback_manager.reset_failed_endpoints()
            print("✅ 已重置所有失败端点")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 备用内容测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为ERROR以减少输出
    logging.getLogger().setLevel(logging.ERROR)
    
    success = test_backup_content()
    
    if success:
        print("\n🎉 备用内容功能测试完成！")
    else:
        print("\n⚠️ 备用内容功能测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)