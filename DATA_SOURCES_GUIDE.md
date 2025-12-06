# 量化交易平台 - 行情数据获取指南

## 📊 概述

本文档详细说明量化交易平台的行情数据获取方案，包括免费和付费数据源的配置、使用方法和最佳实践。

## 🚀 快速开始

### 1. 基础数据获取（无需配置）

```python
# 使用内置的示例数据快速开始
from app.services.data_collector import DataCollector
from app.core.database import SessionLocal

async def get_sample_data():
    db = SessionLocal()
    
    async with DataCollector(db) as collector:
        # 获取示例股票数据
        aapl_data = await collector.fetch_yahoo_data("AAPL")
        
        # 获取示例加密货币数据
        btc_data = await collector.fetch_binance_data("BTCUSDT")
        
        # 保存到数据库
        if aapl_data:
            await collector.save_market_data("AAPL", aapl_data)
        
        if btc_data:
            await collector.save_market_data("BTCUSDT", btc_data)
    
    db.close()

# 运行示例
import asyncio
asyncio.run(get_sample_data())
```

### 2. API调用示例

```python
# 通过API获取数据
import requests

# 获取K线数据
response = requests.get("http://localhost:8000/api/market/kline/AAPL?period=1d&limit=1000")
kline_data = response.json()

# 获取盘口数据
response = requests.get("http://localhost:8000/api/market/orderbook/BTCUSDT?depth=10")
orderbook_data = response.json()

# 获取行情列表
response = requests.get("http://localhost:8000/api/market/tickers?market_type=stock&limit=50")
tickers_data = response.json()
```

## 🔧 数据源配置

### 1. 免费数据源配置

#### Alpha Vantage（股票、外汇、加密货币）

**注册API密钥：**
1. 访问 https://www.alphavantage.co/support/#api-key
2. 注册账号获取免费API密钥
3. 每日限制：500次请求

**配置方法：**
```bash
# 环境变量配置
export ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

**使用示例：**
```python
from app.services.data_collector import DataCollector

async def get_alpha_vantage_data():
    async with DataCollector(db) as collector:
        # 获取股票数据
        data = await collector.fetch_alpha_vantage_data("AAPL", "TIME_SERIES_DAILY")
        
        # 获取加密货币数据
        crypto_data = await collector.fetch_alpha_vantage_data("BTC", "DIGITAL_CURRENCY_DAILY")
```

#### Yahoo Finance（股票、ETF、基金）

**无需API密钥，直接使用：**
```bash
# 安装依赖
pip install yfinance
```

**使用示例：**
```python
from app.services.data_collector import DataCollector

async def get_yahoo_data():
    async with DataCollector(db) as collector:
        # 获取股票数据
        data = await collector.fetch_yahoo_data("AAPL", period="1mo")
        
        # 获取指数数据
        index_data = await collector.fetch_yahoo_data("^GSPC")  # S&P 500
```

#### Binance（加密货币）

**API密钥（可选，用于更高频率）：**
1. 访问 https://www.binance.com/en/my/settings/api-management
2. 创建API密钥
3. 设置IP白名单

**配置方法：**
```bash
# 环境变量配置
export BINANCE_API_KEY="your_api_key"
export BINANCE_SECRET_KEY="your_secret_key"
```

**使用示例：**
```python
from app.services.data_collector import DataCollector

async def get_binance_data():
    async with DataCollector(db) as collector:
        # 获取K线数据
        kline_data = await collector.fetch_binance_data("BTCUSDT", "1d", 1000)
        
        # 批量获取多个交易对
        symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
        results = await collector.collect_batch_data(symbols, "binance")
```

### 2. 中文数据源配置

#### Tushare（A股数据）

**注册API密钥：**
1. 访问 https://tushare.pro/
2. 注册账号获取API密钥
3. 免费版有积分限制

**配置方法：**
```bash
# 环境变量配置
export TUSHARE_API_KEY="your_tushare_token"
```

**使用示例：**
```python
from app.services.data_collector import DataCollector

async def get_tushare_data():
    async with DataCollector(db) as collector:
        # 获取A股数据
        data = await collector.fetch_tushare_data("000001.SH", "20200101", "20231231")
        
        # 获取股票列表
        import tushare as ts
        ts.set_token("your_token")
        stock_list = ts.get_stock_basics()
```

#### AKShare（中文金融数据）

**无需API密钥：**
```bash
# 安装依赖
pip install akshare
```

**使用示例：**
```python
import akshare as ak

# 获取A股实时行情
stock_zh_a_spot_df = ak.stock_zh_a_spot()

# 获取指数数据
index_data = ak.stock_zh_index_spot()

# 获取基金数据
fund_data = ak.fund_em_open_fund_daily()
```

### 3. 付费数据源配置

#### Wind（专业金融数据）

**获取API密钥：**
1. 联系Wind客户经理
2. 购买API服务
3. 获取用户名和密码

**配置方法：**
```bash
# 环境变量配置
export WIND_API_KEY="your_wind_api_key"
export WIND_USERNAME="your_username"
export WIND_PASSWORD="your_password"
```

## 📈 数据获取策略

### 1. 历史数据获取

```python
from datetime import datetime, timedelta
from app.services.data_collector import DataCollector

async def get_historical_data():
    """获取历史数据"""
    async with DataCollector(db) as collector:
        
        # 定义时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 1年数据
        
        # 股票列表
        stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
        
        # 批量获取数据
        for stock in stocks:
            data = await collector.fetch_yahoo_data(stock, period="1y")
            if data:
                await collector.save_market_data(stock, data)
                print(f"已保存 {stock} 的历史数据")
```

### 2. 实时数据获取

```python
import asyncio
from app.services.data_collector import DataCollector

async def start_realtime_collection():
    """启动实时数据采集"""
    async with DataCollector(db) as collector:
        
        # 监控的交易对
        symbols = ["BTCUSDT", "ETHUSDT", "AAPL", "GOOGL"]
        
        # 启动实时采集
        await collector.start_realtime_collection(symbols)
        
        # 持续运行
        while True:
            await asyncio.sleep(60)  # 每分钟检查一次

# 在后台运行实时采集
async def main():
    await start_realtime_collection()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. 数据质量检查

```python
from app.services.data_collector import DataCollector

async def check_data_quality():
    """检查数据质量"""
    async with DataCollector(db) as collector:
        
        # 检查数据完整性
        symbols = ["AAPL", "BTCUSDT"]
        
        for symbol in symbols:
            # 获取最近的数据点
            latest_data = await collector.fetch_yahoo_data(symbol, period="1d")
            
            if latest_data:
                # 检查数据是否最新
                latest_timestamp = latest_data.index[-1]
                time_diff = datetime.now() - latest_timestamp
                
                if time_diff.total_seconds() > 3600:  # 超过1小时
                    print(f"警告: {symbol} 数据可能已过期")
                else:
                    print(f"{symbol} 数据正常")
```

## 🔄 数据更新策略

### 1. 定时任务配置

```python
import schedule
import time
from app.services.data_collector import DataCollector

async def scheduled_data_update():
    """定时数据更新"""
    async with DataCollector(db) as collector:
        
        # 每日更新股票数据
        stocks = ["AAPL", "GOOGL", "MSFT"]
        await collector.collect_batch_data(stocks, "yahoo")
        
        # 每小时更新加密货币数据
        cryptos = ["BTCUSDT", "ETHUSDT"]
        await collector.collect_batch_data(cryptos, "binance")

# 配置定时任务
def setup_scheduler():
    # 每天9:00更新股票数据
    schedule.every().day.at("09:00").do(
        lambda: asyncio.run(scheduled_data_update())
    )
    
    # 每小时更新加密货币数据
    schedule.every().hour.do(
        lambda: asyncio.run(scheduled_data_update())
    )
    
    # 运行调度器
    while True:
        schedule.run_pending()
        time.sleep(1)
```

### 2. 增量更新策略

```python
from datetime import datetime
from app.services.data_collector import DataCollector

async def incremental_update(symbol: str, data_source: str):
    """增量数据更新"""
    async with DataCollector(db) as collector:
        
        # 获取数据库中最新数据的时间
        latest_record = db.query(MarketData).filter(
            MarketData.symbol == symbol
        ).order_by(MarketData.timestamp.desc()).first()
        
        if latest_record:
            # 从最新时间点开始更新
            start_time = latest_record.timestamp
        else:
            # 首次获取，获取1年数据
            start_time = datetime.now() - timedelta(days=365)
        
        # 根据数据源获取增量数据
        if data_source == "yahoo":
            data = await collector.fetch_yahoo_data(symbol, period="ytd")
        elif data_source == "binance":
            data = await collector.fetch_binance_data(symbol, "1d", 365)
        
        # 过滤新数据
        if data:
            new_data = [item for item in data if item["timestamp"] > start_time]
            
            if new_data:
                await collector.save_market_data(symbol, new_data)
                print(f"已更新 {symbol} 的 {len(new_data)} 条新数据")
```

## 🛡️ 错误处理和容错机制

### 1. 数据源故障处理

```python
from app.services.data_collector import DataCollector

async def robust_data_fetch(symbol: str, primary_source: str, fallback_sources: list):
    """健壮的数据获取，支持故障转移"""
    
    sources = [primary_source] + fallback_sources
    
    for source in sources:
        try:
            async with DataCollector(db) as collector:
                
                if source == "yahoo":
                    data = await collector.fetch_yahoo_data(symbol)
                elif source == "binance":
                    data = await collector.fetch_binance_data(symbol)
                elif source == "alpha_vantage":
                    data = await collector.fetch_alpha_vantage_data(symbol)
                
                if data:
                    print(f"成功从 {source} 获取 {symbol} 数据")
                    return data
                    
        except Exception as e:
            print(f"从 {source} 获取数据失败: {e}")
            continue
    
    print(f"所有数据源都失败，无法获取 {symbol} 数据")
    return None
```

### 2. 速率限制处理

```python
import time
from app.services.data_collector import DataCollector

class RateLimitedCollector:
    """带速率限制的数据采集器"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.last_request_time = 0
        self.request_count = 0
    
    async def rate_limited_fetch(self, symbol: str, source: str):
        """带速率限制的数据获取"""
        
        # 检查速率限制
        current_time = time.time()
        if current_time - self.last_request_time < 60:
            if self.request_count >= self.requests_per_minute:
                # 等待下一分钟
                wait_time = 60 - (current_time - self.last_request_time)
                print(f"达到速率限制，等待 {wait_time:.1f} 秒")
                await asyncio.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = time.time()
        else:
            # 新的一分钟，重置计数器
            self.request_count = 0
            self.last_request_time = current_time
        
        # 执行请求
        self.request_count += 1
        
        async with DataCollector(db) as collector:
            if source == "yahoo":
                return await collector.fetch_yahoo_data(symbol)
            elif source == "binance":
                return await collector.fetch_binance_data(symbol)
```

## 📊 数据验证和清洗

### 1. 数据质量检查

```python
import pandas as pd
from app.services.data_collector import DataCollector

async def validate_data_quality(symbol: str, data_source: str):
    """验证数据质量"""
    async with DataCollector(db) as collector:
        
        data = await robust_data_fetch(symbol, data_source, ["yahoo", "binance"])
        
        if not data:
            return False
        
        # 转换为DataFrame进行验证
        df = pd.DataFrame(data)
        
        # 检查缺失值
        missing_values = df.isnull().sum()
        if missing_values.any():
            print(f"发现缺失值: {missing_values}")
        
        # 检查异常值
        price_stats = df[['open', 'high', 'low', 'close']].describe()
        
        # 检查价格合理性
        if (df['high'] < df['low']).any():
            print("发现价格异常: 最高价低于最低价")
            return False
        
        if (df['close'] > df['high']).any() or (df['close'] < df['low']).any():
            print("发现价格异常: 收盘价超出高低价范围")
            return False
        
        return True
```

## 🚀 性能优化建议

### 1. 批量数据获取

```python
from app.services.data_collector import DataCollector

async def batch_data_collection():
    """批量数据获取优化"""
    async with DataCollector(db) as collector:
        
        # 分组获取，减少API调用
        stock_groups = [
            ["AAPL", "GOOGL", "MSFT"],
            ["AMZN", "TSLA", "META"],
            ["NFLX", "NVDA", "AMD"]
        ]
        
        for group in stock_groups:
            # 批量获取一组数据
            results = await collector.collect_batch_data(group, "yahoo")
            
            # 处理结果
            for symbol, success in results.items():
                if success:
                    print(f"成功获取 {symbol} 数据")
                else:
                    print(f"获取 {symbol} 数据失败")
            
            # 组间延迟，避免触发速率限制
            await asyncio.sleep(1)
```

### 2. 数据缓存策略

```python
import redis
from datetime import datetime, timedelta

class CachedDataCollector:
    """带缓存的数据采集器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.collector = DataCollector
    
    async def get_cached_data(self, symbol: str, source: str, cache_minutes: int = 5):
        """获取缓存数据"""
        cache_key = f"{source}:{symbol}"
        
        # 检查缓存
        cached_data = self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        
        # 从数据源获取
        async with self.collector(db) as collector:
            if source == "yahoo":
                data = await collector.fetch_yahoo_data(symbol)
            elif source == "binance":
                data = await collector.fetch_binance_data(symbol)
        
        if data:
            # 缓存数据
            self.redis.setex(
                cache_key, 
                timedelta(minutes=cache_minutes), 
                json.dumps(data)
            )
        
        return data
```

## 📋 最佳实践总结

1. **数据源选择**：根据市场类型选择最合适的数据源
2. **速率限制**：遵守各数据源的API调用限制
3. **错误处理**：实现故障转移和重试机制
4. **数据验证**：定期检查数据质量和完整性
5. **性能优化**：使用批量获取和缓存策略
6. **监控告警**：设置数据更新失败的告警机制

通过以上配置和使用指南，您可以灵活地获取和管理各种金融市场的行情数据，为量化交易策略提供可靠的数据支持。