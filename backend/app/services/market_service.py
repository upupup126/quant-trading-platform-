from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, case
from datetime import datetime, timedelta, timezone
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
        from datetime import datetime, timedelta, timezone
        try:
            # 计算时间范围
            end_time = datetime.now(timezone.utc)
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
            
        except Exception as e:
            return {"success": False, "message": f"获取价格变化信息失败: {str(e)}"}

    @staticmethod
    def update_market_data(
        db: Session,
        symbol: str,
        data_source: str = "yahoo",
        **kwargs
    ) -> Dict[str, Any]:
        """
        更新指定交易对的市场数据
        
        Args:
            db: 数据库会话
            symbol: 交易对符号
            data_source: 数据源（yahoo/binance/tushare/baostock）
            **kwargs: 其他参数
        
        Returns:
            更新结果
        """
        try:
            import asyncio
            from app.services.data_collector import DataCollector
            from app.models.market import MarketDataUpdateLog
            
            # 生成任务ID
            task_id = f"update_{symbol}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
            start_time = datetime.now(timezone.utc)
            
            # 创建更新日志记录
            update_log = MarketDataUpdateLog(
                task_id=task_id,
                symbol=symbol,
                data_source=data_source,
                status="running",
                message="开始更新数据...",
                start_time=start_time,
                data_count=0
            )
            db.add(update_log)
            db.commit()
            
            # 异步执行数据采集
            async def collect_data():
                async with DataCollector(db) as collector:
                    # 根据不同数据源调用相应方法
                    if data_source == "yahoo":
                        data = await collector.fetch_yahoo_data(symbol, period="1d")
                    elif data_source == "binance":
                        data = await collector.fetch_binance_data(symbol, interval="1d", limit=100)
                    elif data_source == "tushare":
                        start_date = kwargs.get("start_date", "20230101")
                        end_date = kwargs.get("end_date", "20231231")
                        freq = kwargs.get("freq", "D")
                        data = await collector.fetch_tushare_data(symbol, start_date, end_date, freq)
                    elif data_source == "baostock":
                        start_date = kwargs.get("start_date", "2023-01-01")
                        end_date = kwargs.get("end_date", "2023-12-31")
                        frequency = kwargs.get("frequency", "d")
                        data = await collector.fetch_baostock_data(symbol, start_date, end_date, frequency)
                    else:
                        return {"success": False, "message": f"不支持的数据源: {data_source}"}
                    
                    if data is not None:
                        # 转换数据格式
                        kline_data = []
                        
                        if isinstance(data, pd.DataFrame):
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
                            return {"success": False, "message": f"未知的数据格式: {type(data)}"}
                        
                        if kline_data:
                            period = kwargs.get("period", "1d")
                            success = await collector.save_market_data(symbol, kline_data, period)
                            return {
                                "success": success, 
                                "message": f"成功更新{len(kline_data)}条数据", 
                                "data_count": len(kline_data),
                                "task_id": task_id
                            }
                        else:
                            return {"success": False, "message": "数据为空", "task_id": task_id}
                    else:
                        return {"success": False, "message": "获取数据失败", "task_id": task_id}
            
            # 运行异步任务
            import pandas as pd
            result = asyncio.run(collect_data())
            
            # 更新日志记录
            end_time = datetime.now(timezone.utc)
            update_log.status = "success" if result.get("success") else "failed"
            update_log.message = result.get("message", "更新完成")
            update_log.data_count = result.get("data_count", 0)
            update_log.end_time = end_time
            db.commit()
            
            result["task_id"] = task_id
            result["start_time"] = start_time.isoformat()
            result["end_time"] = end_time.isoformat()
            result["duration"] = (end_time - start_time).total_seconds()
            
            return result
            
        except ImportError as e:
            # 更新错误日志
            update_log.status = "failed"
            update_log.message = f"依赖库未安装: {str(e)}"
            update_log.end_time = datetime.now(timezone.utc)
            db.commit()
            
            return {"success": False, "message": f"依赖库未安装: {str(e)}", "task_id": task_id}
        except Exception as e:
            # 更新错误日志
            if 'update_log' in locals():
                update_log.status = "failed"
                update_log.message = f"更新数据失败: {str(e)}"
                update_log.end_time = datetime.now(timezone.utc)
                db.commit()
            
            return {"success": False, "message": f"更新数据失败: {str(e)}", "task_id": task_id if 'task_id' in locals() else None}

    @staticmethod
    def update_batch_market_data(
        db: Session,
        symbols: List[str],
        data_source: str = "yahoo",
        **kwargs
    ) -> Dict[str, Any]:
        """
        批量更新多个交易对的市场数据
        
        Args:
            db: 数据库会话
            symbols: 交易对符号列表
            data_source: 数据源
            **kwargs: 其他参数
        
        Returns:
            批量更新结果
        """
        try:
            import asyncio
            from app.services.data_collector import DataCollector
            
            # 异步执行批量数据采集
            async def collect_batch_data():
                async with DataCollector(db) as collector:
                    results = await collector.collect_batch_data(symbols, data_source, **kwargs)
                    
                    success_count = sum(1 for success in results.values() if success)
                    total_count = len(results)
                    
                    return {
                        "success": success_count > 0,
                        "message": f"成功更新{success_count}/{total_count}个交易对",
                        "results": results,
                        "success_count": success_count,
                        "total_count": total_count
                    }
            
            result = asyncio.run(collect_batch_data())
            return result
            
        except Exception as e:
            return {"success": False, "message": f"批量更新失败: {str(e)}", "results": {}}

    @staticmethod
    def start_realtime_update(
        db: Session,
        symbols: List[str],
        update_interval: int = 60
    ) -> Dict[str, Any]:
        """
        启动实时数据更新任务
        
        Args:
            db: 数据库会话
            symbols: 交易对符号列表
            update_interval: 更新间隔（秒）
        
        Returns:
            实时更新任务状态
        """
        try:
            # 这里可以启动后台任务或定时任务
            # 实际项目中可以使用APScheduler、Celery等
            
            from app.core.logging_config import get_app_logger
            app_logger = get_app_logger()
            
            app_logger.info(f"启动实时数据更新任务: symbols={symbols}, interval={update_interval}s")
            
            # 返回任务信息
            return {
                "success": True,
                "message": "实时更新任务已启动",
                "task_id": f"realtime_update_{datetime.now(timezone.utc).timestamp()}",
                "symbols": symbols,
                "update_interval": update_interval,
                "start_time": datetime.now(timezone.utc).isoformat(),
                "status": "running"
            }
            
        except Exception as e:
            from app.core.logging_config import get_app_logger
            app_logger = get_app_logger()
            app_logger.error(f"启动实时更新任务失败: {str(e)}", exc_info=True)
            return {"success": False, "message": f"启动实时更新任务失败: {str(e)}"}

    @staticmethod
    def get_update_status(
        db: Session,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取数据更新任务状态
        
        Args:
            db: 数据库会话
            task_id: 任务ID（可选）
        
        Returns:
            任务状态信息
        """
        try:
            # 查询最近的更新记录
            from app.models.market import MarketDataUpdateLog
            
            query = db.query(MarketDataUpdateLog)
            if task_id:
                query = query.filter(MarketDataUpdateLog.task_id == task_id)
            
            latest_log = query.order_by(MarketDataUpdateLog.updated_at.desc()).first()
            
            if latest_log:
                return {
                    "success": True,
                    "task_id": latest_log.task_id,
                    "symbol": latest_log.symbol,
                    "data_source": latest_log.data_source,
                    "status": latest_log.status,
                    "message": latest_log.message,
                    "data_count": latest_log.data_count,
                    "start_time": latest_log.start_time.isoformat() if latest_log.start_time else None,
                    "end_time": latest_log.end_time.isoformat() if latest_log.end_time else None,
                    "updated_at": latest_log.updated_at.isoformat()
                }
            else:
                # 返回默认状态
                return {
                    "success": True,
                    "message": "暂无更新记录",
                    "status": "idle",
                    "last_update": None
                }
                
        except Exception as e:
            return {"success": False, "message": f"获取更新状态失败: {str(e)}"}

    @staticmethod
    def get_market_summary(
        db: Session,
        market_type: Optional[str] = None,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """
        获取市场摘要数据
        
        Args:
            db: 数据库会话
            market_type: 市场类型（可选）
            time_range: 时间范围（24h/7d/30d）
        
        Returns:
            市场摘要数据
        """
        try:
            from datetime import datetime, timedelta, timezone
            
            # 计算时间范围
            end_time = datetime.now(timezone.utc)
            if time_range == "24h":
                start_time = end_time - timedelta(hours=24)
            elif time_range == "7d":
                start_time = end_time - timedelta(days=7)
            elif time_range == "30d":
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(hours=24)
            
            # 1. 统计交易对数量
            symbol_query = db.query(SymbolInfo)
            if market_type:
                symbol_query = symbol_query.filter(SymbolInfo.market_type == market_type)
            symbol_query = symbol_query.filter(SymbolInfo.status == "active")
            total_symbols = symbol_query.count()
            
            # 2. 统计不同类型的交易对数量
            market_stats = db.query(
                SymbolInfo.market_type,
                func.count(SymbolInfo.symbol)
            ).filter(SymbolInfo.status == "active")
            
            if market_type:
                market_stats = market_stats.filter(SymbolInfo.market_type == market_type)
            
            market_stats = market_stats.group_by(SymbolInfo.market_type).all()
            
            market_type_counts = {}
            for market_type_name, count in market_stats:
                # 处理 market_type 为 None 的情况
                key = market_type_name if market_type_name else "unknown"
                market_type_counts[key] = count
            
            # 3. 统计总交易量（过去24小时）
            volume_query = db.query(func.sum(MarketTicker.volume))
            if market_type:
                volume_query = volume_query.join(SymbolInfo, MarketTicker.symbol == SymbolInfo.symbol)
                volume_query = volume_query.filter(SymbolInfo.market_type == market_type)
            
            # 筛选时间范围内的数据
            volume_query = volume_query.filter(MarketTicker.timestamp >= start_time)
            total_volume = volume_query.scalar() or 0
            
            # 4. 统计总成交额（过去24小时）
            turnover_query = db.query(func.sum(MarketTicker.turnover))
            if market_type:
                turnover_query = turnover_query.join(SymbolInfo, MarketTicker.symbol == SymbolInfo.symbol)
                turnover_query = turnover_query.filter(SymbolInfo.market_type == market_type)
            
            turnover_query = turnover_query.filter(MarketTicker.timestamp >= start_time)
            total_turnover = turnover_query.scalar() or 0
            
            # 5. 获取涨跌情况
            change_stats_query = db.query(
                func.avg(MarketTicker.price_change_percent).label("avg_change"),
                func.sum(
                    case(
                        (MarketTicker.price_change_percent > 0, 1),
                        else_=0
                    )
                ).label("up_count"),
                func.sum(
                    case(
                        (MarketTicker.price_change_percent < 0, 1),
                        else_=0
                    )
                ).label("down_count"),
                func.sum(
                    case(
                        (MarketTicker.price_change_percent == 0, 1),
                        else_=0
                    )
                ).label("flat_count")
            )
            
            if market_type:
                change_stats_query = change_stats_query.join(SymbolInfo, MarketTicker.symbol == SymbolInfo.symbol)
                change_stats_query = change_stats_query.filter(SymbolInfo.market_type == market_type)
            
            change_stats_query = change_stats_query.filter(MarketTicker.timestamp >= start_time)
            change_stats = change_stats_query.first()
            
            if change_stats:
                avg_change = change_stats.avg_change or 0
                up_count = change_stats.up_count or 0
                down_count = change_stats.down_count or 0
                flat_count = change_stats.flat_count or 0
            else:
                avg_change = 0
                up_count = 0
                down_count = 0
                flat_count = 0
            
            total_change_count = up_count + down_count + flat_count
            
            # 6. 获取最新更新的数据时间
            latest_update_query = db.query(func.max(MarketData.timestamp))
            if market_type:
                latest_update_query = latest_update_query.join(SymbolInfo, MarketData.symbol == SymbolInfo.symbol)
                latest_update_query = latest_update_query.filter(SymbolInfo.market_type == market_type)
            
            latest_update_time = latest_update_query.scalar()
            
            # 7. 获取交易量最大的交易对
            top_volume_query = db.query(
                MarketTicker.symbol,
                MarketTicker.volume,
                SymbolInfo.name
            ).join(SymbolInfo, MarketTicker.symbol == SymbolInfo.symbol)
            
            if market_type:
                top_volume_query = top_volume_query.filter(SymbolInfo.market_type == market_type)
            
            top_volume_query = top_volume_query.filter(MarketTicker.timestamp >= start_time)
            top_volume_result = top_volume_query.order_by(MarketTicker.volume.desc()).first()
            
            top_volume_symbol = {
                "symbol": top_volume_result[0] if top_volume_result else "",
                "volume": (top_volume_result[1] or 0) if top_volume_result else 0,
                "name": (top_volume_result[2] or "") if top_volume_result else ""
            }
            
            # 8. 计算市场活跃度（基于交易对数量和交易量）
            if total_symbols > 0 and total_volume > 0:
                avg_volume_per_symbol = total_volume / total_symbols
                
                # 简单的活跃度评分（0-100）
                volume_score = min(100, (total_volume / 1_000_000_000) * 10)  # 每100亿得1分，上限100
                symbol_score = min(100, total_symbols * 5)  # 每个交易对得5分，上限100
                activity_score = round((volume_score + symbol_score) / 2, 1)
            else:
                avg_volume_per_symbol = 0
                activity_score = 0
            
            # 构建返回结果
            summary = {
                "total_symbols": total_symbols or 0,
                "market_type_counts": market_type_counts or {},
                "total_volume": float(total_volume or 0),
                "total_turnover": float(total_turnover or 0),
                "avg_volume_per_symbol": float(avg_volume_per_symbol or 0),
                "price_change_stats": {
                    "avg_change": round(float(avg_change or 0), 2),
                    "up_count": up_count or 0,
                    "down_count": down_count or 0,
                    "flat_count": flat_count or 0,
                    "up_percent": round((up_count / total_change_count * 100) if total_change_count > 0 else 0, 1),
                    "down_percent": round((down_count / total_change_count * 100) if total_change_count > 0 else 0, 1)
                },
                "latest_update_time": latest_update_time.isoformat() if latest_update_time else "",
                "top_volume_symbol": top_volume_symbol or {},
                "activity_score": float(activity_score or 0),
                "market_type": market_type or "",
                "time_range": time_range or "24h",
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": None
            }
            
            return summary
            
        except Exception as e:
            from app.core.logging_config import get_app_logger
            app_logger = get_app_logger()
            app_logger.error(f"获取市场摘要失败: {str(e)}", exc_info=True)
            
            # 创建错误情况下的时间信息
            from datetime import datetime, timedelta, timezone
            end_time_error = datetime.now(timezone.utc)
            if time_range == "24h":
                start_time_error = end_time_error - timedelta(hours=24)
            elif time_range == "7d":
                start_time_error = end_time_error - timedelta(days=7)
            elif time_range == "30d":
                start_time_error = end_time_error - timedelta(days=30)
            else:
                start_time_error = end_time_error - timedelta(hours=24)
            
            # 返回基本的摘要数据（如果有错误）
            return {
                "total_symbols": 0,
                "market_type_counts": {},
                "total_volume": 0,
                "total_turnover": 0,
                "avg_volume_per_symbol": 0,
                "price_change_stats": {
                    "avg_change": 0,
                    "up_count": 0,
                    "down_count": 0,
                    "flat_count": 0,
                    "up_percent": 0,
                    "down_percent": 0
                },
                "latest_update_time": "",
                "top_volume_symbol": {"symbol": "", "volume": 0, "name": ""},
                "activity_score": 0,
                "market_type": market_type or "",
                "time_range": time_range,
                "start_time": start_time_error.isoformat(),
                "end_time": end_time_error.isoformat(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e)
            }