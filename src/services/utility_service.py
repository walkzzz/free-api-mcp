"""
实用工具服务：二维码生成、短链接、UUID等
"""
import uuid
import random
import string
from ..core.config import config_manager
from ..core.http_client import http_manager
from ..core.error_handler import handle_api_error
from ..core.fallback_manager import fallback_manager

def generate_qr_code(text: str, size: str = "200x200") -> str:
    """生成二维码"""
    service_config = config_manager.get_service_config("qr_code")
    
    # 验证输入
    if not text.strip():
        return "❌ 错误: 请提供要生成二维码的文本内容"
    
    if len(text) > 1000:
        return "❌ 错误: 文本内容过长，请限制在1000字符以内"
    
    def make_request(endpoint: str) -> str:
        try:
            # QR Server API
            if "qrserver.com" in endpoint:
                params = {
                    'size': size,
                    'data': text
                }
                
                # 构建完整URL
                qr_url = f"{endpoint}?size={size}&data={text}"
                
                # 测试URL是否可访问
                response = http_manager.get(qr_url, timeout=service_config.timeout)
                if response.status_code == 200:
                    return (
                        f"📱 二维码生成成功:\n\n"
                        f"📝 内容: {text}\n"
                        f"📏 尺寸: {size}\n"
                        f"🖼️ 二维码链接: {qr_url}\n"
                        f"💡 提示: 可以直接在浏览器中打开链接查看或下载二维码"
                    )
                
                raise ValueError("二维码生成失败")
            
            # GoQR API 备用
            elif "goqr.me" in endpoint:
                params = {
                    'size': size,
                    'data': text
                }
                
                qr_url = f"{endpoint}?size={size}&data={text}"
                response = http_manager.get(qr_url, timeout=service_config.timeout)
                
                if response.status_code == 200:
                    return (
                        f"📱 二维码生成成功:\n\n"
                        f"📝 内容: {text}\n"
                        f"📏 尺寸: {size}\n"
                        f"🖼️ 二维码链接: {qr_url}\n"
                        f"💡 提示: 可以直接在浏览器中打开链接查看或下载二维码\n"
                        f"📊 数据来源: GoQR"
                    )
                
                raise ValueError("二维码生成失败")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "二维码生成", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def shorten_url(long_url: str) -> str:
    """生成短链接"""
    service_config = config_manager.get_service_config("url_shortener")
    
    # 验证URL格式
    if not long_url.strip():
        return "❌ 错误: 请提供要缩短的URL"
    
    if not (long_url.startswith('http://') or long_url.startswith('https://')):
        long_url = 'https://' + long_url
    
    def make_request(endpoint: str) -> str:
        try:
            # TinyURL API
            if "tinyurl.com" in endpoint:
                params = {'url': long_url}
                response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
                
                if response.status_code == 200:
                    short_url = response.text.strip()
                    if short_url and short_url.startswith('http'):
                        return (
                            f"🔗 短链接生成成功:\n\n"
                            f"📎 原始链接: {long_url}\n"
                            f"✂️ 短链接: {short_url}\n"
                            f"📊 数据来源: TinyURL"
                        )
                
                raise ValueError("短链接生成失败")
            
            # is.gd API 备用
            elif "is.gd" in endpoint:
                params = {
                    'format': 'simple',
                    'url': long_url
                }
                response = http_manager.get(endpoint, params=params, timeout=service_config.timeout)
                
                if response.status_code == 200:
                    short_url = response.text.strip()
                    if short_url and short_url.startswith('http'):
                        return (
                            f"🔗 短链接生成成功:\n\n"
                            f"📎 原始链接: {long_url}\n"
                            f"✂️ 短链接: {short_url}\n"
                            f"📊 数据来源: is.gd"
                        )
                
                raise ValueError("短链接生成失败")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "短链接生成", endpoint)
            raise Exception(error_msg)
    
    return fallback_manager.execute_with_fallback(service_config, make_request)

def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """生成随机密码"""
    # 验证参数
    if length < 4:
        return "❌ 错误: 密码长度至少为4位"
    
    if length > 128:
        return "❌ 错误: 密码长度不能超过128位"
    
    # 字符集
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    # 确保密码包含各种字符类型
    password_chars = []
    
    # 至少包含一个小写字母
    password_chars.append(random.choice(lowercase))
    
    # 至少包含一个大写字母
    password_chars.append(random.choice(uppercase))
    
    # 至少包含一个数字
    password_chars.append(random.choice(digits))
    
    # 如果包含符号，至少包含一个符号
    if include_symbols:
        password_chars.append(random.choice(symbols))
    
    # 填充剩余长度
    all_chars = lowercase + uppercase + digits + symbols
    remaining_length = length - len(password_chars)
    
    for _ in range(remaining_length):
        password_chars.append(random.choice(all_chars))
    
    # 打乱顺序
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    
    # 计算密码强度
    strength_score = 0
    if any(c in lowercase for c in password):
        strength_score += 1
    if any(c in uppercase for c in password):
        strength_score += 1
    if any(c in digits for c in password):
        strength_score += 1
    if any(c in symbols for c in password):
        strength_score += 1
    if length >= 12:
        strength_score += 1
    
    strength_levels = {
        1: "很弱",
        2: "弱", 
        3: "中等",
        4: "强",
        5: "很强"
    }
    
    strength = strength_levels.get(strength_score, "未知")
    
    return (
        f"🔐 随机密码生成:\n\n"
        f"🔑 密码: {password}\n"
        f"📏 长度: {length}位\n"
        f"💪 强度: {strength}\n"
        f"🔢 包含数字: {'是' if any(c in digits for c in password) else '否'}\n"
        f"🔤 包含大写: {'是' if any(c in uppercase for c in password) else '否'}\n"
        f"🔡 包含小写: {'是' if any(c in lowercase for c in password) else '否'}\n"
        f"🔣 包含符号: {'是' if include_symbols and any(c in symbols for c in password) else '否'}\n"
        f"💡 提示: 请妥善保管您的密码"
    )

def generate_uuid(version: int = 4) -> str:
    """生成UUID"""
    try:
        if version == 1:
            generated_uuid = str(uuid.uuid1())
            uuid_type = "UUID1 (基于时间戳和MAC地址)"
        elif version == 4:
            generated_uuid = str(uuid.uuid4())
            uuid_type = "UUID4 (随机生成)"
        else:
            return "❌ 错误: 仅支持UUID版本1和4"
        
        return (
            f"🆔 UUID生成成功:\n\n"
            f"🔢 UUID: {generated_uuid}\n"
            f"📋 类型: {uuid_type}\n"
            f"📏 长度: 36字符\n"
            f"🔤 格式: 8-4-4-4-12\n"
            f"💡 用途: 数据库主键、文件名、会话ID等"
        )
        
    except Exception as e:
        return f"❌ UUID生成失败: {str(e)}"

def get_color_info(color_input: str) -> str:
    """获取颜色信息"""
    service_config = config_manager.get_service_config("color_info")
    
    # 清理输入
    color_input = color_input.strip().replace('#', '')
    
    # 验证十六进制颜色格式
    if not color_input:
        return "❌ 错误: 请提供颜色值（如: FF5733 或 #FF5733）"
    
    if len(color_input) not in [3, 6]:
        return "❌ 错误: 请提供有效的十六进制颜色值（3位或6位）"
    
    try:
        # 验证是否为有效的十六进制
        int(color_input, 16)
    except ValueError:
        return "❌ 错误: 请提供有效的十六进制颜色值"
    
    # 转换为6位格式
    if len(color_input) == 3:
        color_input = ''.join([c*2 for c in color_input])
    
    def make_request(endpoint: str) -> str:
        try:
            # TheColorAPI
            if "thecolorapi.com" in endpoint:
                url = f"{endpoint}?hex={color_input}"
                response = http_manager.get(url, timeout=service_config.timeout)
                data = response.json()
                
                hex_value = data.get('hex', {}).get('value', '')
                rgb = data.get('rgb', {})
                hsl = data.get('hsl', {})
                name = data.get('name', {}).get('value', '未知')
                
                if hex_value:
                    return (
                        f"🎨 颜色信息:\n\n"
                        f"🏷️ 颜色名称: {name}\n"
                        f"🔢 十六进制: {hex_value}\n"
                        f"🔴 RGB: rgb({rgb.get('r', 0)}, {rgb.get('g', 0)}, {rgb.get('b', 0)})\n"
                        f"🌈 HSL: hsl({hsl.get('h', 0)}, {hsl.get('s', 0)}%, {hsl.get('l', 0)}%)\n"
                        f"📊 数据来源: TheColorAPI"
                    )
                
                raise ValueError("无法获取颜色信息")
            
            raise ValueError("未知的API端点")
            
        except Exception as e:
            error_msg = handle_api_error(e, "颜色信息获取", endpoint)
            raise Exception(error_msg)
    
    # 如果API失败，提供基本的颜色信息
    try:
        result = fallback_manager.execute_with_fallback(service_config, make_request)
        return result
    except:
        # 本地计算RGB值
        r = int(color_input[0:2], 16)
        g = int(color_input[2:4], 16)
        b = int(color_input[4:6], 16)
        
        return (
            f"🎨 颜色信息:\n\n"
            f"🔢 十六进制: #{color_input.upper()}\n"
            f"🔴 RGB: rgb({r}, {g}, {b})\n"
            f"💡 提示: 这是基本的颜色信息，详细信息需要API支持\n"
            f"📊 数据来源: 本地计算"
        )