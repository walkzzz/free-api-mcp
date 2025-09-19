"""
HTTP客户端配置和管理
"""
import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class HTTPClientManager:
    """HTTP客户端管理器"""
    
    def __init__(self):
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None
    
    @property
    def client(self) -> httpx.Client:
        """获取同步HTTP客户端"""
        if self._client is None:
            self._client = httpx.Client(
                timeout=5.0,
                limits=httpx.Limits(
                    max_keepalive_connections=10,
                    max_connections=20
                ),
                headers={
                    "User-Agent": "Free-API-MCP/1.0"
                }
            )
        return self._client
    
    @property
    def async_client(self) -> httpx.AsyncClient:
        """获取异步HTTP客户端"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                timeout=5.0,
                limits=httpx.Limits(
                    max_keepalive_connections=10,
                    max_connections=20
                ),
                headers={
                    "User-Agent": "Free-API-MCP/1.0"
                }
            )
        return self._async_client
    
    def close(self):
        """关闭客户端连接"""
        if self._client:
            self._client.close()
        if self._async_client:
            # 注意：异步客户端需要在异步上下文中关闭
            pass
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, timeout: float = 5.0) -> httpx.Response:
        """
        发送GET请求
        
        Args:
            url: 请求URL
            params: 查询参数
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HTTP响应对象
        """
        try:
            response = self.client.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=timeout
            )
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"HTTP GET error for {url}: {e}")
            raise

# 全局HTTP客户端管理器实例
http_manager = HTTPClientManager()