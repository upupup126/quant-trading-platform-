# 量化交易平台开发指南

本文档为开发者提供详细的开发环境搭建、代码规范、调试技巧和部署指南。

## 🚀 快速开始

### 环境要求

- **Node.js** 16.0+ (推荐 18.0+)
- **Python** 3.9+ (推荐 3.10+)
- **Docker** 20.0+ (可选，用于容器化部署)
- **Git** 2.0+

### 一键启动开发环境

```bash
# 克隆项目
git clone <repository-url>
cd quant-trading-platform

# 一键启动开发环境
./scripts/start.sh dev

# 或者使用容器模式
./scripts/start.sh docker

# 停止服务
./scripts/stop.sh
```

## 🛠️ 开发环境搭建

### 手动搭建开发环境

#### 1. 前端开发环境

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

#### 2. 后端开发环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动API服务
python main.py

# 访问 http://localhost:8000/docs
```

### 开发工具推荐

#### 前端开发工具
- **编辑器**: VS Code + TypeScript插件
- **调试工具**: React Developer Tools
- **包管理**: pnpm (推荐) 或 npm
- **代码格式化**: Prettier + ESLint

#### 后端开发工具
- **编辑器**: VS Code + Python插件
- **调试工具**: Python Debugger (pdb)
- **API测试**: Postman 或 Insomnia
- **数据库工具**: DBeaver 或 pgAdmin

## 📁 项目结构详解

### 前端项目结构

```
frontend/
├── src/
│   ├── components/          # 通用组件
│   │   ├── common/          # 基础组件
│   │   ├── market/          # 行情组件
│   │   ├── strategy/        # 策略组件
│   │   └── trade/           # 交易组件
│   ├── pages/               # 页面组件
│   ├── services/            # API服务
│   ├── store/               # 状态管理
│   ├── types/               # TypeScript类型
│   ├── utils/               # 工具函数
│   └── hooks/               # 自定义Hooks
├── public/                  # 静态资源
└── package.json
```

### 后端项目结构

```
backend/
├── app/
│   ├── api/                # API路由
│   ├── core/               # 核心模块
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   ├── schemas/            # 数据验证
│   └── utils/              # 工具函数
├── tests/                  # 测试文件
└── main.py                # 应用入口
```

## 💻 开发工作流

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/your-feature-name

# 2. 开发前端功能
cd frontend
npm run dev

# 3. 开发后端API
cd backend
source venv/bin/activate
python main.py

# 4. 编写测试
npm test                    # 前端测试
pytest                      # 后端测试

# 5. 提交代码
git add .
git commit -m "feat: 添加新功能"

# 6. 推送到远程
git push origin feature/your-feature-name
```

### 2. 代码规范

#### 前端代码规范

```typescript
// 组件命名使用PascalCase
interface MarketDataProps {
  symbol: string;
  period: string;
}

const MarketChart: React.FC<MarketDataProps> = ({ symbol, period }) => {
  // 使用const声明变量
  const [data, setData] = useState<KLineData[]>([]);
  
  // 使用async/await处理异步
  const fetchData = async () => {
    try {
      const response = await marketService.getKLineData(symbol, period);
      setData(response.data);
    } catch (error) {
      console.error('获取数据失败:', error);
    }
  };
  
  return (
    <div className="market-chart">
      {/* JSX注释格式 */}
      {data.map(item => (
        <KLineItem key={item.timestamp} data={item} />
      ))}
    </div>
  );
};
```

#### 后端代码规范

```python
# 使用类型注解
def get_kline_data(
    symbol: str,
    period: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[KLineData]:
    """
    获取K线数据
    
    Args:
        symbol: 交易对符号
        period: K线周期
        start_time: 开始时间
        end_time: 结束时间
    
    Returns:
        K线数据列表
    """
    try:
        # 使用f-string格式化字符串
        logger.info(f"获取{symbol}的{period}K线数据")
        
        # 使用列表推导式
        return [
            KLineData.from_orm(item)
            for item in db.query(MarketData)
            .filter_by(symbol=symbol, period=period)
            .all()
        ]
    except Exception as e:
        logger.error(f"获取K线数据失败: {e}")
        raise HTTPException(status_code=500, detail="数据获取失败")
```

### 3. Git提交规范

```bash
# 功能提交
feat: 新增K线图组件

# 修复提交
fix: 修复策略执行bug

# 文档提交
docs: 更新API文档

# 样式提交
style: 调整组件样式

# 重构提交
refactor: 重构数据服务

# 测试提交
test: 添加单元测试

# 性能优化
perf: 优化图表渲染性能
```

## 🔧 调试技巧

### 前端调试

#### React组件调试

```typescript
// 使用React DevTools
import { useState, useEffect } from 'react';

const StrategyEditor: React.FC = () => {
  const [code, setCode] = useState<string>('');
  
  // 使用useEffect调试状态变化
  useEffect(() => {
    console.log('代码内容变化:', code);
  }, [code]);
  
  return (
    <div>
      <textarea 
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
    </div>
  );
};
```

#### Redux状态调试

```typescript
// 配置Redux DevTools
import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {
    market: marketReducer,
    strategy: strategyReducer,
  },
  devTools: process.env.NODE_ENV !== 'production',
});
```

### 后端调试

#### FastAPI调试

```python
# 启用调试模式
from fastapi import FastAPI

app = FastAPI(
    debug=True,
    title="量化交易平台API",
    description="API调试模式已启用"
)

# 使用日志记录
import logging

logger = logging.getLogger(__name__)

@app.get("/market/kline")
async def get_kline_data(symbol: str, period: str):
    logger.info(f"请求K线数据: symbol={symbol}, period={period}")
    
    try:
        data = await market_service.get_kline_data(symbol, period)
        logger.info(f"返回数据条数: {len(data)}")
        return data
    except Exception as e:
        logger.error(f"获取K线数据失败: {e}")
        raise
```

#### 数据库调试

```python
# 启用SQL日志
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 或者使用echo参数
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=True  # 输出SQL语句
)
```

## 🧪 测试指南

### 前端测试

```typescript
// 组件测试示例
import { render, screen } from '@testing-library/react';
import KLineChart from '../components/KLineChart';

describe('KLineChart组件', () => {
  test('渲染K线图', () => {
    const mockData = [
      { timestamp: '2023-01-01', open: 100, high: 110, low: 95, close: 105, volume: 1000 }
    ];
    
    render(<KLineChart data={mockData} period="1d" />);
    
    expect(screen.getByText('K线图')).toBeInTheDocument();
  });
});
```

### 后端测试

```python
# API接口测试示例
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_kline_data():
    response = client.get("/api/market/kline/BTCUSDT?period=1d")
    
    assert response.status_code == 200
    assert "timestamp" in response.json()[0]
    assert "open" in response.json()[0]
```

## 📊 性能优化

### 前端性能优化

```typescript
// 使用React.memo优化组件渲染
const KLineChart = React.memo(({ data, period }: KLineChartProps) => {
  // 组件实现
});

// 使用useMemo缓存计算结果
const processedData = useMemo(() => {
  return data.map(item => ({
    ...item,
    change: ((item.close - item.open) / item.open) * 100
  }));
}, [data]);

// 使用useCallback缓存函数
const handlePeriodChange = useCallback((period: string) => {
  setSelectedPeriod(period);
}, []);
```

### 后端性能优化

```python
# 使用数据库连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)

# 使用Redis缓存
import redis
from redis_lru import RedisLRU

redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = RedisLRU(redis_client, default_ttl=300)

@cache
async def get_cached_kline_data(symbol: str, period: str):
    return await market_service.get_kline_data(symbol, period)
```

## 🚀 部署指南

### 开发环境部署

```bash
# 使用Docker Compose部署开发环境
docker-compose -f docker-compose.dev.yml up -d

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f backend
```

### 生产环境部署

```bash
# 构建生产镜像
docker-compose -f docker-compose.prod.yml build

# 启动生产服务
docker-compose -f docker-compose.prod.yml up -d

# 执行数据库迁移
docker-compose exec backend alembic upgrade head

# 健康检查
curl http://localhost:8000/health
```

## 🔍 常见问题

### Q: 前端启动失败
**A:** 检查Node.js版本和依赖安装
```bash
node --version  # 确保版本 >= 16.0
npm install     # 重新安装依赖
```

### Q: 后端启动失败
**A:** 检查Python环境和依赖
```bash
python --version  # 确保版本 >= 3.9
pip install -r requirements.txt  # 重新安装依赖
```

### Q: 数据库连接失败
**A:** 检查数据库服务和连接配置
```bash
# 检查PostgreSQL服务
sudo systemctl status postgresql

# 检查连接配置
cat .env | grep DATABASE
```

### Q: 跨域问题
**A:** 配置CORS中间件
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 学习资源

### 前端学习资源
- [React官方文档](https://reactjs.org/)
- [TypeScript手册](https://www.typescriptlang.org/docs/)
- [Ant Design组件库](https://ant.design/)

### 后端学习资源
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM指南](https://docs.sqlalchemy.org/)
- [Python异步编程](https://docs.python.org/3/library/asyncio.html)

### 量化交易学习资源
- [量化投资基础](https://www.quantconnect.com/docs/)
- [技术分析指标](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [金融市场数据API](https://www.alphavantage.co/documentation/)

---

💡 **提示**: 如果在开发过程中遇到问题，请查看项目文档或提交Issue。