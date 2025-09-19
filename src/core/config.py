"""
配置管理模块
"""
import os
import logging
from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ServiceConfig:
    """API服务配置"""
    name: str
    primary_endpoint: str
    fallback_endpoints: List[str] = field(default_factory=list)
    timeout: int = 5
    retry_count: int = 2
    api_key: str = ""
    enabled: bool = True

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self._config = self._load_config()
        self._setup_logging()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        return {
            # API密钥配置
            "news_api_key": os.getenv("NEWS_API_KEY", "3a7809d74c124c4ba0433760efbcd8bc"),
            "weather_api_key": os.getenv("WEATHER_API_KEY", "6ab957b52e6f9710ee017ce4115c8933"),
            "abuseipdb_api_key": os.getenv("ABUSEIPDB_API_KEY", ""),
            
            # 日志配置
            "enable_logging": os.getenv("ENABLE_LOGGING", "true").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
            "log_file": os.getenv("LOG_FILE", "free-api-mcp.log"),
            
            # 性能配置
            "default_timeout": int(os.getenv("DEFAULT_TIMEOUT", "5")),
            "max_retries": int(os.getenv("MAX_RETRIES", "2")),
            
            # 服务配置
            "enable_health_check": os.getenv("ENABLE_HEALTH_CHECK", "true").lower() == "true",
        }
    
    def _setup_logging(self):
        """设置日志配置"""
        if not self._config["enable_logging"]:
            return
            
        log_level = getattr(logging, self._config["log_level"], logging.INFO)
        log_file = self._config["log_file"]
        
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 配置根日志记录器
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        # 清除现有处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(key, default)
    
    def get_service_config(self, service_name: str) -> ServiceConfig:
        """获取服务配置"""
        configs = {
            "ip_location": ServiceConfig(
                name="ip_location",
                primary_endpoint="https://ip-api.com/json/{}?fields=status,message,country,regionName,city,isp&lang=zh",
                fallback_endpoints=[
                    "https://freeipapi.com/api/json/{}",
                    "http://ip-api.com/json/{}?fields=country,regionName,city,isp"
                ]
            ),
            "cryptocurrency": ServiceConfig(
                name="cryptocurrency", 
                primary_endpoint="https://api.coingecko.com/api/v3/simple/price",
                fallback_endpoints=[
                    "https://api.coincap.io/v2/assets",
                    "https://min-api.cryptocompare.com/data/price"
                ]
            ),
            "quotes": ServiceConfig(
                name="quotes",
                primary_endpoint="https://api.quotable.io/random",
                fallback_endpoints=[
                    "https://zenquotes.io/api/random"
                ]
            ),
            "jokes": ServiceConfig(
                name="jokes", 
                primary_endpoint="https://v2.jokeapi.dev/joke/Any?safe-mode",
                fallback_endpoints=[
                    "https://official-joke-api.appspot.com/random_joke"
                ]
            ),
            "exchange_rate": ServiceConfig(
                name="exchange_rate",
                primary_endpoint="https://api.exchangerate-api.com/v4/latest/{}",
                fallback_endpoints=[
                    "https://api.fixer.io/latest?base={}",
                    "backup://local-rates"  # 本地备用汇率
                ]
            ),
            "qr_code": ServiceConfig(
                name="qr_code",
                primary_endpoint="https://api.qrserver.com/v1/create-qr-code/",
                fallback_endpoints=[
                    "https://api.goqr.me/qr/create"
                ]
            ),
            "url_shortener": ServiceConfig(
                name="url_shortener",
                primary_endpoint="https://tinyurl.com/api-create.php",
                fallback_endpoints=[
                    "https://is.gd/create.php"
                ]
            ),
            "news": ServiceConfig(
                name="news",
                primary_endpoint="https://newsapi.org/v2/top-headlines",
                fallback_endpoints=[
                    "https://newsdata.io/api/1/news"
                ],
                api_key=self.get("news_api_key")
            ),
            "weather": ServiceConfig(
                name="weather",
                primary_endpoint="https://api.openweathermap.org/data/2.5/weather",
                fallback_endpoints=[
                    "https://api.weatherapi.com/v1/current.json"
                ],
                api_key=self.get("weather_api_key")
            )
        }
        
        return configs.get(service_name, ServiceConfig(
            name=service_name,
            primary_endpoint="",
            fallback_endpoints=[]
        ))

# 全局配置管理器实例
config_manager = ConfigManager()