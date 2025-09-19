"""
Free API MCP Server - 主入口文件
"""
from mcp.server.fastmcp import FastMCP
import pinyin
import logging

# 导入核心模块
try:
    # 尝试相对导入（当作为模块运行时）
    from .core.config import config_manager
    from .core.http_client import http_manager
    from .core.error_handler import handle_api_error
    from .core.fallback_manager import fallback_manager
    
    # 导入服务模块
    from .services.ip_service import (
        ip_location, ip_detailed_info, ip_security_check, ip_comprehensive_analysis
    )
    from .services.crypto_service import get_crypto_price
    from .services.content_service import (
        get_inspirational_quote, get_random_joke, get_daily_motivation
    )
    from .services.exchange_service import get_exchange_rate, get_supported_currencies
except ImportError:
    # 回退到绝对导入（当直接导入时）
    from src.core.config import config_manager
    from src.core.http_client import http_manager
    from src.core.error_handler import handle_api_error
    from src.core.fallback_manager import fallback_manager
    
    # 导入服务模块
    from src.services.ip_service import (
        ip_location, ip_detailed_info, ip_security_check, ip_comprehensive_analysis
    )
    from src.services.crypto_service import get_crypto_price
    from src.services.content_service import (
        get_inspirational_quote, get_random_joke, get_daily_motivation
    )
    from src.services.exchange_service import get_exchange_rate, get_supported_currencies

# 初始化MCP服务器
mcp = FastMCP("free-api-server")
logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# IP 信息查询服务
# ----------------------------------------------------------
@mcp.tool()
def query_ip_location(ip_or_domain: str) -> str:
    """查询IP地址或域名的基本归属地信息"""
    return ip_location(ip_or_domain)

@mcp.tool()
def query_ip_detailed_info(ip_or_domain: str) -> str:
    """查询IP地址或域名的详细信息，包括地理位置、ISP、时区等"""
    return ip_detailed_info(ip_or_domain)

@mcp.tool()
def check_ip_security(ip_address: str) -> str:
    """检查IP地址的安全威胁信息"""
    return ip_security_check(ip_address)

@mcp.tool()
def analyze_ip_comprehensive(ip_or_domain: str) -> str:
    """对IP地址或域名进行综合分析，包括地理位置、网络信息和安全检查"""
    return ip_comprehensive_analysis(ip_or_domain)

# ----------------------------------------------------------
# 新闻和天气服务
# ----------------------------------------------------------
@mcp.tool()
def get_china_news(limit: int = 5) -> str:
    """获取中国新闻热点"""
    service_config = config_manager.get_service_config("news")
    api_key = service_config.api_key or config_manager.get("news_api_key")
    
    def make_request(endpoint: str) -> str:
        try:
            params = {
                'country': 'cn',
                'apiKey': api_key,
                'pageSize': min(limit, 20)  # 限制最大数量
            }
            
            response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                news_list = []
                for i, article in enumerate(articles, 1):
                    title = article.get('title', '无标题')
                    source = article.get('source', {}).get('name', '未知来源')
                    news_list.append(f"{i}. {title}（{source}）")
                return '\n'.join(news_list) if news_list else "暂无新闻数据"
            else:
                raise ValueError(f"API返回错误: {data.get('message', '未知错误')}")
                
        except Exception as e:
            error_msg = handle_api_error(e, "新闻获取", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

@mcp.tool()
def get_weather(city: str) -> str:
    """查询城市天气"""
    service_config = config_manager.get_service_config("weather")
    api_key = service_config.api_key or config_manager.get("weather_api_key")
    city_pinyin = pinyin.get(city.strip(), format="strip")
    
    def make_request(endpoint: str) -> str:
        try:
            params = {
                'q': city_pinyin,
                'appid': api_key,
                'lang': 'zh_cn',
                'units': 'metric'  # 使用摄氏度
            }
            
            response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
            data = response.json()
            
            if 'weather' in data and 'main' in data:
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                feels_like = data['main'].get('feels_like', temp)
                humidity = data['main'].get('humidity', 0)
                
                return (
                    f"{city}：{weather_desc}，温度 {temp:.1f}℃"
                    f"（体感 {feels_like:.1f}℃），湿度 {humidity}%"
                )
            else:
                raise ValueError("天气数据格式错误")
                
        except Exception as e:
            error_msg = handle_api_error(e, "天气查询", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

# ----------------------------------------------------------
# 加密货币服务
# ----------------------------------------------------------
@mcp.tool()
def query_crypto_price(crypto_symbol: str, vs_currency: str = "usd") -> str:
    """查询加密货币价格信息"""
    return get_crypto_price(crypto_symbol, vs_currency)

# ----------------------------------------------------------
# 内容服务
# ----------------------------------------------------------
@mcp.tool()
def fetch_inspirational_quote() -> str:
    """获取励志名言"""
    return get_inspirational_quote()

@mcp.tool()
def fetch_random_joke() -> str:
    """获取随机笑话"""
    return get_random_joke()

@mcp.tool()
def fetch_daily_motivation(content_type: str = "quote") -> str:
    """获取每日励志内容"""
    return get_daily_motivation(content_type)

# ----------------------------------------------------------
# 汇率服务
# ----------------------------------------------------------
@mcp.tool()
def query_exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """查询货币汇率转换"""
    return get_exchange_rate(from_currency, to_currency, amount)

@mcp.tool()
def list_supported_currencies() -> str:
    """获取支持的货币代码列表"""
    return get_supported_currencies()

# ----------------------------------------------------------
# 系统工具
# ----------------------------------------------------------
@mcp.tool()
def health_check() -> str:
    """检查所有API服务的健康状态"""
    if not config_manager.get("enable_health_check", True):
        return "健康检查已禁用"
    
    services = ["ip_location", "news", "weather", "cryptocurrency", "quotes", "jokes", "exchange_rate"]
    results = []
    
    for service_name in services:
        service_config = config_manager.get_service_config(service_name)
        try:
            # 简单的连通性测试
            endpoint = service_config.primary_endpoint.split('?')[0]  # 移除查询参数
            
            # 特殊处理需要参数的端点
            if "{}" in endpoint:
                if service_name == "exchange_rate":
                    endpoint = endpoint.replace("{}", "USD")  # 使用USD作为测试货币
                elif service_name == "ip_location":
                    endpoint = endpoint.replace("{}", "8.8.8.8")  # 使用Google DNS作为测试IP
                else:
                    endpoint = endpoint.replace("{}", "test")  # 通用测试值
            
            # 特殊处理加密货币API
            if service_name == "cryptocurrency" and "coingecko" in endpoint:
                # 为CoinGecko API添加必要的参数
                endpoint = f"{endpoint}?ids=bitcoin&vs_currencies=usd"
            
            if endpoint and not endpoint.startswith("backup://"):
                response = http_manager.get(endpoint, timeout=2)
                status = "✅ 正常" if response.status_code < 400 else f"⚠️ HTTP {response.status_code}"
            else:
                status = "⚠️ 跳过检查"
        except Exception as e:
            status = f"❌ 失败: {str(e)[:50]}"
        
        results.append(f"{service_name}: {status}")
    
    failed_endpoints = fallback_manager.get_failed_endpoints()
    if failed_endpoints:
        results.append(f"\n失败端点数量: {len(failed_endpoints)}")
    
    return "\n".join(results)

@mcp.tool()
def reset_failed_endpoints(service_name: str = "") -> str:
    """重置失败的API端点"""
    if service_name:
        fallback_manager.reset_failed_endpoints(service_name)
        return f"已重置 {service_name} 服务的失败端点"
    else:
        fallback_manager.reset_failed_endpoints()
        return "已重置所有失败端点"

def initialize_server():
    """初始化服务器"""
    logger.info("正在启动 Free API MCP Server...")
    logger.info(f"日志级别: {config_manager.get('log_level')}")
    logger.info(f"默认超时: {config_manager.get('default_timeout')}秒")
    
    # 如果启用健康检查，在启动时检查服务状态
    if config_manager.get("enable_health_check", True):
        logger.info("正在进行启动健康检查...")
        try:
            health_status = health_check()
            logger.info(f"健康检查结果:\n{health_status}")
        except Exception as e:
            logger.warning(f"启动健康检查失败: {e}")

def main():
    """主函数"""
    try:
        initialize_server()
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("服务器正在关闭...")
        http_manager.close()
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise

if __name__ == "__main__":
    main()