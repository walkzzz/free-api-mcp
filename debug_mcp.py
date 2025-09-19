#!/usr/bin/env python3
"""
调试MCP服务器启动
"""
import sys
import os
import traceback

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_mcp_startup():
    """调试MCP服务器启动过程"""
    try:
        print("🔍 开始调试MCP服务器启动...")
        
        # 1. 检查模块导入
        print("\n1. 检查模块导入...")
        try:
            from src.main import mcp
            print("✅ 主模块导入成功")
        except Exception as e:
            print(f"❌ 主模块导入失败: {e}")
            traceback.print_exc()
            return False
        
        # 2. 检查工具注册
        print("\n2. 检查工具注册...")
        try:
            import asyncio
            
            # 使用FastMCP的list_tools方法（异步）
            async def check_tools():
                tools_result = await mcp.list_tools()
                return tools_result
            
            tools_result = asyncio.run(check_tools())
            print(f"✅ list_tools() 调用成功")
            
            if hasattr(tools_result, 'tools'):
                tools = tools_result.tools
                print(f"✅ 已注册工具数量: {len(tools)}")
                
                if tools:
                    print("📋 已注册的工具:")
                    for tool in tools:
                        tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                        print(f"  - {tool_name}")
                else:
                    print("⚠️ 工具列表为空")
            else:
                print(f"工具结果类型: {type(tools_result)}")
                print(f"工具结果: {tools_result}")
                
        except Exception as e:
            print(f"❌ 工具注册检查失败: {e}")
            traceback.print_exc()
        
        # 3. 检查服务配置
        print("\n3. 检查服务配置...")
        try:
            from src.core.config import config_manager
            services = ["ip_location", "cryptocurrency", "quotes", "jokes", "exchange_rate", "news", "weather"]
            
            for service in services:
                config = config_manager.get_service_config(service)
                print(f"  - {service}: {config.name} ({'启用' if config.enabled else '禁用'})")
                
        except Exception as e:
            print(f"❌ 服务配置检查失败: {e}")
            traceback.print_exc()
        
        # 4. 测试简单工具调用
        print("\n4. 测试工具调用...")
        try:
            from src.main import health_check
            result = health_check()
            print(f"✅ 健康检查调用成功: {len(result)} 字符")
        except Exception as e:
            print(f"❌ 工具调用失败: {e}")
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ 调试过程失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = debug_mcp_startup()
    
    if success:
        print("\n🎉 MCP服务器调试完成")
        print("\n💡 建议:")
        print("1. 如果工具数量为0，检查@mcp.tool()装饰器是否正确")
        print("2. 如果导入失败，检查PYTHONPATH设置")
        print("3. 如果配置异常，检查环境变量设置")
        print("4. 尝试重启MCP服务器")
    else:
        print("\n⚠️ MCP服务器存在问题，请检查错误信息")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)