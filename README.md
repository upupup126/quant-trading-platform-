# 量化交易平台

一个功能完整的量化交易软件，支持股票、期货、加密货币的实时行情展示、策略编写、回测和模拟交易。

## 🚀 功能特性

### 📊 行情展示
- **实时K线图**：支持1分钟、5分钟、15分钟、1小时、日K等多周期K线
- **盘口数据**：实时显示买卖盘口深度数据
- **涨跌排行**：按涨跌幅、成交量、成交额等维度排行
- **技术指标**：支持MA、MACD、RSI、KDJ、BOLL等常用技术指标

### 📈 策略管理
- **策略编辑器**：基于Monaco Editor的代码编辑器，支持Python策略编写
- **参数配置**：可视化调整策略参数，支持参数优化
- **策略库管理**：策略的创建、编辑、删除、导入导出功能

### 🔄 回测功能
- **历史数据回测**：使用历史数据验证策略收益
- **绩效指标**：胜率、最大回撤、夏普比率等关键指标
- **交易明细**：详细展示每笔交易的详细信息
- **资金曲线**：可视化展示策略的资金变化曲线

### 💰 模拟交易
- **虚拟账户**：支持创建多个虚拟账户进行模拟交易
- **实时模拟**：基于实时行情进行模拟交易执行
- **风险控制**：支持止损止盈、仓位控制等风险管理
- **交易监控**：实时监控策略的实盘表现

### 📋 资产监控
- **资金明细**：展示账户资金变动明细和统计
- **持仓情况**：实时显示持仓盈亏和风险暴露
- **收益曲线**：展示账户收益变化曲线和对比分析

## 🏗️ 技术架构

### 前端技术栈
- **框架**：React 18 + TypeScript
- **状态管理**：Redux Toolkit + RTK Query
- **UI组件**：Ant Design
- **图表库**：ECharts + AntV G2
- **代码编辑器**：Monaco Editor
- **构建工具**：Vite

### 后端技术栈
- **框架**：FastAPI + Python 3.9+
- **数据库**：SQLite（开发）/ PostgreSQL（生产）
- **缓存**：Redis
- **任务队列**：Celery
- **数据计算**：Pandas + NumPy

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端展示层     │    │   业务逻辑层     │    │   数据服务层     │
│                 │    │                 │    │                 │
│ • React应用     │◄──►│ • FastAPI服务   │◄──►│ • 数据采集      │
│ • 图表组件      │    │ • 策略引擎      │    │ • 数据存储      │
│ • 交易界面      │    │ • 回测引擎      │    │ • 缓存服务      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 项目结构

```
quant-trading-platform/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # 通用组件
│   │   ├── pages/           # 页面组件
│   │   ├── store/           # 状态管理
│   │   ├── services/        # API服务
│   │   └── types/           # TypeScript类型
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务服务
│   │   └── core/           # 核心模块
│   ├── requirements.txt
│   └── main.py
├── data/                    # 数据目录
├── docs/                   # 项目文档
└── docker/                 # Docker配置
```

## 🚀 部署指南

### 🛠️ 开发环境搭建

#### 1. 环境准备
- **Node.js**: v16 或更高版本
- **Python**: v3.9 或更高版本
- **Redis**: v6+ (可选，用于缓存和任务队列)
- **Git**: 版本控制工具

#### 2. 后端服务启动
```bash
# 1. 进入后端目录
cd backend

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 .\venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量 (可选)
# cp .env.example .env
# 编辑 .env 文件配置数据库和API密钥

# 5. 启动开发服务器
python main.py
# 或使用 uvicorn 热重载
uvicorn main:app --reload
```
后端服务将在 `http://localhost:8000` 启动，API文档位于 `/docs`。

#### 3. 前端服务启动
```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```
前端应用将在 `http://localhost:3000` 启动。

---

### 📦 生产环境部署

#### 1. Docker 容器化部署 (推荐)

项目提供了完整的 Docker 支持，这是最简单的部署方式。

```bash
# 1. 构建并启动所有服务
docker-compose up -d --build

# 2. 查看服务状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f
```

#### 2. 手动部署

**前端构建**
```bash
cd frontend
npm run build
# 构建产物位于 dist/ 目录，可使用 Nginx 进行托管
```

**Nginx 配置示例**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**后端部署**
建议使用 Gunicorn 作为生产环境服务器：

```bash
cd backend
source venv/bin/activate
pip install gunicorn

# 启动 Gunicorn 服务 (4个工作进程)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --daemon
```

### 📜 自动化脚本

项目在 `scripts/` 目录下提供了便捷的维护脚本：

- `deploy.sh`: 自动化部署脚本
  ```bash
  ./scripts/deploy.sh dev   # 部署开发环境
  ./scripts/deploy.sh prod  # 部署生产环境
  ```
- `start.sh`: 快速启动服务
- `stop.sh`: 停止所有服务

## 📈 A股数据获取配置

### 数据源介绍

本平台支持两种主要的A股数据获取方式：

1. **Tushare（推荐）**
   - 免费版提供基础的日线数据和部分分钟线数据
   - 需要注册获取API token
   - 适合获取实时数据和更多维度的数据

2. **BaoStock（免费）**
   - 完全免费，无需注册
   - 提供完整的历史数据批量下载
   - 适合获取大量历史数据

### 配置步骤

#### 1. 环境变量配置

复制环境配置文件并添加Tushare token：

```bash
# 复制环境配置模板
cp .env.example .env

# 编辑.env文件，添加以下配置
TUSHARE_TOKEN=your_tushare_token_here
```

#### 2. 获取Tushare Token

1. 访问 [Tushare Pro官网](https://tushare.pro)
2. 注册账号并登录
3. 在个人中心获取API Token
4. 将Token添加到.env文件中

#### 3. 安装数据采集依赖

确保已安装以下Python包（已在requirements.txt中）：
```bash
# 如果手动安装
pip install tushare baostock pandas
```

### 使用示例

#### 使用Tushare获取A股数据

```python
from app.services.data_collector import DataCollector
from app.core.database import SessionLocal
import asyncio

async def collect_a_share_data():
    db = SessionLocal()
    async with DataCollector(db) as collector:
        # 获取上证指数数据
        data = await collector.fetch_tushare_data(
            symbol="000001.SH",
            start_date="20240101",
            end_date="20241231",
            freq="D"  # 日线数据
        )
        
        if data is not None:
            print(f"获取到{len(data)}条数据")
            print(data.head())

# 运行
asyncio.run(collect_a_share_data())
```

#### 使用BaoStock批量下载历史数据

```python
from app.services.data_collector import DataCollector
from app.core.database import SessionLocal
import asyncio

async def download_history_data():
    db = SessionLocal()
    async with DataCollector(db) as collector:
        # 批量下载多只股票的历史数据
        symbols = ["000001.SZ", "000002.SZ", "600036.SH"]
        
        results = await collector.collect_batch_data(
            symbols=symbols,
            data_source="baostock",
            start_date="2020-01-01",
            end_date="2024-12-31",
            frequency="d"  # 日线数据
        )
        
        print("下载结果:", results)

# 运行
asyncio.run(download_history_data())
```

#### 使用示例脚本

平台提供了专门的示例脚本：

```bash
# 进入backend目录
cd backend

# 运行A股数据采集示例
python collect_a_share_data.py
```

该脚本提供交互式菜单，可以选择：
1. Tushare数据采集
2. BaoStock历史数据下载
3. 单个功能测试

### 支持的A股数据

- **指数数据**：上证指数、深证成指、沪深300、中证500、创业板指等
- **个股数据**：A股市场所有股票
- **数据周期**：日线、周线、月线、分钟线（需权限）
- **数据字段**：开盘价、最高价、最低价、收盘价、成交量、成交额等

### 注意事项

1. **Tushare免费版限制**：
   - 日线数据：无限制
   - 分钟线数据：有一定限制
   - 访问频率：每分钟最多200次请求

2. **BaoStock使用限制**：
   - 无需API密钥，完全免费
   - 适合批量下载历史数据
   - 数据更新可能略有延迟

3. **数据存储**：
   - 采集的数据会自动保存到数据库
   - 可在行情中心页面查看历史数据
   - 支持数据导出和分析

## 📖 使用指南

### 1. 行情查看
- 在行情中心页面选择交易对和K线周期
- 查看实时K线图和盘口数据
- 使用技术指标进行技术分析

### 2. 策略开发
- 在策略管理页面创建新策略
- 使用Python编写交易逻辑
- 配置策略参数和交易规则

### 3. 策略回测
- 选择历史数据时间段进行回测
- 查看回测结果和绩效指标
- 分析交易明细和资金曲线

### 4. 模拟交易
- 创建虚拟账户并设置初始资金
- 启动策略进行实时模拟交易
- 监控交易执行和账户变化

## 🔧 开发指南

### 代码规范
- 前端：使用ESLint + Prettier进行代码规范
- 后端：遵循PEP8规范，使用Black进行格式化
- Git：遵循Conventional Commits规范

### 测试策略
- 单元测试：为每个核心功能编写测试用例
- 集成测试：测试模块间的接口和交互
- 性能测试：定期进行性能基准测试

### 部署方案
- 开发环境：使用Docker Compose进行本地部署
- 生产环境：使用云服务器和负载均衡
- 监控告警：使用Prometheus + Grafana进行监控

## 📊 性能指标

- **响应时间**：页面加载时间不超过3秒
- **数据更新**：行情数据更新延迟不超过1秒
- **回测速度**：单策略回测时间不超过5分钟（基于1年日线数据）
- **系统稳定性**：7×24小时稳定运行

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目主页：https://github.com/upupup126/quant-trading-platform-
- 问题反馈：https://github.com/yourusername/quant-trading-platform-/issues

## 🙏 致谢

感谢以下开源项目的支持：
- [React](https://reactjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Ant Design](https://ant.design/)
- [ECharts](https://echarts.apache.org/)
- [Pandas](https://pandas.pydata.org/)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！