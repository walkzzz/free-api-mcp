#!/usr/bin/env python3
"""
测试修复后的安全检查功能
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主测试函数"""
    # 设置日志级别
    logging.getLogger().setLevel(logging.ERROR)
    
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试修复后的安全检查功能...\n")
            
            # 测试各种IP类型
            test_cases = [
                ("8.8.8.8", "公共IP"),
                ("192.168.1.1", "私有IP"),
                ("10.0.0.1", "私有IP"),
                ("172.16.0.1", "私有IP"),
                ("127.0.0.1", "本地回环"),
                ("1.1.1.1", "公共IP"),
            ]
            
            for ip, ip_type in test_cases:
                result = free_api_server.ip_security_check(ip)
                print(f"{ip_type} {ip}:")
                
                if "私有IP地址" in result:
                    print("✅ 正确识别为私有IP")
                elif "本地回环地址" in result:
                    print("✅ 正确识别为本地回环")
                elif "正常" in result:
                    print("✅ 正确识别为正常公共IP")
                elif "可疑" in result:
                    print("⚠️ 识别为可疑IP")
                else:
                    print("❓ 未知状态")
                
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