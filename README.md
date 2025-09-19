# Free API MCP Server 🚀

一个功能丰富的免费API服务聚合器，基于Model Context Protocol (MCP)构建，提供多种实用的API服务。

## ✨ 功能特性

### 🌍 IP信息查询
- **基本归属地查询**: IP地址和域名的地理位置信息
- **详细信息查询**: 包含坐标、时区、ISP、AS号等详细信息
- **安全威胁检查**: 基于规则的IP威胁检测
- **综合分析报告**: 整合地理位置和安全信息的完整报告

### 💰 加密货币价格
- **实时价格查询**: 支持主流加密货币价格查询
- **多货币对比**: 支持USD、CNY等多种法币对比
- **市值信息**: 显示市值和24小时价格变化
- **多数据源**: CoinGecko、CoinCap、CryptoCompare多重备用

### 💱 汇率转换
- **20种主要货币**: 支持USD、EUR、CNY、JPY等主要货币
- **实时汇率**: 获取最新的汇率信息
- **自定义金额**: 支持任意金额的货币转换
- **本地备用**: 当API不可用时使用本地备用汇率

### 📝 内容服务
- **励志名言**: 英文名言API + 中文名言备用库
- **随机笑话**: 英文笑话API + 中文笑话备用库
- **每日励志**: 支持名言和笑话两种类型

### 📰 新闻天气
- **中国新闻热点**: 获取国内最新新闻
- **城市天气查询**: 支持中文城市名称，返回详细天气信息
- **多语言支持**: 中文界面和数据展示

### 🔧 系统工具
- **健康检查**: 监控所有API服务状态
- **失败端点重置**: 重置失败的API端点
- **详细日志**: 完整的请求和错误日志

## 🏗️ 技术架构

### 核心特性
- **统一错误处理**: 标准化的错误信息和日志记录
- **备用端点管理**: 自动切换失败的API端点
- **HTTP连接池**: 优化的网络请求性能
- **配置管理**: 灵活的环境变量和配置支持

### 容错机制
- **多端点备用**: 每个服务都有多个备用API端点
- **本地备用内容**: 当所有API都失败时使用本地内容
- **自动重试**: 智能的重试和超时机制
- **优雅降级**: 服务不可用时的友好错误提示

## 📦 安装和使用

### 环境要求
- Python 3.13+
- uv (推荐的包管理工具)

### 快速开始
```bash
# 克隆项目
git clone <repository-url>
cd free-api-mcp

# 安装依赖
uv sync

# 启动服务
uv run python -m src.main
```

### 环境变量配置
```bash
# API密钥配置
export NEWS_API_KEY="your_news_api_key"
export WEATHER_API_KEY="your_weather_api_key"

# 日志配置
export LOG_LEVEL="INFO"
export ENABLE_LOGGING="true"

# 性能配置
export DEFAULT_TIMEOUT="5"
export MAX_RETRIES="2"
```

## 📁 项目结构

```
free-api-mcp/
├── src/                          # 源代码目录
│   ├── main.py                   # 主入口文件
│   ├── core/                     # 核心模块
│   │   ├── config.py             # 配置管理
│   │   ├── error_handler.py      # 错误处理
│   │   ├── fallback_manager.py   # 备用端点管理
│   │   └── http_client.py        # HTTP客户端
│   └── services/                 # API服务模块
│       ├── ip_service.py         # IP信息服务
│       ├── crypto_service.py     # 加密货币服务
│       ├── content_service.py    # 内容服务
│       └── exchange_service.py   # 汇率服务
├── tests/                        # 测试文件
├── .kiro/specs/                  # 功能规格文档
├── pyproject.toml                # 项目配置
└── README.md                     # 项目说明
```

## 🧪 测试

项目包含完整的测试套件：

```bash
# 运行所有测试
uv run python -m pytest tests/

# 运行特定功能测试
uv run python tests/test_crypto_unit.py
uv run python tests/test_exchange_rate_unit.py
uv run python tests/test_enhanced_ip_unit.py

# 运行回归测试
uv run python tests/test_regression.py
```

## 🔌 MCP工具列表

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

## 📊 使用示例

```python
# IP信息查询
result = query_ip_location("8.8.8.8")
detailed = query_ip_detailed_info("google.com")
security = check_ip_security("192.168.1.1")

# 加密货币价格
btc_price = query_crypto_price("bitcoin", "usd")
eth_cny = query_crypto_price("ethereum", "cny")

# 汇率转换
usd_to_cny = query_exchange_rate("USD", "CNY", 100)
currencies = list_supported_currencies()

# 内容服务
quote = fetch_inspirational_quote()
joke = fetch_random_joke()
motivation = fetch_daily_motivation("quote")

# 新闻天气
news = get_china_news(5)
weather = get_weather("北京")

# 系统工具
status = health_check()
reset = reset_failed_endpoints("cryptocurrency")
```

## 🛠️ 扩展开发

### 添加新的API服务

1. 在 `src/services/` 创建新服务文件
2. 实现服务函数，遵循错误处理模式
3. 在 `src/main.py` 添加MCP工具装饰器
4. 在配置中添加服务端点
5. 编写测试文件

### 配置管理

所有配置都在 `src/core/config.py` 中管理：
- API端点配置
- 超时和重试设置
- API密钥管理
- 日志配置

## 📈 性能特性

- **连接池**: HTTP连接复用，提高请求效率
- **并发支持**: 支持多个并发请求
- **智能缓存**: 减少重复API调用
- **超时控制**: 防止长时间等待
- **资源管理**: 自动清理和释放资源

## 🔒 安全特性

- **输入验证**: 严格的参数验证
- **错误隐藏**: 不暴露敏感的内部信息
- **API密钥保护**: 安全的密钥管理
- **威胁检测**: IP安全威胁检查

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 编写代码和测试
4. 提交 Pull Request
5. 代码审查和合并

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🙏 致谢

感谢所有提供免费API服务的平台：
- IP-API.com
- CoinGecko
- OpenWeatherMap
- NewsAPI
- Quotable
- JokeAPI
- ExchangeRate-API

---

**Free API MCP Server** - 让API服务更简单、更可靠！ 🎉