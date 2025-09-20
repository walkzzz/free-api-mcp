# Free API MCP Server - MCP 配置指南

## 概述

Free API MCP Server 提供25个MCP工具，支持通过 Model Context Protocol (MCP) 与各种AI助手集成。本文档提供了详细的配置指南。

## 配置文件位置

### 工作区级别配置
- **路径**: `.kiro/settings/mcp.json`
- **作用域**: 仅当前项目
- **优先级**: 高（会覆盖用户级别的同名服务器）

### 用户级别配置
- **路径**: `~/.kiro/settings/mcp.json`
- **作用域**: 全局所有项目
- **优先级**: 低

## 基本配置

### 工作区配置示例

```json
{
  "mcpServers": {
    "free-api-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "PYTHONPATH": ".",
        "LOG_LEVEL": "INFO",
        "ENABLE_LOGGING": "true"
      }
    }
  }
}
```

### 用户级别配置示例

```json
{
  "mcpServers": {
    "free-api-mcp-global": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/free-api-mcp",
        "NEWS_API_KEY": "your_api_key",
        "WEATHER_API_KEY": "your_api_key"
      }
    }
  }
}
```

## 配置参数详解

### 基本参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `command` | string | ✅ | 启动命令，推荐使用 `uv` |
| `args` | array | ✅ | 命令参数 |
| `env` | object | ❌ | 环境变量配置 |

### 环境变量配置

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `PYTHONPATH` | `.` | Python模块搜索路径 |
| `LOG_LEVEL` | `INFO` | 日志级别 (DEBUG/INFO/WARNING/ERROR) |
| `ENABLE_LOGGING` | `true` | 是否启用日志记录 |
| `DEFAULT_TIMEOUT` | `5` | 默认请求超时时间（秒） |
| `MAX_RETRIES` | `2` | 最大重试次数 |
| `ENABLE_HEALTH_CHECK` | `true` | 是否启用健康检查 |
| `NEWS_API_KEY` | - | 新闻API密钥 |
| `WEATHER_API_KEY` | - | 天气API密钥 |

### 标准MCP配置

MCP配置只支持以下标准字段：
- `command`: 启动命令
- `args`: 命令参数
- `env`: 环境变量

工具管理（如自动批准、禁用工具等）需要在MCP客户端中配置，不在服务器配置文件中设置。

## 可用工具列表

### IP信息查询
- `query_ip_location(ip_or_domain)` - 基本IP归属地查询
- `query_ip_detailed_info(ip_or_domain)` - 详细IP信息查询
- `check_ip_security(ip_address)` - IP安全检查
- `analyze_ip_comprehensive(ip_or_domain)` - IP综合分析

### 加密货币
- `query_crypto_price(crypto_symbol, vs_currency)` - 加密货币价格查询

### 汇率转换
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

## 配置示例

### 开发环境配置

```json
{
  "mcpServers": {
    "free-api-mcp-dev": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "LOG_LEVEL": "DEBUG",
        "ENABLE_LOGGING": "true",
        "DEFAULT_TIMEOUT": "10"
      }
    }
  }
}
```

### 生产环境配置

```json
{
  "mcpServers": {
    "free-api-mcp-prod": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"],
      "env": {
        "LOG_LEVEL": "WARNING",
        "ENABLE_LOGGING": "true",
        "NEWS_API_KEY": "${NEWS_API_KEY}",
        "WEATHER_API_KEY": "${WEATHER_API_KEY}",
        "DEFAULT_TIMEOUT": "5",
        "MAX_RETRIES": "3"
      }
    }
  }
}
```

### 最小化配置

```json
{
  "mcpServers": {
    "free-api-mcp-minimal": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.main"]
    }
  }
}
```

## 工具管理

### 工具权限控制

工具的权限控制（如自动批准、禁用工具等）需要在MCP客户端中配置，而不是在服务器配置文件中。不同的MCP客户端可能有不同的配置方式。

### 可用工具列表

服务器提供以下15个工具，客户端可以选择性地启用或禁用：

- `query_ip_location` - 基本IP归属地查询
- `query_ip_detailed_info` - 详细IP信息查询  
- `check_ip_security` - IP安全检查
- `analyze_ip_comprehensive` - IP综合分析
- `query_crypto_price` - 加密货币价格查询
- `query_exchange_rate` - 汇率转换
- `list_supported_currencies` - 支持的货币列表
- `fetch_inspirational_quote` - 获取励志名言
- `fetch_random_joke` - 获取随机笑话
- `fetch_daily_motivation` - 每日励志内容
- `get_china_news` - 获取中国新闻
- `get_weather` - 查询城市天气
- `health_check` - 健康检查
- `reset_failed_endpoints` - 重置失败端点

## 安全建议

### API密钥管理
1. **不要在配置文件中硬编码API密钥**
2. **使用环境变量**: `"NEWS_API_KEY": "${NEWS_API_KEY}"`
3. **限制敏感工具**: 在客户端禁用 `reset_failed_endpoints` 等管理工具

## 故障排除

### 常见问题

1. **服务器无法启动**
   - 检查 `command` 和 `args` 是否正确
   - 验证 `PYTHONPATH` 环境变量设置
   - 确认项目依赖已安装 (`uv sync`)

2. **工具调用失败**
   - 检查工具名称是否正确
   - 确认工具未在 `disabledTools` 中
   - 查看日志输出

3. **API调用失败**
   - 检查网络连接
   - 验证API密钥设置
   - 查看服务健康检查结果

### 调试配置

```json
{
  "env": {
    "LOG_LEVEL": "DEBUG",
    "ENABLE_LOGGING": "true"
  }
}
```

## 配置验证

使用以下命令验证配置：

```bash
# 测试服务器启动
uv run python -m src.main

# 检查健康状态
# 在MCP客户端中调用 health_check() 工具
```

## 更新和维护

1. **定期更新**: 使用 `uv sync` 更新依赖
2. **监控日志**: 检查 `free-api-mcp.log` 文件
3. **健康检查**: 定期调用 `health_check()` 工具
4. **重置端点**: 必要时使用 `reset_failed_endpoints()` 工具

---

更多信息请参考 [README.md](README.md) 和 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)。