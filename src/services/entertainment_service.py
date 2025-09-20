"""
娱乐服务：随机图片、表情包、有趣事实等
"""
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def get_random_cat_image() -> str:
    """获取随机猫咪图片"""
    service_config = config_manager.get_service_config("cat_images")
    
    def make_request(endpoint: str) -> str:
        try:
            # TheCatAPI
            if "thecatapi.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    cat_data = data[0]
                    image_url = cat_data.get('url', '')
                    width = cat_data.get('width', 0)
                    height = cat_data.get('height', 0)
                    
                    if image_url:
                        return (
                            f"🐱 随机猫咪图片:\n\n"
                            f"🖼️ 图片链接: {image_url}\n"
                            f"📏 尺寸: {width}x{height}px\n"
                            f"💡 提示: 可以直接在浏览器中打开链接查看图片"
                        )
                
                raise ValueError("无法获取猫咪图片数据")
            
            # Cataas API 备用
            elif "cataas.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                if response.status_code == 200:
                    # 这个API直接返回图片，我们返回URL
                    return (
                        f"🐱 随机猫咪图片:\n\n"
                        f"🖼️ 图片链接: {endpoint}\n"
                        f"💡 提示: 可以直接在浏览器中打开链接查看图片\n"
                        f"📊 数据来源: Cataas"
                    )
                
                raise ValueError("无法获取猫咪图片")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "猫咪图片获取", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def get_random_dog_image() -> str:
    """获取随机狗狗图片"""
    service_config = config_manager.get_service_config("dog_images")
    
    def make_request(endpoint: str) -> str:
        try:
            # Dog CEO API
            if "dog.ceo" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if data.get('status') == 'success':
                    image_url = data.get('message', '')
                    if image_url:
                        # 从URL中提取品种信息
                        breed = "未知品种"
                        if "/breeds/" in image_url:
                            try:
                                breed_part = image_url.split("/breeds/")[1].split("/")[0]
                                breed = breed_part.replace("-", " ").title()
                            except:
                                pass
                        
                        return (
                            f"🐶 随机狗狗图片:\n\n"
                            f"🖼️ 图片链接: {image_url}\n"
                            f"🐕 品种: {breed}\n"
                            f"💡 提示: 可以直接在浏览器中打开链接查看图片\n"
                            f"📊 数据来源: Dog CEO"
                        )
                
                raise ValueError("无法获取狗狗图片数据")
            
            # TheDogAPI 备用
            elif "thedogapi.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    dog_data = data[0]
                    image_url = dog_data.get('url', '')
                    width = dog_data.get('width', 0)
                    height = dog_data.get('height', 0)
                    
                    if image_url:
                        return (
                            f"🐶 随机狗狗图片:\n\n"
                            f"🖼️ 图片链接: {image_url}\n"
                            f"📏 尺寸: {width}x{height}px\n"
                            f"💡 提示: 可以直接在浏览器中打开链接查看图片\n"
                            f"📊 数据来源: TheDogAPI"
                        )
                
                raise ValueError("无法获取狗狗图片数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "狗狗图片获取", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def get_random_fact() -> str:
    """获取随机有趣事实"""
    service_config = config_manager.get_service_config("random_facts")
    
    # 中文有趣事实备用库
    backup_facts = [
        "蜂蜜永远不会变质。考古学家在古埃及金字塔中发现了3000年前的蜂蜜，至今仍然可以食用。",
        "章鱼有三颗心脏和蓝色的血液。",
        "香蕉是浆果，但草莓不是。",
        "一只蜗牛可以睡3年。",
        "鲨鱼比树木出现得更早。鲨鱼存在了4亿年，而树木只有3.85亿年。",
        "人类的大脑使用的能量相当于一个20瓦的灯泡。",
        "蝴蝶用脚来品尝食物。",
        "企鹅有膝盖，只是被羽毛遮住了。",
        "一个人一生中会走过相当于绕地球5圈的距离。",
        "猫咪无法品尝甜味，因为它们缺少甜味受体。"
    ]
    
    def make_request(endpoint: str) -> str:
        try:
            # Useless Facts API
            if "uselessfacts.jsph.pl" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                fact = data.get('text', '')
                if fact:
                    return f"🤔 有趣事实:\n\n💡 {fact}\n\n📊 数据来源: Useless Facts API"
                
                raise ValueError("无法获取事实数据")
            
            # Fun Facts API 备用
            elif "api.api-ninjas.com" in endpoint:
                headers = {'X-Api-Key': 'your_api_key'}  # 需要API密钥
                response = http_manager.get(endpoint, headers=headers, timeout=service_config.timeout)
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    fact = data[0].get('fact', '')
                    if fact:
                        return f"🤔 有趣事实:\n\n💡 {fact}\n\n📊 数据来源: API Ninjas"
                
                raise ValueError("无法获取事实数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "有趣事实获取", endpoint)
            raise Exception(error_msg)
    
    result = fallback_manager.execute_with_fallback(service_config, make_request)
    
    # 如果所有API都失败，使用本地备用事实
    if "不可用" in result or "失败" in result:
        import random
        selected_fact = random.choice(backup_facts)
        return f"🤔 有趣事实:\n\n💡 {selected_fact}\n\n📝 来源：本地事实库"
    
    return result

def get_meme_image() -> str:
    """获取随机表情包"""
    service_config = config_manager.get_service_config("meme_images")
    
    def make_request(endpoint: str) -> str:
        try:
            # Meme API
            if "meme-api.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                if data.get('count', 0) > 0:
                    memes = data.get('data', {}).get('memes', [])
                    if memes:
                        meme = memes[0]
                        image_url = meme.get('image', '')
                        title = meme.get('title', '无标题')
                        
                        if image_url:
                            return (
                                f"😂 随机表情包:\n\n"
                                f"🏷️ 标题: {title}\n"
                                f"🖼️ 图片链接: {image_url}\n"
                                f"💡 提示: 可以直接在浏览器中打开链接查看图片"
                            )
                
                raise ValueError("无法获取表情包数据")
            
            # Reddit Meme API 备用
            elif "reddit.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                posts = data.get('data', {}).get('children', [])
                if posts:
                    post = posts[0]['data']
                    title = post.get('title', '无标题')
                    image_url = post.get('url', '')
                    
                    if image_url and any(ext in image_url for ext in ['.jpg', '.png', '.gif']):
                        return (
                            f"😂 随机表情包:\n\n"
                            f"🏷️ 标题: {title}\n"
                            f"🖼️ 图片链接: {image_url}\n"
                            f"💡 提示: 可以直接在浏览器中打开链接查看图片\n"
                            f"📊 数据来源: Reddit"
                        )
                
                raise ValueError("无法获取表情包数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "表情包获取", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def get_today_in_history() -> str:
    """获取历史上的今天"""
    service_config = config_manager.get_service_config("history_today")
    
    def make_request(endpoint: str) -> str:
        try:
            # Today in History API
            if "history.muffinlabs.com" in endpoint:
                response = http_manager.get(endpoint, timeout=service_config.timeout)
                data = response.json()
                
                events = data.get('data', {}).get('Events', [])
                if events:
                    # 取前3个事件
                    result_lines = ["📅 历史上的今天:\n"]
                    
                    for i, event in enumerate(events[:3], 1):
                        year = event.get('year', '未知年份')
                        text = event.get('text', '无描述')
                        result_lines.append(f"{i}. {year}年: {text}")
                    
                    result_lines.append(f"\n📊 数据来源: Muffin Labs")
                    return '\n'.join(result_lines)
                
                raise ValueError("无法获取历史事件数据")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "历史事件获取", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)