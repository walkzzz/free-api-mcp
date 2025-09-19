"""
IP信息查询服务
"""
from urllib.parse import quote
import socket
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def resolve(host: str) -> str:
    """解析主机名或IP地址"""
    try:
        socket.inet_aton(host)
        return host
    except OSError:
        return socket.gethostbyname(host)

def ip_location(ip_or_domain: str) -> str:
    """查询IP地址或域名的基本归属地信息"""
    service_config = config_manager.get_service_config("ip_location")
    target = resolve(ip_or_domain.strip())
    
    def make_request(endpoint: str) -> str:
        try:
            url = endpoint.format(quote(target))
            response = http_manager.get(url, timeout=service_config.timeout)
            data = response.json()
            
            # ip-api.com 响应格式
            if data.get("status") == "success":
                return (
                    f"{ip_or_domain}（{target}）归属地："
                    f"{data['country']} {data['regionName']} {data['city']}｜{data['isp']}"
                )
            
            # freeipapi.com 响应格式
            if "countryName" in data:
                return (
                    f"{ip_or_domain}（{target}）归属地："
                    f"{data['countryName']} {data['regionName']} {data['cityName']}｜{data['isp']}"
                )
            
            # 通用格式
            if "country" in data:
                country = data.get("country", "未知")
                region = data.get("regionName", data.get("region", "未知"))
                city = data.get("city", "未知")
                isp = data.get("isp", data.get("org", "未知"))
                return f"{ip_or_domain}（{target}）归属地：{country} {region} {city}｜{isp}"
                
            raise ValueError("无法解析响应数据")
            
        except Exception as e:
            error_msg = handle_api_error(e, "IP归属地查询", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def ip_detailed_info(ip_or_domain: str) -> str:
    """查询IP地址或域名的详细信息，包括地理位置、ISP、时区等"""
    service_config = config_manager.get_service_config("ip_location")
    target = resolve(ip_or_domain.strip())
    
    def make_request(endpoint: str) -> str:
        try:
            # 使用更详细的字段查询
            if "ip-api.com" in endpoint:
                detailed_url = f"http://ip-api.com/json/{quote(target)}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
                response = http_manager.get(detailed_url, timeout=service_config.timeout)
                data = response.json()
                
                if data.get("status") == "success":
                    result = f"🌍 {ip_or_domain}（{target}）详细信息:\n\n"
                    result += f"📍 地理位置:\n"
                    result += f"   国家: {data.get('country', '未知')} ({data.get('countryCode', 'N/A')})\n"
                    result += f"   地区: {data.get('regionName', '未知')} ({data.get('region', 'N/A')})\n"
                    result += f"   城市: {data.get('city', '未知')}\n"
                    result += f"   邮编: {data.get('zip', '未知')}\n"
                    result += f"   坐标: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n"
                    result += f"   时区: {data.get('timezone', '未知')}\n\n"
                    result += f"🏢 网络信息:\n"
                    result += f"   ISP: {data.get('isp', '未知')}\n"
                    result += f"   组织: {data.get('org', '未知')}\n"
                    result += f"   AS: {data.get('as', '未知')}\n"
                    
                    return result
                else:
                    raise ValueError(f"API错误: {data.get('message', '未知错误')}")
            
            # 备用端点的简化处理
            else:
                url = endpoint.format(quote(target))
                response = http_manager.get(url, timeout=service_config.timeout)
                data = response.json()
                
                # 通用格式处理
                result = f"🌍 {ip_or_domain}（{target}）信息:\n\n"
                result += f"📍 位置: {data.get('country', '未知')} {data.get('regionName', data.get('region', '未知'))} {data.get('city', '未知')}\n"
                result += f"🏢 ISP: {data.get('isp', data.get('org', '未知'))}\n"
                
                return result
                
        except Exception as e:
            error_msg = handle_api_error(e, "IP详细信息查询", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def ip_security_check(ip_address: str) -> str:
    """检查IP地址的安全威胁信息"""
    # 验证输入是否为有效IP地址
    try:
        socket.inet_aton(ip_address.strip())
        target_ip = ip_address.strip()
    except OSError:
        # 如果不是IP地址，尝试解析域名
        try:
            target_ip = resolve(ip_address.strip())
        except:
            return f"❌ 无效的IP地址或域名: {ip_address}"
    
    # 简单的威胁检查（基于一些已知的恶意IP范围）
    def is_suspicious_ip(ip: str) -> tuple:
        """简单的IP威胁检查"""
        octets = ip.split('.')
        if len(octets) != 4:
            return False, "无效IP格式"
        
        try:
            first_octet = int(octets[0])
            second_octet = int(octets[1])
            
            # 检查私有IP地址（优先检查，避免误报）
            if (first_octet == 10 or 
                (first_octet == 172 and 16 <= second_octet <= 31) or
                (first_octet == 192 and second_octet == 168)):
                return False, "私有IP地址"
            
            # 检查本地回环地址
            if first_octet == 127:
                return False, "本地回环地址"
            
            # 检查一些已知的可疑IP范围（这只是示例，实际应用需要更完整的威胁情报数据库）
            suspicious_ranges = [
                # 这些只是示例范围，实际应用中需要使用真实的威胁情报数据
                # (185, 220), # 示例：185-220.x.x.x 范围（某些Tor出口节点常见范围）
            ]
            
            for start, end in suspicious_ranges:
                if start <= first_octet <= end:
                    return True, f"IP位于可疑范围 {start}.x.x.x - {end}.x.x.x"
            
            return False, "未发现威胁"
            
        except ValueError:
            return False, "IP格式错误"
    
    # 执行威胁检查
    is_threat, threat_info = is_suspicious_ip(target_ip)
    
    result = f"🔒 {ip_address}（{target_ip}）安全检查:\n\n"
    
    if is_threat:
        result += f"⚠️ 威胁状态: 可疑\n"
        result += f"📋 详情: {threat_info}\n"
        result += f"🚨 建议: 谨慎处理来自此IP的流量\n"
    else:
        result += f"✅ 威胁状态: 正常\n"
        result += f"📋 详情: {threat_info}\n"
        result += f"💡 建议: 未发现明显威胁\n"
    
    result += f"\n⚠️ 注意: 这是基于简单规则的检查，建议使用专业威胁情报服务进行更准确的分析。"
    
    return result

def ip_comprehensive_analysis(ip_or_domain: str) -> str:
    """对IP地址或域名进行综合分析，包括地理位置、网络信息和安全检查"""
    try:
        target = resolve(ip_or_domain.strip())
        
        result = f"🔍 {ip_or_domain} 综合分析报告\n"
        result += "=" * 50 + "\n\n"
        
        # 获取详细信息
        try:
            detailed_info = ip_detailed_info(ip_or_domain)
            result += detailed_info + "\n\n"
        except Exception as e:
            result += f"⚠️ 详细信息获取失败: {str(e)[:100]}...\n\n"
        
        # 获取安全检查信息
        try:
            security_info = ip_security_check(target)
            result += security_info + "\n\n"
        except Exception as e:
            result += f"⚠️ 安全检查失败: {str(e)[:100]}...\n\n"
        
        result += f"📅 分析时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"🔧 分析工具: Free API MCP Server"
        
        return result
        
    except Exception as e:
        return f"❌ 综合分析失败: {str(e)}"