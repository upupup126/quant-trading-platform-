# 量化交易平台 - 后端服务

## 概述

后端服务为量化交易平台提供API接口，包括市场数据、交易信号、策略回测等功能。

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip (Python包管理器)

### 2. 安装依赖

```bash
# 克隆项目后进入后端目录
cd quant-trading-platform/backend

# 安装依赖
pip install -r requirements.txt

# 或安装核心依赖
pip install fastapi uvicorn pydantic sqlalchemy
```

### 3. 启动服务

```bash
# 方法1: 直接启动
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 方法2: 使用启动脚本
python start_server.py

# 方法3: 手动启动
python -c "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
```

### 4. 验证服务

服务启动后，访问以下链接：

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/market/health
- 市场摘要: http://localhost:8000/api/market/summary

## API端点

### 市场数据API

- `GET /api/market/summary` - 获取市场摘要
- `GET /api/market/symbols` - 获取交易对列表
- `GET /api/market/simple-kline/{symbol}` - 获取简化K线数据
- `GET /api/market/simple-orderbook/{symbol}` - 获取简化盘口数据
- `GET /api/market/kline/{symbol}` - 获取详细K线数据
- `GET /api/market/orderbook/{symbol}` - 获取详细盘口数据
- `GET /api/market/tickers` - 获取行情列表
- `GET /api/market/health` - 健康检查

## 数据库设置

当前版本使用SQLite数据库，无需额外配置。数据库文件将自动创建在 `data/` 目录下。

如需使用MySQL或PostgreSQL，请修改 `app/core/database.py` 中的配置。

## 常见问题

### 1. ModuleNotFoundError: No module named 'fastapi'

**解决方案**:
```bash
pip install fastapi
```

### 2. ModuleNotFoundError: No module named 'app.schemas'

**解决方案**:
确保已经按照项目结构创建了必要的目录和文件。如果缺少某些文件，可以重新克隆项目或手动创建缺失的文件。

### 3. 端口被占用

**解决方案**:
```bash
# 停止占用8000端口的进程
lsof -ti:8000 | xargs kill -9

# 或使用其他端口启动
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. 数据库连接错误

**解决方案**:
检查数据库配置，确保数据库服务正在运行。对于SQLite，确保有写入权限。

## 开发

### 项目结构

```
backend/
├── app/
│   ├── api/           # API路由
│   │   └── market.py  # 市场数据API
│   ├── core/          # 核心模块
│   │   └── database.py # 数据库配置
│   ├── models/        # 数据模型
│   │   └── market.py  # 市场数据模型
│   ├── schemas/       # Pydantic模型
│   │   └── market.py  # 市场数据Schemas
│   └── services/      # 业务逻辑
│       └── market_service.py # 市场数据服务
├── data/              # 数据存储目录
├── main.py           # 主应用文件
├── requirements.txt  # 依赖列表
├── start_server.py   # 启动脚本
└── README.md         # 本文档
```

### 添加新的API端点

1. 在 `app/api/` 目录下创建新的路由文件
2. 在 `app/schemas/` 目录下创建对应的Pydantic模型
3. 在 `app/services/` 目录下实现业务逻辑
4. 在 `main.py` 中注册路由

## 部署

### 生产环境

```bash
# 使用gunicorn（推荐）
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 使用docker
# 参考 Dockerfile 文件
```

## 日志管理

### 查看运行日志

#### 1. 实时控制台日志
启动服务时日志会直接显示在控制台：

```bash
# 查看实时日志
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或使用详细日志级别
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

**常见日志内容**：
- 服务启动信息
- 数据库连接状态
- API请求和响应
- 错误和异常信息

#### 2. 保存日志到文件

```bash
# 将日志保存到文件
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 2>&1 | tee app.log

# 按日期保存日志
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 2>&1 | tee "app_$(date +%Y%m%d).log"
```

#### 3. 日志级别控制

```bash
# 调试级别（最详细）
uvicorn main:app --log-level debug

# 信息级别（默认推荐）
uvicorn main:app --log-level info

# 警告级别
uvicorn main:app --log-level warning

# 错误级别
uvicorn main:app --log-level error
```

#### 4. 查看历史日志

```bash
# 查看最近的日志文件
cat app.log

# 实时查看日志文件更新
tail -f app.log

# 查看最后100行日志
tail -n 100 app.log

# 按时间筛选日志
grep "2025-12-06" app.log
```

### 常见日志问题排查

1. **查看启动错误**：
   ```bash
   # 检查启动过程中的错误
   python check_env.py
   ```

2. **查看API请求错误**：
   - 日志中会显示HTTP状态码和错误信息
   - 常见错误：404（未找到）、500（服务器错误）

3. **查看数据库错误**：
   - 连接失败时会显示数据库连接错误
   - SQL执行错误会显示具体的SQL语句和错误信息

## 支持

遇到问题请检查以下事项：

1. 依赖是否安装完整
2. 数据库是否可访问
3. 端口是否被占用
4. 文件权限是否正确
5. 查看相关日志信息

如果问题仍未解决，请提供相关日志信息并联系开发人员。