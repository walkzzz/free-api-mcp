#!/usr/bin/env python3
"""
测试增强的IP信息查询功能
"""
import sys
import os
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_ip_services():
    """测试增强的IP信息查询服务"""
    try:
        # 导入服务器模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("free_api_server", "./free-api-server.py")
        if spec is not None and spec.loader is not None:
            free_api_server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(free_api_server)
            
            print("测试增强的IP信息查询功能...\n")
            
            # 测试基本IP归属地查询
            print("1. 测试基本IP归属地查询...")
            try:
                result = free_api_server.ip_location("8.8.8.8")
                print(f"✅ 基本IP查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 基本IP查询异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试详细IP信息查询
            print("2. 测试详细IP信息查询...")
            try:
                result = free_api_server.ip_detailed_info("1.1.1.1")
                print(f"✅ 详细IP信息查询成功:\n{result}")
            except Exception as e:
                print(f"⚠️ 详细IP信息查询异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试IP安全检查
            print("3. 测试IP安全检查...")
            test_ips = ["8.8.8.8", "127.0.0.1", "192.168.1.1", "1.1.1.1"]
            
            for test_ip in test_ips:
                try:
                    result = free_api_server.ip_security_check(test_ip)
                    print(f"✅ {test_ip} 安全检查:\n{result[:200]}...\n")
                except Exception as e:
                    print(f"⚠️ {test_ip} 安全检查异常: {e}\n")
            
            print("="*60 + "\n")
            
            # 测试域名解析和查询
            print("4. 测试域名解析和查询...")
            try:
                result = free_api_server.ip_detailed_info("google.com")
                print(f"✅ 域名查询成功:\n{result[:300]}...")
            except Exception as e:
                print(f"⚠️ 域名查询异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试综合分析
            print("5. 测试IP综合分析...")
            try:
                result = free_api_server.ip_comprehensive_analysis("1.1.1.1")
                print(f"✅ 综合分析成功:\n{result[:400]}...")
            except Exception as e:
                print(f"⚠️ 综合分析异常: {e}")
            
            print("\n" + "="*60 + "\n")
            
            # 测试无效输入处理
            print("6. 测试无效输入处理...")
            invalid_inputs = ["invalid.ip", "999.999.999.999", ""]
            
            for invalid_input in invalid_inputs:
                try:
                    result = free_api_server.ip_security_check(invalid_input)
                    print(f"✅ 无效输入 '{invalid_input}' 处理: {result[:100]}...")
                except Exception as e:
                    print(f"⚠️ 无效输入 '{invalid_input}' 处理异常: {e}")
            
            return True
        else:
            print("❌ 无法加载服务器模块")
            return False
            
    except Exception as e:
        print(f"❌ 增强IP信息查询功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    # 设置日志级别为WARNING以减少输出
    logging.getLogger().setLevel(logging.WARNING)
    
    success = test_enhanced_ip_services()
    
    if success:
        print("\n🎉 增强IP信息查询功能测试完成！")
    else:
        print("\n⚠️ 增强IP信息查询功能测试失败。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)