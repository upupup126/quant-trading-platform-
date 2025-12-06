from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from app.models.market import MarketData, OrderBook, SymbolInfo, MarketTicker
from app.schemas.market import KLineData, OrderBookData, MarketTickerData
import json

class MarketService:
    """市场数据服务类"""
    
    @staticmethod
    def get_kline_data(
        db: Session,
        symbol: str,
        period: str = "1m",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[KLineData]:
        """
        获取K线数据
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
            period: K线周期
            start_time: 开始时间
            end_time: 结束时间
            limit: 数据条数限制
        
        Returns:
            K线数据列表
        """
        query = db.query(MarketData).filter(
            MarketData.symbol == symbol,
            MarketData.period == period
        )
        
        if start_time:
            query = query.filter(MarketData.timestamp >= start_time)
        if end_time:
            query = query.filter(MarketData.timestamp <= end_time)
        
        kline_data = query.order_by(MarketData.timestamp.asc()).limit(limit).all()
        
        return [
            KLineData(
                timestamp=data.timestamp,
                open=data.open,
                high=data.high,
                low=data.low,
                close=data.close,
                volume=data.volume,
                symbol=data.symbol,
                period=data.period
            )
            for data in kline_data
        ]
    
    @staticmethod
    def get_order_book(
        db: Session,
        symbol: str,
        depth: int = 10
    ) -> Optional[OrderBookData]:
        """
        获取盘口数据
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
            depth: 盘口深度
        
        Returns:
            盘口数据
        """
        order_book = db.query(OrderBook).filter(
            OrderBook.symbol == symbol
        ).order_by(OrderBook.timestamp.desc()).first()
        
        if not order_book:
            return None
        
        # 解析盘口数据
        bids = json.loads(order_book.bids)[:depth]
        asks = json.loads(order_book.asks)[:depth]
        
        return OrderBookData(
            symbol=order_book.symbol,
            timestamp=order_book.timestamp,
            bids=bids,
            asks=asks
        )
    
    @staticmethod
    def get_market_tickers(
        db: Session,
        market_type: Optional[str] = None,
        sort_by: str = "volume",
        sort_order: str = "desc",
        limit: int = 100
    ) -> List[MarketTickerData]:
        """
        获取行情列表
        
        Args:
            db: 数据库会话
            market_type: 市场类型
            sort_by: 排序字段
            sort_order: 排序顺序
            limit: 返回条数
        
        Returns:
            行情数据列表
        """
        # 关联查询获取名称
        query = db.query(MarketTicker, SymbolInfo.name).join(
            SymbolInfo, MarketTicker.symbol == SymbolInfo.symbol
        )
        
        if market_type:
            query = query.filter(SymbolInfo.market_type == market_type)
        
        # 排序处理
        sort_column = getattr(MarketTicker, sort_by, MarketTicker.volume)
        if sort_order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        results = query.limit(limit).all()
        
        return [
            MarketTickerData(
                symbol=ticker.symbol,
                name=name,
                timestamp=ticker.timestamp,
                last_price=ticker.last_price,
                price_change=ticker.price_change,
                price_change_percent=ticker.price_change_percent,
                high=ticker.high,
                low=ticker.low,
                volume=ticker.volume,
                turnover=ticker.turnover
            )
            for ticker, name in results
        ]
    
    @staticmethod
    def get_symbols(
        db: Session,
        market_type: Optional[str] = None
    ) -> List[str]:
        """
        获取交易对列表
        
        Args:
            db: 数据库会话
            market_type: 市场类型
        
        Returns:
            交易对符号列表
        """
        query = db.query(SymbolInfo.symbol)
        
        if market_type:
            query = query.filter(SymbolInfo.market_type == market_type)
        
        query = query.filter(SymbolInfo.status == "active")
        
        symbols = query.all()
        return [symbol[0] for symbol in symbols]
    
    @staticmethod
    def get_symbol_info(
        db: Session,
        symbol: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取交易对详细信息
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
        
        Returns:
            交易对详细信息
        """
        symbol_info = db.query(SymbolInfo).filter(SymbolInfo.symbol == symbol).first()
        
        if not symbol_info:
            return None
        
        return {
            "symbol": symbol_info.symbol,
            "name": symbol_info.name,
            "base_asset": symbol_info.base_asset,
            "quote_asset": symbol_info.quote_asset,
            "market_type": symbol_info.market_type,
            "status": symbol_info.status,
            "min_price": symbol_info.min_price,
            "max_price": symbol_info.max_price,
            "price_precision": symbol_info.price_precision,
            "quantity_precision": symbol_info.quantity_precision,
            "created_at": symbol_info.created_at,
            "updated_at": symbol_info.updated_at
        }
    
    @staticmethod
    def search_symbols(
        db: Session,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索交易对
        
        Args:
            db: 数据库会话
            query: 搜索关键词
            limit: 返回条数
        
        Returns:
            匹配的交易对列表
        """
        results = db.query(SymbolInfo).filter(
            (SymbolInfo.symbol.ilike(f"%{query}%")) |
            (SymbolInfo.name.ilike(f"%{query}%")) |
            (SymbolInfo.base_asset.ilike(f"%{query}%")) |
            (SymbolInfo.quote_asset.ilike(f"%{query}%"))
        ).filter(SymbolInfo.status == "active").limit(limit).all()
        
        return [
            {
                "symbol": result.symbol,
                "name": result.name,
                "base_asset": result.base_asset,
                "quote_asset": result.quote_asset,
                "market_type": result.market_type
            }
            for result in results
        ]
    
    @staticmethod
    def get_latest_price(
        db: Session,
        symbol: str
    ) -> Optional[float]:
        """
        获取最新价格
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
        
        Returns:
            最新价格
        """
        latest_data = db.query(MarketData).filter(
            MarketData.symbol == symbol
        ).order_by(MarketData.timestamp.desc()).first()
        
        return latest_data.close if latest_data else None
    
    @staticmethod
    def get_price_change(
        db: Session,
        symbol: str,
        period: str = "24h"
    ) -> Optional[Dict[str, Any]]:
        """
        获取价格变化信息
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
            period: 时间周期
        
        Returns:
            价格变化信息
        """
        # 计算时间范围
        end_time = datetime.utcnow()
        if period == "24h":
            start_time = end_time - timedelta(hours=24)
        elif period == "7d":
            start_time = end_time - timedelta(days=7)
        elif period == "30d":
            start_time = end_time - timedelta(days=30)
        else:
            start_time = end_time - timedelta(hours=24)
        
        # 获取当前价格
        current_price = MarketService.get_latest_price(db, symbol)
        if not current_price:
            return None
        
        # 获取历史价格
        historical_data = db.query(MarketData).filter(
            MarketData.symbol == symbol,
            MarketData.timestamp >= start_time,
            MarketData.timestamp <= end_time
        ).order_by(MarketData.timestamp.asc()).first()
        
        if not historical_data:
            return None
        
        historical_price = historical_data.close
        price_change = current_price - historical_price
        price_change_percent = (price_change / historical_price) * 100
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "historical_price": historical_price,
            "price_change": price_change,
            "price_change_percent": price_change_percent,
            "period": period,
            "start_time": start_time,
            "end_time": end_time
        }