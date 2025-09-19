# Free API MCP Server - 项目结构

## 项目概述

Free API MCP Server 是一个基于 Model Context Protocol (MCP) 的免费API服务聚合器，提供多种实用的API服务，包括IP信息查询、加密货币价格、汇率转换、励志内容等。

## 目录结构

```
free-api-mcp/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── main.py                   # 主入口文件
│   ├── server.py                 # 原始服务器文件（保留）
│   ├── core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── config.py             # 配置管理
│   │   ├── error_handler.py      # 错误处理
│   │   ├── fallback_manager.py   # 备用端点管理
│   │   └── http_client.py        # HTTP客户端管理
│   └── services/                 # API服务模块
│       ├── __init__.py
│       ├── ip_service.py         # IP信息查询服务
│       ├── crypto_service.py     # 加密货币价格服务
│       ├── content_service.py    # 内容服务（名言/笑话）
│       └── exchange_service.py   # 汇率查询服务
├── tests/                        # 测试文件
│   ├── __init__.py
│   ├── test_*.py                 # 各种测试文件
│   └── ...
├── .kiro/                        # Kiro IDE 配置
│   └── specs/                    # 功能规格文档
│       └── free-api-mcp-expansion/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── pyproject.toml                # 项目配置
├── README.md                     # 项目说明
├── PROJECT_STRUCTURE.md          # 项目结构文档
├── MCP_CONFIGURATION.md          # MCP配置指南
└── uv.lock                       # 依赖锁定文件
```

## 核心模块说明

### src/core/

- **config.py**: 配置管理器，负责加载环境变量、API密钥和服务配置
- **error_handler.py**: 统一的错误处理机制，提供标准化的错误信息格式
- **fallback_manager.py**: 备用端点管理器，实现API失败时的自动切换
- **http_client.py**: HTTP客户端管理器，提供连接池和统一的请求接口

### src/services/

- **ip_service.py**: IP信息查询服务
  - 基本IP归属地查询
  - 详细IP信息查询（包含坐标、时区等）
  - IP安全威胁检查
  - IP综合分析报告

- **crypto_service.py**: 加密货币价格服务
  - 支持多种加密货币价格查询
  - 多货币对比（USD/CNY）
  - 市值和24小时变化信息

- **content_service.py**: 内容服务
  - 励志名言获取（英文+中文备用）
  - 随机笑话获取（英文+中文备用）
  - 每日励志内容

- **exchange_service.py**: 汇率查询服务
  - 支持20种主要货币转换
  - 实时汇率查询
  - 本地备用汇率机制

## 主要功能

### 1. IP信息查询
- 基本归属地查询
- 详细地理信息（坐标、时区、ISP等）
- 安全威胁检查
- 综合分析报告

### 2. 加密货币价格
- 实时价格查询
- 市值信息
- 24小时价格变化
- 多货币支持

### 3. 汇率转换
- 20种主要货币支持
- 实时汇率查询
- 自定义金额转换
- 备用汇率机制

### 4. 内容服务
- 励志名言（英文API + 中文备用）
- 随机笑话（英文API + 中文备用）
- 每日励志内容

### 5. 新闻和天气
- 中国新闻热点
- 城市天气查询
- 多语言支持

### 6. 系统工具
- 健康检查
- 失败端点重置
- 服务状态监控

## 技术特性

### 容错机制
- 多端点备用切换
- 统一错误处理
- 本地备用内容
- 自动重试机制

### 性能优化
- HTTP连接池
- 请求超时控制
- 并发请求支持
- 缓存机制

### 配置管理
- 环境变量支持
- 动态配置加载
- 服务开关控制
- 日志级别配置

### 监控和日志
- 详细的请求日志
- 性能监控
- 健康检查
- 错误追踪

## 使用方式

### 开发环境启动
```bash
# 启动服务
uv run python -m src.main
```

### 测试运行
```bash
# 运行所有测试
uv run python -m pytest tests/

# 运行特定测试
uv run python tests/test_crypto_unit.py
```

## 扩展指南

### 添加新的API服务

1. 在 `src/services/` 目录下创建新的服务文件
2. 实现服务函数，遵循现有的错误处理模式
3. 在 `src/main.py` 中添加MCP工具装饰器
4. 在 `src/core/config.py` 中添加服务配置
5. 编写相应的测试文件

### 配置新的API端点

1. 在 `ConfigManager.get_service_config()` 中添加服务配置
2. 设置主端点和备用端点
3. 配置超时和重试参数
4. 添加API密钥支持（如需要）

## 依赖管理

项目使用 `uv` 进行依赖管理：

```bash
# 安装依赖
uv sync

# 添加新依赖
uv add package_name

# 更新依赖
uv lock --upgrade
```

## 贡献指南

1. 遵循现有的代码结构和命名规范
2. 为新功能编写测试
3. 更新相关文档
4. 确保所有测试通过
5. 遵循错误处理和日志记录的最佳实践