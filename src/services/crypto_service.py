"""
加密货币价格查询服务
"""
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def get_crypto_price(crypto_symbol: str, vs_currency: str = "usd") -> str:
    """
    查询加密货币价格信息
    
    Args:
        crypto_symbol: 加密货币符号，如 bitcoin, ethereum, dogecoin
        vs_currency: 对比货币，默认为 usd，也支持 cny
    """
    service_config = config_manager.get_service_config("cryptocurrency")
    crypto_symbol = crypto_symbol.lower().strip()
    vs_currency = vs_currency.lower().strip()
    
    def make_request(endpoint: str) -> str:
        try:
            # CoinGecko API
            if "coingecko" in endpoint:
                params = {
                    'ids': crypto_symbol,
                    'vs_currencies': vs_currency,
                    'include_market_cap': 'true',
                    'include_24hr_change': 'true'
                }
                response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
                data = response.json()
                
                if crypto_symbol in data:
                    crypto_data = data[crypto_symbol]
                    price = crypto_data.get(vs_currency, 0)
                    market_cap = crypto_data.get(f"{vs_currency}_market_cap", 0)
                    change_24h = crypto_data.get(f"{vs_currency}_24h_change", 0)
                    
                    currency_symbol = "$" if vs_currency == "usd" else "¥" if vs_currency == "cny" else vs_currency.upper()
                    
                    return (
                        f"{crypto_symbol.upper()} 价格信息:\n"
                        f"💰 当前价格: {currency_symbol}{price:,.2f}\n"
                        f"📊 市值: {currency_symbol}{market_cap:,.0f}\n"
                        f"📈 24小时变化: {change_24h:+.2f}%"
                    )
                else:
                    raise ValueError(f"未找到加密货币: {crypto_symbol}")
            
            # CoinCap API 备用
            elif "coincap" in endpoint:
                # 首先搜索资产ID
                search_url = f"{endpoint}?search={crypto_symbol}&limit=1"
                response = http_manager.get(search_url, timeout=service_config.timeout)
                data = response.json()
                
                if data.get('data') and len(data['data']) > 0:
                    asset = data['data'][0]
                    price_usd = float(asset.get('priceUsd', 0))
                    market_cap_usd = float(asset.get('marketCapUsd', 0))
                    change_24h = float(asset.get('changePercent24Hr', 0))
                    
                    # 简单的USD到CNY转换（实际应该调用汇率API）
                    if vs_currency == "cny":
                        price = price_usd * 7.2  # 近似汇率
                        market_cap = market_cap_usd * 7.2
                        currency_symbol = "¥"
                    else:
                        price = price_usd
                        market_cap = market_cap_usd
                        currency_symbol = "$"
                    
                    return (
                        f"{asset['name']} ({asset['symbol']}) 价格信息:\n"
                        f"💰 当前价格: {currency_symbol}{price:,.2f}\n"
                        f"📊 市值: {currency_symbol}{market_cap:,.0f}\n"
                        f"📈 24小时变化: {change_24h:+.2f}%"
                    )
                else:
                    raise ValueError(f"未找到加密货币: {crypto_symbol}")
            
            # CryptoCompare API 备用
            elif "cryptocompare" in endpoint:
                params = {
                    'fsym': crypto_symbol.upper(),
                    'tsyms': vs_currency.upper()
                }
                response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
                data = response.json()
                
                if vs_currency.upper() in data:
                    price = data[vs_currency.upper()]
                    currency_symbol = "$" if vs_currency == "usd" else "¥" if vs_currency == "cny" else vs_currency.upper()
                    
                    return (
                        f"{crypto_symbol.upper()} 价格信息:\n"
                        f"💰 当前价格: {currency_symbol}{price:,.2f}\n"
                        f"📊 数据来源: CryptoCompare"
                    )
                else:
                    raise ValueError(f"未找到加密货币: {crypto_symbol}")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "加密货币价格查询", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)