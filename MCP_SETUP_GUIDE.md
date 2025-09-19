# Free API MCP Server - 快速配置指南

## 🚀 快速开始

### 1. 基本配置

在你的MCP配置文件中添加以下内容：

**工作区配置** (`.kiro/settings/mcp.json`):
```json
{
  "mcpServers": {
    "free-api-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"]
    }
  }
}
```

**用户级配置** (`~/.kiro/settings/mcp.json`):
```json
{
  "mcpServers": {
    "free-api-mcp": {
      "command": "uv", 
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "PYTHONPATH": "/path/to/free-api-mcp"
      }
    }
  }
}
```

### 2. 环境变量配置（可选）

如果需要自定义配置，可以添加环境变量：

```json
{
  "mcpServers": {
    "free-api-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "LOG_LEVEL": "INFO",
        "ENABLE_LOGGING": "true",
        "DEFAULT_TIMEOUT": "5",
        "NEWS_API_KEY": "your_news_api_key",
        "WEATHER_API_KEY": "your_weather_api_key"
      }
    }
  }
}
```

### 3. 验证配置

启动MCP服务器验证配置：
```bash
uv run python -m src.main
```

如果看到类似以下输出，说明配置成功：
```
INFO - 正在启动 Free API MCP Server...
INFO - 日志级别: INFO
INFO - 默认超时: 5秒
```

## 🔧 可用工具

配置成功后，你可以使用以下15个工具：

### IP信息查询
- `query_ip_location(ip_or_domain)` - 基本IP归属地查询
- `query_ip_detailed_info(ip_or_domain)` - 详细IP信息查询
- `check_ip_security(ip_address)` - IP安全检查
- `analyze_ip_comprehensive(ip_or_domain)` - IP综合分析

### 加密货币和汇率
- `query_crypto_price(crypto_symbol, vs_currency)` - 加密货币价格查询
- `query_exchange_rate(from_currency, to_currency, amount)` - 汇率转换
- `list_supported_currencies()` - 支持的货币列表

### 内容服务
- `fetch_inspirational_quote()` - 获取励志名言
- `fetch_random_joke()` - 获取随机笑话
- `fetch_daily_motivation(content_type)` - 每日励志内容

### 新闻天气
- `get_china_news(limit)` - 获取中国新闻
- `get_weather(city)` - 查询城市天气

### 系统工具
- `health_check()` - 健康检查
- `reset_failed_endpoints(service_name)` - 重置失败端点

## 📝 使用示例

```
# IP查询
query_ip_location("8.8.8.8")
check_ip_security("192.168.1.1")

# 加密货币价格
query_crypto_price("bitcoin", "usd")
query_crypto_price("ethereum", "cny")

# 汇率转换
query_exchange_rate("USD", "CNY", 100)
list_supported_currencies()

# 内容服务
fetch_inspirational_quote()
fetch_random_joke()

# 新闻天气
get_china_news(5)
get_weather("北京")

# 系统工具
health_check()
```

## ⚠️ 注意事项

1. **工具权限**: 工具的启用/禁用需要在MCP客户端中配置
2. **API密钥**: 新闻和天气服务需要API密钥才能正常工作
3. **网络连接**: 所有服务都需要互联网连接
4. **备用机制**: 服务具有多重备用机制，即使部分API失败也能正常工作

## 🔍 故障排除

### 服务器无法启动
- 检查 `uv` 是否已安装
- 运行 `uv sync` 安装依赖
- 验证项目路径是否正确

### 工具调用失败
- 检查网络连接
- 查看服务器日志输出
- 运行 `health_check()` 检查服务状态

### API服务异常
- 大部分服务有备用机制，会自动切换
- 可以运行 `reset_failed_endpoints()` 重置失败的端点
- 检查是否需要配置API密钥

---

更多详细信息请参考 [MCP_CONFIGURATION.md](MCP_CONFIGURATION.md)。