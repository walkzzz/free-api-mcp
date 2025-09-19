"""
统一的错误处理模块
"""
import logging
import httpx
import json
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class APIError(Exception):
    """API调用异常"""
    def __init__(self, message: str, service_name: str, endpoint: str = ""):
        self.message = message
        self.service_name = service_name
        self.endpoint = endpoint
        super().__init__(self.message)

def handle_api_error(e: Exception, service_name: str, endpoint: str = "") -> str:
    """
    统一的API错误处理函数
    
    Args:
        e: 异常对象
        service_name: 服务名称
        endpoint: API端点
        
    Returns:
        格式化的错误信息
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = f"{service_name}服务暂时不可用"
    
    if isinstance(e, httpx.TimeoutException):
        error_msg += "：请求超时"
        logger.error(f"[{timestamp}] {service_name} timeout error: {endpoint}")
    elif isinstance(e, httpx.HTTPStatusError):
        status_code = e.response.status_code
        error_msg += f"：HTTP {status_code}"
        logger.error(f"[{timestamp}] {service_name} HTTP error {status_code}: {endpoint}")
    elif isinstance(e, json.JSONDecodeError):
        error_msg += "：数据解析失败"
        logger.error(f"[{timestamp}] {service_name} JSON decode error: {endpoint}")
    elif isinstance(e, httpx.ConnectError):
        error_msg += "：连接失败"
        logger.error(f"[{timestamp}] {service_name} connection error: {endpoint}")
    else:
        error_msg += f"：{str(e)}"
        logger.error(f"[{timestamp}] {service_name} unknown error: {e}, endpoint: {endpoint}")
    
    return error_msg

def format_success_response(data: dict, service_name: str, endpoint: str = "") -> str:
    """
    格式化成功响应
    
    Args:
        data: 响应数据
        service_name: 服务名称
        endpoint: API端点
        
    Returns:
        格式化的响应字符串
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] {service_name} success: {endpoint}")
    return data