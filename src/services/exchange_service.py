"""
汇率查询服务
"""
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def get_exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """
    查询货币汇率转换
    
    Args:
        from_currency: 源货币代码，如 USD, CNY, EUR
        to_currency: 目标货币代码，如 USD, CNY, EUR  
        amount: 转换金额，默认为 1.0
    """
    service_config = config_manager.get_service_config("exchange_rate")
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()
    
    # 常见货币代码验证
    valid_currencies = {
        'USD', 'EUR', 'GBP', 'JPY', 'CNY', 'AUD', 'CAD', 'CHF', 'HKD', 'SGD',
        'KRW', 'INR', 'RUB', 'BRL', 'ZAR', 'MXN', 'NOK', 'SEK', 'DKK', 'PLN'
    }
    
    if from_currency not in valid_currencies:
        return f"❌ 不支持的源货币代码: {from_currency}\n\n支持的货币: {', '.join(sorted(valid_currencies))}"
    
    if to_currency not in valid_currencies:
        return f"❌ 不支持的目标货币代码: {to_currency}\n\n支持的货币: {', '.join(sorted(valid_currencies))}"
    
    if from_currency == to_currency:
        return f"💱 {amount} {from_currency} = {amount} {to_currency}\n\n汇率: 1.0000 (相同货币)"
    
    def make_request(endpoint: str) -> str:
        try:
            # ExchangeRate-API
            if "exchangerate-api.com" in endpoint:
                url = endpoint.format(from_currency)
                response = http_manager.get(url, timeout=service_config.timeout)
                data = response.json()
                
                # 检查是否有rates字段（新版API格式）或conversion_rates字段（旧版API格式）
                rates = data.get('rates') or data.get('conversion_rates', {})
                if rates and to_currency in rates:
                    rate = rates[to_currency]
                    converted_amount = amount * rate
                    
                    # 获取更新时间
                    update_time = (
                        data.get('time_last_update_utc') or 
                        data.get('date') or 
                        '未知'
                    )
                    
                    return (
                        f"💱 {amount} {from_currency} = {converted_amount:.4f} {to_currency}\n\n"
                        f"汇率: 1 {from_currency} = {rate:.4f} {to_currency}\n"
                        f"📅 更新时间: {update_time}\n"
                        f"📊 数据来源: ExchangeRate-API"
                    )
                elif 'error-type' in data:
                    raise ValueError(f"API错误: {data.get('error-type', '未知错误')}")
                elif not rates:
                    raise ValueError("API返回数据格式错误：缺少汇率数据")
                else:
                    raise ValueError(f"不支持的目标货币: {to_currency}")
            
            # Fixer.io API 备用
            elif "fixer.io" in endpoint:
                url = endpoint.format(from_currency)
                params = {'symbols': to_currency}
                response = http_manager.get(url, params=params, timeout=service_config.timeout)
                data = response.json()
                
                if data.get('success', False):
                    rates = data.get('rates', {})
                    if to_currency in rates:
                        rate = rates[to_currency]
                        converted_amount = amount * rate
                        
                        return (
                            f"💱 {amount} {from_currency} = {converted_amount:.4f} {to_currency}\n\n"
                            f"汇率: 1 {from_currency} = {rate:.4f} {to_currency}\n"
                            f"📅 日期: {data.get('date', '未知')}\n"
                            f"📊 数据来源: Fixer.io"
                        )
                    else:
                        raise ValueError(f"不支持的目标货币: {to_currency}")
                else:
                    error_info = data.get('error', {})
                    raise ValueError(f"API错误: {error_info.get('info', '未知错误')}")
            
            # 简单的固定汇率备用（仅用于演示）
            elif "backup" in endpoint:
                # 一些常见的近似汇率（实际应用中不推荐使用固定汇率）
                backup_rates = {
                    # USD 相关
                    ('USD', 'CNY'): 7.2, ('CNY', 'USD'): 0.139,
                    ('USD', 'EUR'): 0.85, ('EUR', 'USD'): 1.18,
                    ('USD', 'GBP'): 0.73, ('GBP', 'USD'): 1.37,
                    ('USD', 'JPY'): 110.0, ('JPY', 'USD'): 0.009,
                    ('USD', 'AUD'): 1.35, ('AUD', 'USD'): 0.74,
                    ('USD', 'CAD'): 1.25, ('CAD', 'USD'): 0.80,
                    
                    # EUR 相关
                    ('EUR', 'CNY'): 8.5, ('CNY', 'EUR'): 0.118,
                    ('EUR', 'GBP'): 0.86, ('GBP', 'EUR'): 1.16,
                    ('EUR', 'JPY'): 130.0, ('JPY', 'EUR'): 0.0077,
                    
                    # 其他常见货币对
                    ('GBP', 'CNY'): 9.9, ('CNY', 'GBP'): 0.101,
                    ('GBP', 'JPY'): 151.0, ('JPY', 'GBP'): 0.0066,
                    ('CNY', 'JPY'): 15.3, ('JPY', 'CNY'): 0.065,
                }
                
                rate_key = (from_currency, to_currency)
                if rate_key in backup_rates:
                    rate = backup_rates[rate_key]
                    converted_amount = amount * rate
                    
                    return (
                        f"💱 {amount} {from_currency} = {converted_amount:.4f} {to_currency}\n\n"
                        f"汇率: 1 {from_currency} = {rate:.4f} {to_currency}\n"
                        f"⚠️ 使用近似汇率（仅供参考）\n"
                        f"📊 数据来源: 本地备用汇率"
                    )
                else:
                    raise ValueError(f"备用汇率不支持 {from_currency} 到 {to_currency} 的转换")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "汇率查询", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def get_supported_currencies() -> str:
    """获取支持的货币代码列表"""
    currencies = {
        'USD': '美元', 'EUR': '欧元', 'GBP': '英镑', 'JPY': '日元', 'CNY': '人民币',
        'AUD': '澳元', 'CAD': '加元', 'CHF': '瑞士法郎', 'HKD': '港币', 'SGD': '新加坡元',
        'KRW': '韩元', 'INR': '印度卢比', 'RUB': '俄罗斯卢布', 'BRL': '巴西雷亚尔',
        'ZAR': '南非兰特', 'MXN': '墨西哥比索', 'NOK': '挪威克朗', 'SEK': '瑞典克朗',
        'DKK': '丹麦克朗', 'PLN': '波兰兹罗提'
    }
    
    result = "💰 支持的货币代码:\n\n"
    for code, name in currencies.items():
        result += f"{code} - {name}\n"
    
    result += "\n💡 使用示例:\n"
    result += "• get_exchange_rate('USD', 'CNY', 100) - 100美元转人民币\n"
    result += "• get_exchange_rate('EUR', 'JPY') - 1欧元转日元"
    
    return result