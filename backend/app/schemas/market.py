from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any


class KLineData(BaseModel):
    """K线数据模型"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str = Field(..., description="交易对符号")
    period: str = Field(default="1m", description="K线周期")
    
    class Config:
        orm_mode = True


class OrderBookEntry(BaseModel):
    """盘口条目模型"""
    price: float
    amount: float
    total: float


class OrderBookData(BaseModel):
    """盘口数据模型"""
    symbol: str = Field(..., description="交易对符号")
    timestamp: datetime
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    
    class Config:
        orm_mode = True


class MarketTickerData(BaseModel):
    """行情数据模型"""
    symbol: str = Field(..., description="交易对符号")
    name: Optional[str] = Field(None, description="交易对名称")
    timestamp: datetime
    last_price: float = Field(..., description="最新价")
    price_change: float = Field(..., description="价格变化")
    price_change_percent: float = Field(..., description="价格变化百分比")
    high: float = Field(..., description="24小时最高价")
    low: float = Field(..., description="24小时最低价")
    volume: int = Field(..., description="24小时成交量")
    turnover: float = Field(default=0.0, description="24小时成交额")
    
    class Config:
        orm_mode = True


# 用于前端市场的简化模型
class SimpleKLineData(BaseModel):
    """简化K线数据模型"""
    time: str  # ISO格式时间字符串
    open: float
    high: float
    low: float
    close: float
    volume: float


class SimpleOrderBookEntry(BaseModel):
    """简化盘口条目模型"""
    price: float
    amount: float
    total: float


class SimpleMarketSummary(BaseModel):
    """简化市场摘要模型"""
    total_market_cap: float
    daily_volume: float
    btc_dominance: float


class SimpleSymbolData(BaseModel):
    """简化交易对数据模型"""
    symbol: str
    name: str
    price: float
    price_change: float
    price_change_percent: float
    volume_24h: float
    market_cap: float