"""
备用端点管理器
"""
import logging
from typing import List, Callable, Any, Optional
from .config import ServiceConfig
from .http_client import http_manager
from .error_handler import handle_api_error

logger = logging.getLogger(__name__)

class FallbackManager:
    """备用端点管理器"""
    
    def __init__(self):
        self.failed_endpoints = set()
    
    def execute_with_fallback(self, 
                            service_config: ServiceConfig,
                            request_func: Callable[[str], Any],
                            *args, **kwargs) -> str:
        """
        使用备用端点执行请求
        
        Args:
            service_config: 服务配置
            request_func: 请求执行函数
            *args, **kwargs: 传递给请求函数的参数
            
        Returns:
            请求结果或错误信息
        """
        if not service_config.enabled:
            return f"{service_config.name}服务已禁用"
        
        # 尝试主端点
        endpoints = [service_config.primary_endpoint] + service_config.fallback_endpoints
        
        for endpoint in endpoints:
            if endpoint in self.failed_endpoints:
                logger.debug(f"跳过已失败的端点: {endpoint}")
                continue
                
            try:
                logger.info(f"尝试端点: {endpoint}")
                result = request_func(endpoint, *args, **kwargs)
                
                # 如果成功，从失败列表中移除
                if endpoint in self.failed_endpoints:
                    self.failed_endpoints.remove(endpoint)
                    logger.info(f"端点恢复正常: {endpoint}")
                
                return result
                
            except Exception as e:
                logger.warning(f"端点失败: {endpoint}, 错误: {e}")
                self.failed_endpoints.add(endpoint)
                continue
        
        # 所有端点都失败
        error_msg = f"{service_config.name}服务的所有端点都不可用，请稍后再试"
        logger.error(error_msg)
        return error_msg
    
    def reset_failed_endpoints(self, service_name: Optional[str] = None):
        """
        重置失败端点列表
        
        Args:
            service_name: 可选，指定服务名称只重置该服务的端点
        """
        if service_name:
            # 移除特定服务的失败端点
            to_remove = [ep for ep in self.failed_endpoints if service_name in ep]
            for ep in to_remove:
                self.failed_endpoints.remove(ep)
            logger.info(f"已重置 {service_name} 服务的失败端点")
        else:
            # 清空所有失败端点
            self.failed_endpoints.clear()
            logger.info("已重置所有失败端点")
    
    def get_failed_endpoints(self) -> List[str]:
        """获取当前失败的端点列表"""
        return list(self.failed_endpoints)

# 全局备用管理器实例
fallback_manager = FallbackManager()