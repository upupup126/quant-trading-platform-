# Python语言学习指南

## 1. Python语言概述

### 1.1 语言特性
- **诞生年份**：1991年
- **设计目标**：易读易用，开发效率高
- **类型系统**：动态强类型
- **内存管理**：自动垃圾回收（GC）
- **并发模型**：async/await协程
- **包管理**：pip包管理器
- **性能特点**：开发效率高，执行速度中等
- **主要应用**：Web开发、数据科学、机器学习、自动化脚本

### 1.2 学习优势
- 语法简洁，学习曲线平缓
- 丰富的第三方库生态
- 跨平台兼容性好
- 社区活跃，文档完善

## 2. Python基础语法

### 2.1 变量和数据类型

```python
# 变量声明（无需指定类型）
count = 10
price = 150.0
symbol = "AAPL"
is_active = True

# 数据类型检查
type(count)      # <class 'int'>
type(price)      # <class 'float'>
type(symbol)     # <class 'str'>

# 类型转换
int("100")       # 100
str(150.0)       # "150.0"
float("3.14")    # 3.14
```

### 2.2 数据结构

**列表（List）：**
```python
# 列表定义和操作
stocks = ["AAPL", "GOOGL", "TSLA"]
prices = [150.0, 2800.0, 200.0]

# 列表操作
stocks.append("MSFT")          # 添加元素
stocks.remove("GOOGL")         # 删除元素
stocks[0]                      # 访问元素："AAPL"
len(stocks)                    # 列表长度：4

# 列表推导式
squared_prices = [price**2 for price in prices if price > 100]
```

**字典（Dictionary）：**
```python
# 字典定义
stock_info = {
    "symbol": "AAPL",
    "price": 150.0,
    "volume": 1000000,
    "exchange": "NASDAQ"
}

# 字典操作
stock_info["price"] = 155.0    # 更新值
stock_info["sector"] = "Tech"  # 添加新键
"symbol" in stock_info         # 检查键是否存在：True

# 字典推导式
price_dict = {stock: price for stock, price in zip(stocks, prices)}
```

**元组（Tuple）：**
```python
# 元组定义（不可变）
stock_tuple = ("AAPL", 150.0, "NASDAQ")
symbol, price, exchange = stock_tuple  # 元组解包
```

**集合（Set）：**
```python
# 集合定义（无序不重复）
unique_stocks = {"AAPL", "GOOGL", "TSLA", "AAPL"}  # 自动去重

# 集合操作
tech_stocks = {"AAPL", "GOOGL", "MSFT"}
finance_stocks = {"JPM", "BAC", "MSFT"}
union = tech_stocks | finance_stocks     # 并集
intersection = tech_stocks & finance_stocks  # 交集
```

### 2.3 控制结构

**条件语句：**
```python
price = 150.0

if price > 200:
    print("高价股")
elif price > 100:
    print("中价股")
else:
    print("低价股")

# 三元表达式
category = "高价股" if price > 200 else "普通股"
```

**循环结构：**
```python
# for循环
stocks = ["AAPL", "GOOGL", "TSLA"]
for stock in stocks:
    print(f"股票代码: {stock}")

# 带索引的遍历
for i, stock in enumerate(stocks):
    print(f"索引 {i}: {stock}")

# while循环
count = 0
while count < 3:
    print(f"计数: {count}")
    count += 1

# 循环控制
for stock in stocks:
    if stock == "GOOGL":
        continue  # 跳过当前迭代
    if stock == "TSLA":
        break     # 退出循环
    print(stock)
```

## 3. 函数和模块

### 3.1 函数定义

```python
def calculate_profit(price, quantity):
    """计算股票利润"""
    return price * quantity

# 带默认参数的函数
def analyze_stock(symbol, days=30, include_volume=True):
    """分析股票数据"""
    print(f"分析 {symbol} 的 {days} 天数据")
    if include_volume:
        print("包含成交量分析")

# 可变参数
def portfolio_value(*stocks):
    """计算投资组合价值"""
    total = sum(stocks)
    return total

# 关键字参数
def stock_order(symbol, price, quantity, order_type="market"):
    """股票订单函数"""
    return {
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "type": order_type
    }
```

### 3.2 高级函数特性

**Lambda表达式：**
```python
# 匿名函数
square = lambda x: x ** 2
prices = [100, 150, 200]
squared = list(map(lambda x: x**2, prices))

# 排序
stocks = [("AAPL", 150), ("GOOGL", 2800), ("TSLA", 200)]
sorted_stocks = sorted(stocks, key=lambda x: x[1])  # 按价格排序
```

**装饰器：**
```python
import time

def timer_decorator(func):
    """计时装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.2f}秒")
        return result
    return wrapper

@timer_decorator
def complex_calculation():
    """复杂计算函数"""
    time.sleep(1)
    return "计算完成"
```

### 3.3 模块和包

**模块导入：**
```python
# 基本导入
import math
import os
import sys

# 选择性导入
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# 别名导入
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 相对导入（在包内）
from . import utils
from ..models import StockModel
```

**创建模块：**
```python
# stock_analysis.py
"""股票分析模块"""

def calculate_return(initial, current):
    """计算收益率"""
    return (current - initial) / initial

def moving_average(prices, window=5):
    """计算移动平均线"""
    return sum(prices[-window:]) / window

# 模块测试代码
if __name__ == "__main__":
    print("模块测试")
```

## 4. 面向对象编程

### 4.1 类和对象

```python
class Stock:
    """股票类"""
    
    # 类属性
    market = "NASDAQ"
    
    def __init__(self, symbol, price, volume=0):
        """构造函数"""
        self.symbol = symbol      # 实例属性
        self.price = price
        self.volume = volume
        self._history = []        # 私有属性（约定）
    
    def update_price(self, new_price):
        """更新价格"""
        self._history.append(self.price)
        self.price = new_price
    
    def calculate_value(self, quantity):
        """计算价值"""
        return self.price * quantity
    
    @property
    def price_change(self):
        """价格变化属性"""
        if len(self._history) > 0:
            return self.price - self._history[-1]
        return 0
    
    @classmethod
    def from_dict(cls, data):
        """类方法：从字典创建实例"""
        return cls(data["symbol"], data["price"], data.get("volume", 0))
    
    @staticmethod
    def is_valid_symbol(symbol):
        """静态方法：验证股票代码"""
        return len(symbol) >= 1 and symbol.isalpha()

# 使用类
apple = Stock("AAPL", 150.0, 1000000)
apple.update_price(155.0)
print(f"价值: {apple.calculate_value(100)}")
print(f"价格变化: {apple.price_change}")

# 类方法使用
data = {"symbol": "GOOGL", "price": 2800.0}
google = Stock.from_dict(data)

# 静态方法使用
print(f"有效代码: {Stock.is_valid_symbol('AAPL')}")
```

### 4.2 继承和多态

```python
class TechStock(Stock):
    """科技股类，继承自Stock"""
    
    def __init__(self, symbol, price, volume=0, sector="Technology"):
        super().__init__(symbol, price, volume)
        self.sector = sector
    
    def calculate_pe_ratio(self, earnings):
        """计算市盈率"""
        return self.price / earnings if earnings > 0 else float('inf')

class DividendStock(Stock):
    """分红股类"""
    
    def __init__(self, symbol, price, volume=0, dividend_yield=0.02):
        super().__init__(symbol, price, volume)
        self.dividend_yield = dividend_yield
    
    def annual_dividend(self, quantity):
        """计算年度分红"""
        return self.price * quantity * self.dividend_yield

# 多态示例
def analyze_stock(stock):
    """分析股票（多态）"""
    print(f"分析 {stock.symbol}")
    if isinstance(stock, TechStock):
        print("这是科技股")
    elif isinstance(stock, DividendStock):
        print("这是分红股")

# 使用继承
apple_tech = TechStock("AAPL", 150.0, sector="Consumer Electronics")
jpm_dividend = DividendStock("JPM", 150.0, dividend_yield=0.03)

analyze_stock(apple_tech)
analyze_stock(jpm_dividend)
```

## 5. 异常处理

### 5.1 基本异常处理

```python
try:
    # 可能出错的代码
    price = float(input("请输入股票价格: "))
    quantity = int(input("请输入数量: "))
    total = price * quantity
    print(f"总价值: {total}")

except ValueError as e:
    # 值错误处理
    print(f"输入格式错误: {e}")

except ZeroDivisionError:
    # 除零错误处理
    print("数量不能为零")

except Exception as e:
    # 其他所有异常
    print(f"发生错误: {e}")

else:
    # 没有异常时执行
    print("计算成功")

finally:
    # 无论是否异常都执行
    print("计算过程结束")
```

### 5.2 自定义异常

```python
class StockError(Exception):
    """股票相关异常基类"""
    pass

class InvalidSymbolError(StockError):
    """无效股票代码异常"""
    def __init__(self, symbol):
        self.symbol = symbol
        super().__init__(f"无效的股票代码: {symbol}")

class InsufficientFundsError(StockError):
    """资金不足异常"""
    pass

def validate_stock(symbol):
    """验证股票代码"""
    if len(symbol) < 1 or not symbol.isalpha():
        raise InvalidSymbolError(symbol)
    return True

try:
    validate_stock("123")  # 这会抛出异常
except InvalidSymbolError as e:
    print(f"捕获异常: {e}")
```

## 6. 文件操作

### 6.1 基本文件读写

```python
# 写入文件
with open('stocks.txt', 'w', encoding='utf-8') as f:
    f.write("AAPL,150.0\n")
    f.write("GOOGL,2800.0\n")
    f.write("TSLA,200.0\n")

# 读取文件
with open('stocks.txt', 'r', encoding='utf-8') as f:
    for line in f:
        symbol, price = line.strip().split(',')
        print(f"{symbol}: {float(price)}")

# 追加模式
with open('stocks.txt', 'a', encoding='utf-8') as f:
    f.write("MSFT,300.0\n")
```

### 6.2 CSV文件处理

```python
import csv

# 写入CSV
stocks = [
    ["AAPL", 150.0, 1000000],
    ["GOOGL", 2800.0, 500000],
    ["TSLA", 200.0, 2000000]
]

with open('stocks.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Symbol", "Price", "Volume"])  # 表头
    writer.writerows(stocks)  # 数据行

# 读取CSV
with open('stocks.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Symbol']}: ${row['Price']} (成交量: {row['Volume']})")
```

### 6.3 JSON文件处理

```python
import json

# 写入JSON
stock_data = {
    "AAPL": {"price": 150.0, "volume": 1000000},
    "GOOGL": {"price": 2800.0, "volume": 500000},
    "TSLA": {"price": 200.0, "volume": 2000000}
}

with open('stocks.json', 'w', encoding='utf-8') as f:
    json.dump(stock_data, f, indent=2)

# 读取JSON
with open('stocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for symbol, info in data.items():
        print(f"{symbol}: {info['price']}")
```

## 7. 并发编程

### 7.1 多线程

```python
import threading
import time

def fetch_stock_price(symbol):
    """模拟获取股票价格"""
    time.sleep(1)  # 模拟网络延迟
    prices = {"AAPL": 150.0, "GOOGL": 2800.0, "TSLA": 200.0}
    return prices.get(symbol, 0.0)

def worker(symbol, results):
    """工作线程函数"""
    price = fetch_stock_price(symbol)
    results[symbol] = price
    print(f"{symbol}: ${price}")

# 创建线程
symbols = ["AAPL", "GOOGL", "TSLA"]
results = {}
threads = []

for symbol in symbols:
    thread = threading.Thread(target=worker, args=(symbol, results))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("所有股票价格获取完成")
print(f"结果: {results}")
```

### 7.2 异步编程（asyncio）

```python
import asyncio
import aiohttp

async def fetch_stock_data(symbol):
    """异步获取股票数据"""
    # 模拟异步请求
    await asyncio.sleep(1)
    data = {
        "AAPL": {"price": 150.0, "change": +2.5},
        "GOOGL": {"price": 2800.0, "change": -5.0},
        "TSLA": {"price": 200.0, "change": +10.0}
    }
    return data.get(symbol, {"price": 0.0, "change": 0.0})

async def monitor_stocks():
    """监控多只股票"""
    symbols = ["AAPL", "GOOGL", "TSLA"]
    
    # 并发执行多个异步任务
    tasks = [fetch_stock_data(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    
    for symbol, data in zip(symbols, results):
        print(f"{symbol}: ${data['price']} ({data['change']:+})")

# 运行异步程序
async def main():
    await monitor_stocks()

# Python 3.7+
asyncio.run(main())
```

## 8. 常用标准库

### 8.1 数据处理库

**datetime：**
```python
from datetime import datetime, timedelta, date

# 当前时间
now = datetime.now()
print(f"当前时间: {now}")

# 时间计算
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)

# 格式化输出
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化时间: {formatted}")

# 解析字符串
date_str = "2024-01-15"
parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
```

**collections：**
```python
from collections import defaultdict, Counter, deque

# 默认字典
stock_volumes = defaultdict(int)
stock_volumes["AAPL"] += 1000  # 自动创建键

# 计数器
symbols = ["AAPL", "GOOGL", "AAPL", "TSLA", "AAPL"]
symbol_count = Counter(symbols)
print(f"AAPL出现次数: {symbol_count['AAPL']}")

# 双端队列
price_history = deque(maxlen=5)  # 只保留最近5个价格
price_history.append(150.0)
price_history.append(155.0)
```

### 8.2 数学和统计库

**math：**
```python
import math

print(f"平方根: {math.sqrt(16)}")      # 4.0
print(f"对数: {math.log(100, 10)}")    # 2.0
print(f"圆周率: {math.pi}")           # 3.141592653589793
print(f"向上取整: {math.ceil(3.2)}")  # 4
```

**statistics：**
```python
import statistics

prices = [150.0, 155.0, 148.0, 152.0, 160.0]
print(f"平均值: {statistics.mean(prices)}")      # 153.0
print(f"中位数: {statistics.median(prices)}")    # 152.0
print(f"标准差: {statistics.stdev(prices)}")     # 4.743
```

## 9. 第三方库生态

### 9.1 数据科学库

**pandas（数据处理）：**
```python
import pandas as pd
import numpy as np

# 创建DataFrame
data = {
    'Symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT'],
    'Price': [150.0, 2800.0, 200.0, 300.0],
    'Volume': [1000000, 500000, 2000000, 800000]
}
df = pd.DataFrame(data)

# 数据操作
print(df.head())                    # 查看前几行
print(df.describe())               # 统计描述
filtered = df[df['Price'] > 100]   # 过滤数据
grouped = df.groupby('Symbol').mean()  # 分组统计
```

**numpy（数值计算）：**
```python
import numpy as np

# 创建数组
prices = np.array([150.0, 2800.0, 200.0, 300.0])
volumes = np.array([1000000, 500000, 2000000, 800000])

# 数组运算
total_values = prices * volumes           # 元素级乘法
average_price = np.mean(prices)          # 平均值
std_dev = np.std(prices)                 # 标准差

# 矩阵操作
matrix = np.array([[1, 2], [3, 4]])
inverse = np.linalg.inv(matrix)          # 矩阵求逆
```

### 9.2 Web开发库

**FastAPI（现代Web框架）：**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class StockRequest(BaseModel):
    symbol: str
    quantity: int

class StockResponse(BaseModel):
    symbol: str
    price: float
    total_value: float
    timestamp: datetime

@app.post("/order", response_model=StockResponse)
async def create_order(request: StockRequest):
    """创建股票订单"""
    # 模拟获取价格
    price = get_stock_price(request.symbol)
    total_value = price * request.quantity
    
    return StockResponse(
        symbol=request.symbol,
        price=price,
        total_value=total_value,
        timestamp=datetime.now()
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

**requests（HTTP请求）：**
```python
import requests

# GET请求
response = requests.get('https://api.example.com/stocks/AAPL')
data = response.json()

# POST请求
order_data = {"symbol": "AAPL", "quantity": 100}
response = requests.post('https://api.example.com/orders', json=order_data)

# 带认证的请求
headers = {'Authorization': 'Bearer your_token'}
response = requests.get('https://api.example.com/portfolio', headers=headers)
```

## 10. 开发工具和最佳实践

### 10.1 开发环境设置

**虚拟环境：**
```bash
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境（Linux/Mac）
source myenv/bin/activate

# 激活虚拟环境（Windows）
myenv\\Scripts\\activate

# 安装依赖
pip install -r requirements.txt

# 导出依赖
pip freeze > requirements.txt
```

**项目结构：**
```
my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── stock.py
│   └── utils/
│       ├── __init__.py
│       └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_stock.py
├── requirements.txt
├── README.md
└── .gitignore
```

### 10.2 代码质量工具

**代码格式化：**
```bash
# 安装black
pip install black

# 格式化代码
black src/

# 检查代码风格
black --check src/
```

**类型检查：**
```bash
# 安装mypy
pip install mypy

# 类型检查
mypy src/
```

**代码质量检查：**
```bash
# 安装pylint
pip install pylint

# 代码检查
pylint src/
```

### 10.3 测试框架

**单元测试：**
```python
import unittest
from src.utils.calculator import calculate_profit

class TestCalculator(unittest.TestCase):
    
    def test_calculate_profit(self):
        """测试利润计算"""
        result = calculate_profit(100, 10)
        self.assertEqual(result, 1000)
    
    def test_negative_quantity(self):
        """测试负数量"""
        with self.assertRaises(ValueError):
            calculate_profit(100, -5)

if __name__ == '__main__':
    unittest.main()
```

**pytest测试：**
```python
# test_stock.py
import pytest
from src.models.stock import Stock

def test_stock_creation():
    """测试股票创建"""
    stock = Stock("AAPL", 150.0)
    assert stock.symbol == "AAPL"
    assert stock.price == 150.0

def test_price_update():
    """测试价格更新"""
    stock = Stock("AAPL", 150.0)
    stock.update_price(155.0)
    assert stock.price == 155.0

@pytest.fixture
def sample_stock():
    """测试夹具"""
    return Stock("AAPL", 150.0)

def test_with_fixture(sample_stock):
    """使用夹具的测试"""
    assert sample_stock.symbol == "AAPL"
```

## 11. 性能优化技巧

### 11.1 基础优化

**使用生成器：**
```python
# 不好的做法：创建完整列表
def get_all_prices():
    prices = []
    for i in range(1000000):
        prices.append(i * 1.5)
    return prices

# 好的做法：使用生成器
def price_generator():
    for i in range(1000000):
        yield i * 1.5

# 使用生成器
for price in price_generator():
    if price > 1000:
        break  # 提前终止，节省内存
```

**列表推导式 vs map/filter：**
```python
# 列表推导式（推荐）
squared = [x**2 for x in range(1000) if x % 2 == 0]

# map/filter（函数式）
squared = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(1000))))

# 生成器表达式（内存友好）
squared = (x**2 for x in range(1000) if x % 2 == 0)
```

### 11.2 高级优化

**使用局部变量：**
```python
def calculate_portfolio():
    """计算投资组合"""
    # 将频繁访问的全局变量转为局部变量
    local_prices = prices  # 假设prices是全局变量
    local_quantities = quantities
    
    total = 0
    for i in range(len(local_prices)):
        total += local_prices[i] * local_quantities[i]
    return total
```

**避免不必要的对象创建：**
```python
# 不好的做法：频繁创建字符串
for i in range(1000):
    message = "价格: " + str(prices[i])  # 每次循环创建新字符串

# 好的做法：使用格式化
for i in range(1000):
    message = f"价格: {prices[i]}"  # 更高效
```

## 12. 常见陷阱和解决方案

### 12.1 可变默认参数

**问题：**
```python
def add_stock(portfolio, stocks=[]):  # 错误的默认参数
    stocks.append("AAPL")
    portfolio.extend(stocks)
    return portfolio

# 多次调用会产生意外结果
result1 = add_stock([])  # ['AAPL']
result2 = add_stock([])  # ['AAPL', 'AAPL'] - 意外！
```

**解决方案：**
```python
def add_stock(portfolio, stocks=None):
    if stocks is None:
        stocks = []  # 每次创建新列表
    stocks.append("AAPL")
    portfolio.extend(stocks)
    return portfolio
```

### 12.2 变量作用域

**问题：**
```python
total = 0

def calculate_total(prices):
    for price in prices:
        total += price  # UnboundLocalError!
    return total
```

**解决方案：**
```python
total = 0

def calculate_total(prices):
    global total  # 声明使用全局变量
    for price in prices:
        total += price
    return total

# 或者更好的做法：使用返回值
def calculate_total(prices):
    local_total = 0
    for price in prices:
        local_total += price
    return local_total
```

## 13. 学习资源推荐

### 13.1 在线教程
- **官方文档**：docs.python.org
- **Real Python**：realpython.com
- **Python官方教程**：docs.python.org/3/tutorial/
- **廖雪峰Python教程**：liaoxuefeng.com

### 13.2 书籍推荐
- **《流畅的Python》** - Luciano Ramalho
- **《Effective Python》** - Brett Slatkin
- **《Python编程：从入门到实践》** - Eric Matthes
- **《Python Cookbook》** - David Beazley

### 13.3 实践项目
1. **命令行股票查询工具**
2. **Web股票分析平台**
3. **自动化交易策略回测系统**
4. **金融市场数据可视化**

## 14. 总结

Python以其简洁的语法、丰富的生态系统和强大的社区支持，成为学习编程和实际开发的优秀选择。通过掌握基础语法、面向对象编程、异常处理、文件操作等核心概念，你可以快速构建各种应用程序。

记住编程最重要的是实践，多写代码、多调试、多阅读优秀代码，你的Python技能会不断提升！