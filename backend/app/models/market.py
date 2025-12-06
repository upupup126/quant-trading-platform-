from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MarketData(Base):
    """市场K线数据表"""
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False, comment="交易对符号")
    timestamp = Column(DateTime, nullable=False, index=True, comment="K线时间戳")
    open = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="开盘价")
    high = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="最高价")
    low = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="最低价")
    close = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="收盘价")
    volume = Column(BigInteger, nullable=False, comment="成交量")
    turnover = Column(Float(precision=15, decimal_return_scale=4), comment="成交额")
    period = Column(String(10), nullable=False, default="1m", comment="K线周期")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<MarketData(symbol={self.symbol}, timestamp={self.timestamp}, close={self.close})>"

class OrderBook(Base):
    """盘口数据表"""
    __tablename__ = "order_book"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False, comment="交易对符号")
    timestamp = Column(DateTime, nullable=False, index=True, comment="数据时间戳")
    bids = Column(Text, nullable=False, comment="买单数据（JSON格式）")
    asks = Column(Text, nullable=False, comment="卖单数据（JSON格式）")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<OrderBook(symbol={self.symbol}, timestamp={self.timestamp})>"

class SymbolInfo(Base):
    """交易对信息表"""
    __tablename__ = "symbol_info"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), unique=True, nullable=False, comment="交易对符号")
    name = Column(String(100), nullable=False, comment="交易对名称")
    base_asset = Column(String(20), nullable=False, comment="基础资产")
    quote_asset = Column(String(20), nullable=False, comment="计价资产")
    market_type = Column(String(20), nullable=False, comment="市场类型（stock/crypto/futures）")
    status = Column(String(10), nullable=False, default="active", comment="状态")
    min_price = Column(Float(precision=15, decimal_return_scale=4), comment="最小价格")
    max_price = Column(Float(precision=15, decimal_return_scale=4), comment="最大价格")
    price_precision = Column(Integer, nullable=False, default=2, comment="价格精度")
    quantity_precision = Column(Integer, nullable=False, default=2, comment="数量精度")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def __repr__(self):
        return f"<SymbolInfo(symbol={self.symbol}, name={self.name})>"

class MarketTicker(Base):
    """实时行情数据表"""
    __tablename__ = "market_ticker"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False, comment="交易对符号")
    timestamp = Column(DateTime, nullable=False, index=True, comment="数据时间戳")
    last_price = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="最新价")
    price_change = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="价格变化")
    price_change_percent = Column(Float(precision=10, decimal_return_scale=2), nullable=False, comment="价格变化百分比")
    high = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="24小时最高价")
    low = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="24小时最低价")
    volume = Column(BigInteger, nullable=False, comment="24小时成交量")
    turnover = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="24小时成交额")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<MarketTicker(symbol={self.symbol}, last_price={self.last_price})>"