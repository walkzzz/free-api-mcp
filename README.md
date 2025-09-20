# Free API MCP Server 🚀

一个功能丰富的免费API服务聚合器，基于Model Context Protocol (MCP)构建，提供多种实用的API服务。

## 🎉 项目状态

✅ **功能大幅扩展** - 从15个工具扩展到25个工具 (+67%增长)  
✅ **25个MCP工具** - 涵盖娱乐、实用、金融、新闻等多个领域  
✅ **完善的容错机制** - 多层备用策略确保服务稳定性  
✅ **实时数据** - 所有API服务提供最新的实时数据

### 🚀 立即可用的功能
| 服务类型 | 工具数量 | 状态 | 功能描述 |
|---------|----------|------|----------|
| 💱 金融服务 | 3个 | ✅ 完全正常 | 汇率转换、加密货币价格、货币列表 |
| 🌍 IP查询 | 4个 | ✅ 完全正常 | IP归属地、安全检查、详细信息、综合分析 |
| 📰 新闻天气 | 3个 | ✅ 完全正常 | 多国新闻、天气查询、中国新闻 |
| 💡 内容服务 | 3个 | ✅ 完全正常 | 励志名言、笑话、每日励志 |
| 🎮 娱乐服务 | 5个 | 🆕 新增 | 猫狗图片、表情包、有趣事实、历史事件 |
| 🔧 实用工具 | 5个 | 🆕 新增 | 二维码、短链接、密码生成、UUID、颜色分析 |
| 🛠️ 系统工具 | 2个 | ✅ 完全正常 | 健康检查、端点重置 |

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

### 🎮 娱乐服务 🆕 **新增**
- **随机猫咪图片**: 高质量猫咪图片，包含尺寸信息
- **随机狗狗图片**: 狗狗图片，自动识别品种信息
- **有趣事实**: 英文冷知识 + 中文事实备用库
- **随机表情包**: 热门表情包和梗图
- **历史上的今天**: 重要历史事件回顾

### 🔧 实用工具 🆕 **新增**
- **二维码生成**: 文本转二维码，支持自定义尺寸
- **短链接生成**: 长URL转短链接服务
- **随机密码生成**: 安全密码生成，强度评估
- **UUID生成**: 唯一标识符生成，支持多版本
- **颜色分析**: 十六进制颜色信息分析

### 📰 新闻天气 ✅ **全部正常**
- **多国新闻热点**: 支持美国、英国、加拿大等16个国家的新闻
- **中国新闻查询**: 专门的中国新闻接口（可能受API限制）
- **城市天气查询**: 支持中文城市名称，返回详细天气信息
- **实时数据**: 温度、湿度、体感温度等完整信息

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

# 测试所有服务 (可选)
uv run python -c "
from src.main import health_check
print('服务状态检查:')
print(health_check())
"

# 启动MCP服务器
uv run python -m src.main
```

### 🎯 一分钟测试
```bash
# 测试汇率转换
uv run python -c "from src.main import query_exchange_rate; print(query_exchange_rate('USD', 'CNY', 100))"

# 测试加密货币价格
uv run python -c "from src.main import query_crypto_price; print(query_crypto_price('bitcoin', 'usd'))"

# 测试天气查询
uv run python -c "from src.main import get_weather; print(get_weather('北京'))"

# 测试新闻服务
uv run python -c "from src.main import get_news_by_country; print(get_news_by_country('us', 2))"
```

### 环境变量配置 (可选)
```bash
# API密钥配置 (已有默认密钥，可选覆盖)
export NEWS_API_KEY="your_news_api_key"
export WEATHER_API_KEY="your_weather_api_key"

# 日志配置
export LOG_LEVEL="INFO"
export ENABLE_LOGGING="true"

# 性能配置
export DEFAULT_TIMEOUT="5"
export MAX_RETRIES="2"
```

**注意**: 项目已内置有效的API密钥，无需额外配置即可使用所有功能。

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
│       ├── exchange_service.py   # 汇率服务
│       ├── entertainment_service.py  # 🆕 娱乐服务
│       └── utility_service.py    # 🆕 实用工具服务
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

## 🔌 MCP工具列表 (25个工具全部可用)

### IP信息查询 ✅
- `query_ip_location(ip_or_domain)` - 基本IP归属地查询
- `query_ip_detailed_info(ip_or_domain)` - 详细IP信息查询
- `check_ip_security(ip_address)` - IP安全检查
- `analyze_ip_comprehensive(ip_or_domain)` - IP综合分析

### 加密货币 ✅
- `query_crypto_price(crypto_symbol, vs_currency)` - 加密货币价格查询

### 汇率转换 ✅
- `query_exchange_rate(from_currency, to_currency, amount)` - 汇率转换
- `list_supported_currencies()` - 支持的货币列表

### 内容服务 ✅
- `fetch_inspirational_quote()` - 获取励志名言
- `fetch_random_joke()` - 获取随机笑话
- `fetch_daily_motivation(content_type)` - 每日励志内容

### 新闻天气 ✅
- `get_china_news(limit)` - 获取中国新闻
- `get_news_by_country(country, limit)` - 获取指定国家新闻
- `get_weather(city)` - 查询城市天气

### 娱乐服务 🆕 **新增**
- `fetch_random_cat_image()` - 获取随机猫咪图片
- `fetch_random_dog_image()` - 获取随机狗狗图片
- `fetch_random_fact()` - 获取有趣事实
- `fetch_meme_image()` - 获取随机表情包
- `fetch_today_in_history()` - 获取历史上的今天

### 实用工具 🆕 **新增**
- `create_qr_code(text, size)` - 生成二维码
- `create_short_url(long_url)` - 生成短链接
- `create_random_password(length, include_symbols)` - 生成随机密码
- `create_uuid(version)` - 生成UUID
- `analyze_color(color_input)` - 分析颜色信息

### 系统工具 ✅
- `health_check()` - 健康检查
- `reset_failed_endpoints(service_name)` - 重置失败端点

## 📊 使用示例

```python
# IP信息查询 ✅ 全部正常
result = query_ip_location("8.8.8.8")
# 返回: "8.8.8.8（8.8.8.8）归属地：United States Virginia Ashburn｜Google LLC"

detailed = query_ip_detailed_info("google.com")
security = check_ip_security("192.168.1.1")

# 加密货币价格 ✅ 实时数据
btc_price = query_crypto_price("bitcoin", "usd")
# 返回: "BITCOIN 价格信息: 💰 当前价格: $115,584.00 📊 市值: $2,303,325,561,751 📈 24小时变化: -1.69%"

eth_cny = query_crypto_price("ethereum", "cny")

# 汇率转换 ✅ 实时汇率
usd_to_cny = query_exchange_rate("USD", "CNY", 100)
# 返回: "💱 100 USD = 711.0000 CNY 汇率: 1 USD = 7.1100 CNY 📅 更新时间: 2025-09-19"

currencies = list_supported_currencies()

# 内容服务 ✅ 英文+中文备用
quote = fetch_inspirational_quote()
# 返回: "💡 One of the oldest human needs is having someone to wonder where you are when you don't come home at night. —— Margaret Mead"

joke = fetch_random_joke()
# 返回: "😄 What kind of doctor is Dr. Pepper? A fizzician!"

motivation = fetch_daily_motivation("quote")

# 新闻天气 ✅ 实时数据
news = get_china_news(5)  # 中国新闻（可能受限）
us_news = get_news_by_country("us", 3)  # 美国新闻 ✅ 正常
# 返回: "📰 美国新闻热点: 1. Stock Market Today: Dow, Nasdaq Rise After Fed Rate Cut..."

weather = get_weather("北京")
# 返回: "北京：晴，温度 12.9℃（体感 12.2℃），湿度 73%"

# 娱乐服务 🆕 新增功能
cat_image = fetch_random_cat_image()
# 返回: "🐱 随机猫咪图片: 🖼️ 图片链接: https://cdn2.thecatapi.com/images/au1.jpg 📏 尺寸: 800x1124px"

dog_image = fetch_random_dog_image()
# 返回: "🐶 随机狗狗图片: 🖼️ 图片链接: https://images.dog.ceo/breeds/airedale/n02096051_1854.jpg 🐕 品种: Airedale"

history = fetch_today_in_history()
# 返回: "📅 历史上的今天: 1. 1969年: Apollo 11 lands on the moon..."

# 实用工具 🆕 新增功能
qr_code = create_qr_code("https://github.com/walkzzz/free-api-mcp", "200x200")
# 返回: "📱 二维码生成成功: 🖼️ 二维码链接: https://api.qrserver.com/v1/create-qr-code/..."

password = create_random_password(16, True)
# 返回: "🔐 随机密码生成: 🔑 密码: *_(sxb2x$M,wU<CD 💪 强度: 很强"

uuid_id = create_uuid(4)
# 返回: "🆔 UUID生成成功: 🔢 UUID: 82c3be47-ff63-4471-848a-94c930bb8c38"

color_info = analyze_color("FF5733")
# 返回: "🎨 颜色信息: 🏷️ 颜色名称: Outrageous Orange 🔢 十六进制: #FF5733"

# 系统工具 ✅ 监控正常
status = health_check()
# 返回所有服务状态，13个服务监控

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

## 📝 更新日志

### v2.0.0 (2025-09-20) 🎉 **重大功能扩展**
- 🚀 **功能大幅扩展**: 从15个工具扩展到25个工具 (+67%增长)
- 🆕 **娱乐服务**: 新增5个娱乐类工具（猫狗图片、表情包、历史事件、有趣事实）
- 🆕 **实用工具**: 新增5个实用工具（二维码、短链接、密码生成、UUID、颜色分析）
- 📊 **25个MCP工具**: 涵盖娱乐、实用、金融、新闻等多个领域
- 🏗️ **架构扩展**: 新增2个服务模块，保持统一的容错机制
- ✅ **全面测试**: 所有新增工具通过功能测试

### v1.0.0 (2025-09-20)
- 🎉 **重大里程碑**: 所有7个核心服务完全正常工作
- ✅ **汇率服务修复**: 修复API响应格式解析问题
- ✅ **健康检查优化**: 修复URL参数替换问题
- ✅ **加密货币服务**: 完善参数格式，支持实时价格查询
- 🆕 **新增功能**: `get_news_by_country` 支持16个国家新闻
- ✅ **天气服务**: 确认API密钥有效，支持全球城市查询
- 🔧 **容错机制**: 完善多层备用策略和本地备用内容
- 📊 **15个MCP工具**: 全部注册成功并通过测试

### 技术改进
- 修复ExchangeRate-API响应格式兼容性
- 优化健康检查中的端点参数处理
- 完善错误处理和日志记录
- 增强服务稳定性和可靠性
- 新增娱乐和实用工具服务模块
- 扩展配置管理支持更多API服务

---

**Free API MCP Server** - 让API服务更简单、更可靠！ 🎉

> 🌟 **现在就开始使用**: 25个工具开箱即用，从实用工具到娱乐内容，一应俱全！