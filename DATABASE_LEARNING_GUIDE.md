# 数据库学习与实战指南

本文档旨在为量化交易开发者提供数据库基础知识、常用数据库技术以及在量化交易场景中的实际应用指南。

## 1. 数据库基础

### 1.1 什么是数据库
数据库是按照数据结构来组织、存储和管理数据的仓库。在量化交易系统中，数据库用于存储行情数据、交易记录、策略配置等核心资产。

### 1.2 数据库类型
主要分为两大类：
*   **关系型数据库 (RDBMS)**: 使用表格结构存储数据，支持 SQL 语言。
    *   代表：MySQL, PostgreSQL, SQLite, Oracle.
    *   特点：数据一致性高 (ACID)，支持复杂查询 (JOIN)，结构化强。
*   **非关系型数据库 (NoSQL)**: 不使用表格结构，模型多样。
    *   **键值存储 (Key-Value)**: Redis (高性能缓存)。
    *   **文档存储 (Document)**: MongoDB (灵活的 JSON 结构)。
    *   **时序数据库 (Time Series)**: InfluxDB, TimescaleDB, DolphinDB (专为时间序列数据优化)。
    *   **列式存储**: ClickHouse (大数据分析)。

### 1.3 核心概念 (ACID)
关系型数据库事务的四个特性：
*   **Atomicity (原子性)**: 事务中的操作要么全部完成，要么全部不完成。
*   **Consistency (一致性)**: 事务开始前后，数据库状态保持一致。
*   **Isolation (隔离性)**: 并发事务之间互不干扰。
*   **Durability (持久性)**: 事务提交后，修改是永久的。

---

## 2. 关系型数据库 (SQL)

在量化系统中，通常用于存储**用户信息、账户资金、交易订单、策略配置**等对一致性要求高的数据。

### 2.1 常用 SQL 语法
以 MySQL/PostgreSQL 为例：

```sql
-- 创建表
CREATE TABLE stock_daily (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    volume BIGINT
);

-- 插入数据
INSERT INTO stock_daily (symbol, trade_date, open_price, close_price, volume)
VALUES ('AAPL', '2023-01-01', 150.00, 155.00, 1000000);

-- 查询数据
SELECT symbol, close_price FROM stock_daily 
WHERE trade_date > '2023-01-01' AND close_price > 100
ORDER BY trade_date DESC;

-- 更新数据
UPDATE stock_daily SET volume = 2000000 WHERE symbol = 'AAPL';

-- 删除数据
DELETE FROM stock_daily WHERE id = 1;
```

### 2.2 索引与优化
*   **索引 (Index)**: 加快查询速度，但会降低写入速度。
    *   `CREATE INDEX idx_symbol_date ON stock_daily(symbol, trade_date);`
*   **优化建议**:
    *   避免 `SELECT *`，只查询需要的列。
    *   在 `WHERE`, `JOIN`, `ORDER BY` 的字段上建立索引。
    *   大批量插入时使用批量提交 (Batch Insert)。

---

## 3. 时序数据库 (Time Series Database)

量化交易的核心是**行情数据 (Tick, Bar/K线)**，这类数据带有时间戳，且写入量巨大，查询多为按时间范围聚合。

### 3.1 为什么需要时序数据库？
*   **高写入吞吐**: 每秒处理数万甚至数百万个数据点。
*   **高压缩率**: 专门针对时间序列压缩算法 (如 Gorilla)，节省存储空间。
*   **时间聚合查询**: 快速计算 `mean`, `max`, `min` (例如将 Tick 合成 1分钟 K线)。

### 3.2 常用时序数据库
*   **InfluxDB**: 流行度高，生态好，使用 InfluxQL 或 Flux 查询语言。
*   **TimescaleDB**: 基于 PostgreSQL 开发，完全兼容 SQL，适合既需要关系型特性又需要时序特性的场景。
*   **DolphinDB / KDB+**: 金融领域专用，性能极致，通常用于高频交易。

---

## 4. 键值数据库 (Redis)

### 4.1 应用场景
*   **高速缓存**: 缓存实时行情快照 (Snapshot)。
*   **消息队列**: 使用 Pub/Sub 机制分发实时行情。
*   **分布式锁**: 保证多进程交易系统不重复下单。

### 4.2 常用命令
```bash
SET stock:AAPL:price 150.50
GET stock:AAPL:price
HSET order:1001 symbol "AAPL" price 150 qty 100
HGETALL order:1001
```

---

## 5. Python 数据库实战

### 5.1 使用 SQLAlchemy (ORM) 操作 MySQL
ORM (对象关系映射) 允许用 Python 类操作数据库，无需手写 SQL。

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接数据库
engine = create_engine('mysql+pymysql://user:password@localhost/quant_db')
Base = declarative_base()

# 定义模型
class StockDaily(Base):
    __tablename__ = 'stock_daily'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10))
    trade_date = Column(Date)
    close = Column(Float)

# 创建表
Base.metadata.create_all(engine)

# 插入数据
Session = sessionmaker(bind=engine)
session = Session()
new_data = StockDaily(symbol='AAPL', trade_date='2023-10-01', close=170.5)
session.add(new_data)
session.commit()
```

### 5.2 使用 Pandas 读写数据库
Pandas 是量化分析的神器，内置了高效的 SQL 读写功能。

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost/quant_db')

# 1. 将 DataFrame 写入数据库
df = pd.DataFrame({
    'symbol': ['AAPL', 'GOOG'],
    'price': [150.0, 2800.0]
})
df.to_sql('current_prices', engine, if_exists='replace', index=False)

# 2. 从数据库读取数据到 DataFrame
df_read = pd.read_sql("SELECT * FROM stock_daily WHERE symbol='AAPL'", engine)
print(df_read.head())
```

---

## 6. 量化交易系统数据库架构设计

一个成熟的量化系统通常采用**混合数据库架构**：

| 数据类型 | 推荐数据库 | 原因 |
| :--- | :--- | :--- |
| **历史行情 (Tick/K线)** | **TimescaleDB / InfluxDB** | 海量数据存储、高压缩、时间聚合查询快 |
| **实时行情快照** | **Redis** | 内存读写，微秒级延迟，供策略实时读取 |
| **交易账户/订单/持仓** | **PostgreSQL / MySQL** | 强一致性 (ACID)，确保资金数据准确无误 |
| **非结构化数据 (新闻/公告)** | **MongoDB / Elasticsearch** | 灵活的文档结构，支持全文检索 |

### 6.1 最佳实践
1.  **读写分离**: 策略回测读取历史库，实盘交易读取实时库。
2.  **冷热分离**: 最近 1 个月的数据放在 SSD (热数据)，几年前的数据归档到 HDD 或 S3 (冷数据)。
3.  **数据清洗**: 入库前必须进行清洗 (去重、异常值处理)，保证数据质量 ("Garbage In, Garbage Out")。
4.  **备份策略**: 每日定时备份交易数据，行情数据可按月归档。

---

## 7. 学习资源推荐

*   **SQL**: [SQLZoo](https://sqlzoo.net/), [W3Schools SQL](https://www.w3schools.com/sql/)
*   **Redis**: [Redis 官方文档](https://redis.io/docs/)
*   **TimescaleDB**: [TimescaleDB Documentation](https://docs.timescale.com/)
*   **SQLAlchemy**: [SQLAlchemy 1.4/2.0 Documentation](https://docs.sqlalchemy.org/)
