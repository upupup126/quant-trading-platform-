import asyncio
import aiohttp
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import os
from app.models.market import MarketData, OrderBook, SymbolInfo, MarketTicker

logger = logging.getLogger(__name__)

class DataCollector:
    """数据采集服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    # Alpha Vantage数据源
    async def fetch_alpha_vantage_data(self, symbol: str, function: str = "TIME_SERIES_DAILY") -> Optional[Dict]:
        """从Alpha Vantage获取数据"""
        api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # 需要配置API密钥
        
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": function,
                "symbol": symbol,
                "apikey": api_key,
                "outputsize": "full"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Alpha Vantage API错误: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"获取Alpha Vantage数据失败: {e}")
            return None
    
    # Yahoo Finance数据源
    async def fetch_yahoo_data(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """从Yahoo Finance获取数据（通过yfinance库）"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if not data.empty:
                return data
            else:
                logger.warning(f"Yahoo Finance无数据: {symbol}")
                return None
                
        except ImportError:
            logger.error("请安装yfinance库: pip install yfinance")
            return None
        except Exception as e:
            logger.error(f"获取Yahoo Finance数据失败: {e}")
            return None
    
    # Binance加密货币数据
    async def fetch_binance_data(self, symbol: str, interval: str = "1d", limit: int = 1000) -> Optional[List]:
        """从Binance获取加密货币数据"""
        try:
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": limit
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # 转换数据格式
                    kline_data = []
                    for item in data:
                        kline_data.append({
                            "timestamp": datetime.fromtimestamp(item[0] / 1000),
                            "open": float(item[1]),
                            "high": float(item[2]),
                            "low": float(item[3]),
                            "close": float(item[4]),
                            "volume": float(item[5])
                        })
                    
                    return kline_data
                else:
                    logger.error(f"Binance API错误: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"获取Binance数据失败: {e}")
            return None
    
    # Tushare A股数据 - 改进版
    async def fetch_tushare_data(self, symbol: str, start_date: str, end_date: str, 
                                 freq: str = "D", adj: str = "qfq") -> Optional[pd.DataFrame]:
        """从Tushare获取A股数据（支持多种频率和复权）"""
        try:
            import tushare as ts
            
            # 从环境变量获取token
            tushare_token = os.getenv("TUSHARE_TOKEN")
            if not tushare_token:
                logger.error("Tushare token未配置，请在.env文件中设置TUSHARE_TOKEN")
                return None
            
            ts.set_token(tushare_token)
            pro = ts.pro_api()
            
            # 根据频率选择不同的接口
            if freq == "D":
                # 日线数据
                data = pro.daily(ts_code=symbol, start_date=start_date, end_date=end_date)
            elif freq == "W":
                # 周线数据
                data = pro.weekly(ts_code=symbol, start_date=start_date, end_date=end_date)
            elif freq == "M":
                # 月线数据
                data = pro.monthly(ts_code=symbol, start_date=start_date, end_date=end_date)
            elif freq in ["1", "5", "15", "30", "60"]:
                # 分钟线数据（需要权限）
                data = pro.stk_mins(ts_code=symbol, freq=freq, start_date=start_date, end_date=end_date)
            else:
                logger.error(f"不支持的频率: {freq}")
                return None
            
            if not data.empty:
                # 如果需要复权数据
                if adj != "None":
                    adj_data = pro.adj_factor(ts_code=symbol, trade_date=end_date)
                    if not adj_data.empty:
                        # 这里可以添加复权逻辑
                        pass
                
                # 重命名列以匹配通用格式
                data = data.rename(columns={
                    "trade_date": "date",
                    "ts_code": "symbol",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "vol": "volume"
                })
                
                # 转换日期格式
                if "date" in data.columns:
                    data["date"] = pd.to_datetime(data["date"])
                    data.set_index("date", inplace=True)
                
                return data
            else:
                logger.warning(f"Tushare无数据: {symbol} {start_date}~{end_date}")
                return None
                
        except ImportError:
            logger.error("请安装tushare库: pip install tushare")
            return None
        except Exception as e:
            logger.error(f"获取Tushare数据失败: {e}")
            return None
    
    # BaoStock A股历史数据批量下载
    async def fetch_baostock_data(self, symbol: str, start_date: str, end_date: str,
                                  frequency: str = "d", adjustflag: str = "3") -> Optional[pd.DataFrame]:
        """从BaoStock获取A股历史数据（批量下载）"""
        try:
            import baostock as bs
            
            # 登录BaoStock
            lg = bs.login()
            
            if lg.error_code != "0":
                logger.error(f"BaoStock登录失败: {lg.error_msg}")
                return None
            
            # 解析symbol，BaoStock需要单独的代码和交易所
            if symbol.endswith(".SH"):
                code = symbol.replace(".SH", "")
                exchange = "sh"
            elif symbol.endswith(".SZ"):
                code = symbol.replace(".SZ", "")
                exchange = "sz"
            else:
                code = symbol
                exchange = "sh"  # 默认上海交易所
            
            # BaoStock完整的股票代码格式
            bs_code = f"{exchange}.{code}"
            
            # 查询行情数据
            # adjustflag: 复权类型(1:后复权, 2:前复权, 3:不复权)
            rs = bs.query_history_k_data_plus(
                code=bs_code,
                fields="date,code,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,  # d:日k线、w:周、m:月、5:5分钟、15:15分钟等
                adjustflag=adjustflag
            )
            
            if rs.error_code != "0":
                logger.error(f"BaoStock查询失败: {rs.error_msg}")
                bs.logout()
                return None
            
            # 获取数据并转换为DataFrame
            data_list = []
            while (rs.error_code == "0") & rs.next():
                data_list.append(rs.get_row_data())
            
            bs.logout()
            
            if not data_list:
                logger.warning(f"BaoStock无数据: {symbol}")
                return None
            
            # 转换为DataFrame
            data = pd.DataFrame(data_list, columns=rs.fields)
            
            # 数据类型转换
            data["open"] = pd.to_numeric(data["open"])
            data["high"] = pd.to_numeric(data["high"])
            data["low"] = pd.to_numeric(data["low"])
            data["close"] = pd.to_numeric(data["close"])
            data["volume"] = pd.to_numeric(data["volume"])
            data["amount"] = pd.to_numeric(data["amount"])
            
            # 设置日期索引
            data["date"] = pd.to_datetime(data["date"])
            data.set_index("date", inplace=True)
            
            logger.info(f"从BaoStock成功获取{len(data)}条{symbol}数据")
            return data
            
        except ImportError:
            logger.error("请安装baostock库: pip install baostock")
            return None
        except Exception as e:
            logger.error(f"获取BaoStock数据失败: {e}")
            return None
    
    # 数据保存到数据库
    async def save_market_data(self, symbol: str, data: List[Dict], period: str = "1d") -> bool:
        """保存市场数据到数据库"""
        try:
            for item in data:
                market_data = MarketData(
                    symbol=symbol,
                    timestamp=item["timestamp"],
                    open=item["open"],
                    high=item["high"],
                    low=item["low"],
                    close=item["close"],
                    volume=item["volume"],
                    period=period
                )
                
                # 检查是否已存在
                existing = self.db.query(MarketData).filter(
                    MarketData.symbol == symbol,
                    MarketData.timestamp == item["timestamp"],
                    MarketData.period == period
                ).first()
                
                if not existing:
                    self.db.add(market_data)
            
            self.db.commit()
            logger.info(f"成功保存{symbol}的{len(data)}条数据")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"保存数据失败: {e}")
            return False
    
    # 批量数据采集 - 更新版
    async def collect_batch_data(self, symbols: List[str], data_source: str = "yahoo", 
                                 **kwargs) -> Dict[str, bool]:
        """批量采集多个交易对的数据"""
        results = {}
        
        for symbol in symbols:
            try:
                if data_source == "yahoo":
                    data = await self.fetch_yahoo_data(symbol)
                elif data_source == "binance":
                    data = await self.fetch_binance_data(symbol)
                elif data_source == "alpha_vantage":
                    data = await self.fetch_alpha_vantage_data(symbol)
                elif data_source == "tushare":
                    # 获取Tushare参数
                    start_date = kwargs.get("start_date", "20200101")
                    end_date = kwargs.get("end_date", "20231231")
                    freq = kwargs.get("freq", "D")
                    data = await self.fetch_tushare_data(symbol, start_date, end_date, freq)
                elif data_source == "baostock":
                    # 获取BaoStock参数
                    start_date = kwargs.get("start_date", "2020-01-01")
                    end_date = kwargs.get("end_date", "2023-12-31")
                    frequency = kwargs.get("frequency", "d")
                    data = await self.fetch_baostock_data(symbol, start_date, end_date, frequency)
                else:
                    logger.error(f"不支持的数据源: {data_source}")
                    results[symbol] = False
                    continue
                
                if data is not None:
                    # 转换数据格式并保存
                    kline_data = []
                    
                    if isinstance(data, pd.DataFrame):
                        # 处理DataFrame格式数据
                        for index, row in data.iterrows():
                            kline_data.append({
                                "timestamp": index.to_pydatetime() if hasattr(index, "to_pydatetime") else pd.to_datetime(index),
                                "open": float(row["open"]) if "open" in row else 0,
                                "high": float(row["high"]) if "high" in row else 0,
                                "low": float(row["low"]) if "low" in row else 0,
                                "close": float(row["close"]) if "close" in row else 0,
                                "volume": float(row["volume"]) if "volume" in row else 0
                            })
                    elif isinstance(data, list):
                        kline_data = data
                    else:
                        logger.error(f"未知的数据格式: {type(data)}")
                        results[symbol] = False
                        continue
                    
                    if kline_data:
                        period = kwargs.get("period", "1d")
                        success = await self.save_market_data(symbol, kline_data, period)
                        results[symbol] = success
                    else:
                        logger.warning(f"{symbol}数据为空")
                        results[symbol] = False
                else:
                    results[symbol] = False
                    
            except Exception as e:
                logger.error(f"采集{symbol}数据失败: {e}")
                results[symbol] = False
        
        return results
    
    # 实时数据采集（WebSocket）
    async def start_realtime_collection(self, symbols: List[str]):
        """启动实时数据采集"""
        # 这里可以实现WebSocket连接
        # 由于WebSocket实现较复杂，这里只提供框架
        logger.info(f"开始实时采集: {symbols}")
        
        # 示例：Binance WebSocket
        # async with websockets.connect("wss://stream.binance.com:9443/ws") as websocket:
        #     # 订阅行情
        #     subscribe_msg = {
        #         "method": "SUBSCRIBE",
        #         "params": [f"{symbol.lower()}@kline_1m" for symbol in symbols],
        #         "id": 1
        #     }
        #     await websocket.send(json.dumps(subscribe_msg))
        #     
        #     while True:
        #         message = await websocket.recv()
        #         data = json.loads(message)
        #         # 处理实时数据
        #         await self.process_realtime_data(data)
    
    async def process_realtime_data(self, data: Dict):
        """处理实时数据"""
        try:
            # 解析WebSocket数据
            if "k" in data:
                kline = data["k"]
                market_data = MarketData(
                    symbol=kline["s"],
                    timestamp=datetime.fromtimestamp(kline["t"] / 1000),
                    open=float(kline["o"]),
                    high=float(kline["h"]),
                    low=float(kline["l"]),
                    close=float(kline["c"]),
                    volume=float(kline["v"]),
                    period="1m"
                )
                
                self.db.add(market_data)
                self.db.commit()
                
        except Exception as e:
            logger.error(f"处理实时数据失败: {e}")

# 使用示例
async def collect_sample_data():
    """采集示例数据"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    
    async with DataCollector(db) as collector:
        # 采集股票数据
        stocks = ["AAPL", "GOOGL", "TSLA"]
        stock_results = await collector.collect_batch_data(stocks, "yahoo")
        
        # 采集加密货币数据
        cryptos = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
        crypto_results = await collector.collect_batch_data(cryptos, "binance")
        
        print("股票数据采集结果:", stock_results)
        print("加密货币数据采集结果:", crypto_results)
    
    db.close()

if __name__ == "__main__":
    # 运行数据采集
    asyncio.run(collect_sample_data())