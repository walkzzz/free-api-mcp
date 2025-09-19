"""
内容服务：励志名言和笑话
"""
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def get_inspirational_quote() -> str:
    """获取励志名言"""
    service_config = config_manager.get_service_config("quotes")
    
    # 预设的中文励志名言作为备用
    backup_quotes = [
        "成功不是终点，失败不是致命的，继续前进的勇气才是最重要的。 —— 温斯顿·丘吉尔",
        "你唯一需要知道的是如何信任你自己的无意识，那样你就能即兴发挥，做到最好。 —— 马龙·白兰度",
        "不要害怕放弃好的去追求更好的。 —— 约翰·D·洛克菲勒",
        "成功的秘诀在于坚持自己的目标。 —— 本杰明·迪斯雷利",
        "生活中最重要的事情不是你遭遇了什么，而是你记住了什么，又是如何记住的。 —— 加西亚·马尔克斯"
    ]
    
    def make_request(endpoint: str) -> str:
        try:
            # Quotable API
            if "quotable.io" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if 'content' in data and 'author' in data:
                    content = data['content']
                    author = data['author']
                    return f"💡 {content}\n\n—— {author}"
                else:
                    raise ValueError("无法解析名言数据")
            
            # ZenQuotes API 备用
            elif "zenquotes.io" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    quote = data[0]
                    content = quote.get('q', '')
                    author = quote.get('a', 'Unknown')
                    if content:
                        return f"💡 {content}\n\n—— {author}"
                
                raise ValueError("无法解析名言数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "励志名言获取", endpoint)
            raise Exception(error_msg)
    
    result = fallback_manager.execute_with_fallback(service_config, make_request)
    
    # 如果所有API都失败，fallback_manager会返回错误信息，此时使用预设内容
    if "不可用" in result or "失败" in result:
        import random
        selected_quote = random.choice(backup_quotes)
        return f"💡 {selected_quote}\n\n📝 来源：本地预设名言库"
    
    return result

def get_random_joke() -> str:
    """获取随机笑话"""
    service_config = config_manager.get_service_config("jokes")
    
    # 预设的中文笑话作为备用
    backup_jokes = [
        "为什么程序员喜欢黑暗？因为光会产生bug！",
        "有10种人：懂二进制的和不懂二进制的。",
        "为什么Java程序员要戴眼镜？因为他们看不到C#！",
        "程序员的三大美德：懒惰、急躁和傲慢。",
        "为什么程序员总是混淆万圣节和圣诞节？因为Oct 31 == Dec 25！"
    ]
    
    def make_request(endpoint: str) -> str:
        try:
            # JokeAPI
            if "jokeapi.dev" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if data.get('error', False):
                    raise ValueError(f"API错误: {data.get('message', '未知错误')}")
                
                if data.get('type') == 'single':
                    joke = data.get('joke', '')
                    if joke:
                        return f"😄 {joke}"
                elif data.get('type') == 'twopart':
                    setup = data.get('setup', '')
                    delivery = data.get('delivery', '')
                    if setup and delivery:
                        return f"😄 {setup}\n\n{delivery}"
                
                raise ValueError("无法解析笑话数据")
            
            # Official Joke API 备用
            elif "official-joke-api" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if 'setup' in data and 'punchline' in data:
                    setup = data['setup']
                    punchline = data['punchline']
                    return f"😄 {setup}\n\n{punchline}"
                else:
                    raise ValueError("无法解析笑话数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "笑话获取", endpoint)
            raise Exception(error_msg)
    
    result = fallback_manager.execute_with_fallback(service_config, make_request)
    
    # 如果所有API都失败，fallback_manager会返回错误信息，此时使用预设内容
    if "不可用" in result or "失败" in result:
        import random
        selected_joke = random.choice(backup_jokes)
        return f"😄 {selected_joke}\n\n📝 来源：本地预设笑话库"
    
    return result

def get_daily_motivation(content_type: str = "quote") -> str:
    """
    获取每日励志内容
    
    Args:
        content_type: 内容类型，"quote" 为名言，"joke" 为笑话
    """
    content_type = content_type.lower().strip()
    
    if content_type == "joke":
        return get_random_joke()
    else:
        return get_inspirational_quote()