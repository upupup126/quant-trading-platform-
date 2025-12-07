from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.market import MarketData, OrderBook, SymbolInfo, MarketTicker
from app.schemas.market import KLineData, OrderBookData, MarketTickerData, SimpleKLineData, SimpleMarketSummary, MarketSummary, SimpleSymbolData, SimpleOrderBookEntry
from app.services.market_service import MarketService
import json
import os

# 导入日志配置
from app.core.logging_config import get_app_logger, log_exception, get_data_logger_instance

# 获取应用日志记录器
app_logger = get_app_logger()
data_logger = get_data_logger_instance()

router = APIRouter()

def check_data_sufficiency(summary_data, time_range="24h"):
    """检查数据是否充足"""
    total_symbols = summary_data.get('total_symbols', 0)
    total_volume = summary_data.get('total_volume', 0)
    latest_update_time = summary_data.get('latest_update_time')
    
    # 检查是否有有效的交易对数据
    if total_symbols == 0:
        app_logger.warning("数据库中没有有效的交易对数据，需要获取实时数据")
        return False
    
    # 检查数据是否过于陈旧（超过24小时）
    if latest_update_time:
        try:
            import datetime as dt
            update_time = dt.datetime.fromisoformat(latest_update_time.replace('Z', '+00:00'))
            now = dt.datetime.utcnow()
            
            if (now - update_time).total_seconds() > 24 * 3600:  # 超过24小时
                app_logger.warning(f"数据过于陈旧: 最新更新时间为{latest_update_time}，需要刷新数据")
                return False
        except Exception as e:
            app_logger.warning(f"解析最新更新时间失败: {str(e)}")
    
    # 检查是否有足够的交易量数据
    if total_volume == 0 and time_range == "24h":
        app_logger.warning("数据库中没有近24小时的交易量数据，需要获取实时数据")
        return False
    
    return True

@router.get("/summary", response_model=MarketSummary)
async def get_market_summary(
    market_type: Optional[str] = Query(None, description="市场类型: stock/crypto/futures（可选）"),
    time_range: str = Query("24h", description="时间范围: 24h/7d/30d"),
    db: Session = Depends(get_db)
):
    """
    获取市场摘要数据
    
    Args:
        market_type: 市场类型（可选）
        time_range: 时间范围
    
    Returns:
        市场摘要数据
    """
    try:
        app_logger.info(f"获取市场摘要数据 - 开始处理请求: market_type={market_type}, time_range={time_range}")
        
        def get_or_fetch_market_data():
            """获取市场数据，如果数据不足则触发实时获取"""
            # 第一次尝试获取摘要数据
            summary_data = MarketService.get_market_summary(
                db=db,
                market_type=market_type,
                time_range=time_range
            )
            
            # 检查数据是否充足
            if check_data_sufficiency(summary_data, time_range):
                return summary_data
            
            # 数据不足，需要获取实时数据
            app_logger.info("数据库数据不足，开始触发实时数据获取...")
            
            # 获取当前活跃的交易对列表
            symbols = []
            if market_type:
                symbols = MarketService.get_symbols(db, market_type=market_type)
            else:
                # 默认获取股票数据
                symbols = MarketService.get_symbols(db, market_type="stock")   
                
            # 如果有交易对，获取实时数据
            if symbols:
                try:
                    # 尝试获取股票数据
                    stock_symbols = [s for s in symbols if ".SH" in s or ".SZ" in s]
                    
                    if stock_symbols:
                        app_logger.info(f"获取股票实时数据: {len(stock_symbols)}个交易对")
                        
                        # 使用DataCollector类获取实际股票数据
                        from app.services.data_collector import DataCollector
                        
                        async def fetch_and_save_stock_data():
                            """异步获取并保存股票数据"""
                            try:
                                # 创建DataCollector实例
                                collector = DataCollector(db)
                                
                                # 使用Tushare作为首选数据源（如果没有配置则使用BaoStock）
                                tushare_token = os.getenv("TUSHARE_TOKEN")
                                data_source = "tushare" if tushare_token else "baostock"
                                
                                # 设置时间范围
                                end_date = datetime.utcnow().strftime("%Y%m%d")
                                start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y%m%d")
                                
                                for symbol in stock_symbols:
                                    try:
                                        app_logger.info(f"开始获取{symbol}的实时数据...")
                                        
                                        if data_source == "tushare":
                                            # 使用Tushare获取数据
                                            data = await collector.fetch_tushare_data(
                                                symbol=symbol,
                                                start_date=start_date,
                                                end_date=end_date,
                                                freq="D",
                                                adj="qfq"
                                            )
                                            
                                            if data is not None and not data.empty:
                                                # 转换数据格式并保存
                                                kline_data = []
                                                for index, row in data.iterrows():
                                                    kline_data.append({
                                                        "timestamp": index,
                                                        "open": float(row.get("open", 0)),
                                                        "high": float(row.get("high", 0)),
                                                        "low": float(row.get("low", 0)),
                                                        "close": float(row.get("close", 0)),
                                                        "volume": float(row.get("volume", 0))
                                                    })
                                                
                                                # 保存到数据库
                                                success = await collector.save_market_data(symbol, kline_data, "1d")
                                                
                                                if success:
                                                    app_logger.info(f"{symbol}数据获取并保存成功，共{len(kline_data)}条")
                                                else:
                                                    app_logger.warning(f"{symbol}数据保存失败")
                                            else:
                                                app_logger.warning(f"{symbol}未获取到Tushare数据，尝试BaoStock")
                                                
                                                # 如果Tushare失败，尝试BaoStock
                                                start_date_str = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
                                                end_date_str = datetime.utcnow().strftime("%Y-%m-%d")
                                                
                                                data = await collector.fetch_baostock_data(
                                                    symbol=symbol,
                                                    start_date=start_date_str,
                                                    end_date=end_date_str,
                                                    frequency="d",
                                                    adjustflag="3"
                                                )
                                                
                                                if data is not None and not data.empty:
                                                    kline_data = []
                                                    for index, row in data.iterrows():
                                                        kline_data.append({
                                                            "timestamp": index,
                                                            "open": float(row.get("open", 0)),
                                                            "high": float(row.get("high", 0)),
                                                            "low": float(row.get("low", 0)),
                                                            "close": float(row.get("close", 0)),
                                                            "volume": float(row.get("volume", 0))
                                                        })
                                                    
                                                    success = await collector.save_market_data(symbol, kline_data, "1d")
                                                    
                                                    if success:
                                                        app_logger.info(f"{symbol}数据通过BaoStock获取并保存成功，共{len(kline_data)}条")
                                                    else:
                                                        app_logger.warning(f"{symbol}数据保存失败")
                                                else:
                                                    app_logger.error(f"{symbol}通过BaoStock也未获取到数据")
                                                
                                        else:
                                            # 直接使用BaoStock
                                            start_date_str = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
                                            end_date_str = datetime.utcnow().strftime("%Y-%m-%d")
                                            
                                            data = await collector.fetch_baostock_data(
                                                symbol=symbol,
                                                start_date=start_date_str,
                                                end_date=end_date_str,
                                                frequency="d",
                                                adjustflag="3"
                                            )
                                            
                                            if data is not None and not data.empty:
                                                kline_data = []
                                                for index, row in data.iterrows():
                                                    kline_data.append({
                                                        "timestamp": index,
                                                        "open": float(row.get("open", 0)),
                                                        "high": float(row.get("high", 0)),
                                                        "low": float(row.get("low", 0)),
                                                        "close": float(row.get("close", 0)),
                                                        "volume": float(row.get("volume", 0))
                                                    })
                                                
                                                success = await collector.save_market_data(symbol, kline_data, "1d")
                                                
                                                if success:
                                                    app_logger.info(f"{symbol}数据获取并保存成功，共{len(kline_data)}条")
                                                else:
                                                    app_logger.warning(f"{symbol}数据保存失败")
                                            else:
                                                app_logger.error(f"{symbol}未获取到BaoStock数据")
                                        
                                    except Exception as e:
                                        app_logger.error(f"获取{symbol}数据失败: {str(e)}", exc_info=True)
                                        continue
                                
                                return True
                                
                            except Exception as e:
                                app_logger.error(f"数据获取过程失败: {str(e)}", exc_info=True)
                                return False
                        
                        # 运行异步数据获取任务
                        import asyncio
                        
                        # 检查是否已有运行的事件循环
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        
                        # 在事件循环中运行异步任务
                        if loop.is_running():
                            # 如果事件循环已在运行，创建任务
                            future = asyncio.ensure_future(fetch_and_save_stock_data())
                        else:
                            # 否则直接运行
                            result = loop.run_until_complete(fetch_and_save_stock_data())
                        
                        # 数据获取后等待短暂时间让数据库处理
                        import time
                        time.sleep(1)
                        
                    # 再次获取摘要数据
                    app_logger.info("重新获取摘要数据...")
                    summary_data = MarketService.get_market_summary(
                        db=db,
                        market_type=market_type,
                        time_range=time_range
                    )
                    
                    if check_data_sufficiency(summary_data, time_range):
                        app_logger.info("实时数据获取后数据充足")
                        return summary_data
                    else:
                        app_logger.warning("实时数据获取后数据仍不足")
                        return summary_data
                        
                except Exception as e:
                    app_logger.error(f"获取实时数据失败: {str(e)}", exc_info=True)
                    # 返回原始数据
                    return summary_data
            else:
                app_logger.warning("没有找到活跃的交易对，无法获取实时数据")
                return summary_data
        
        # 调用数据获取逻辑
        summary_data = get_or_fetch_market_data()
        
        app_logger.info(f"获取市场摘要数据 - 处理完成: total_symbols={summary_data.get('total_symbols', 0)}, total_volume={summary_data.get('total_volume', 0)}")
        
    except Exception as e:
        app_logger.error(f"获取市场摘要失败: {str(e)}", exc_info=True)
        
        # 返回错误信息摘要
        error_summary = {
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
            "start_time": datetime.utcnow().isoformat(),
            "end_time": datetime.utcnow().isoformat(),
            "timestamp": datetime.utcnow().isoformat(),
            "error": f"获取摘要数据失败: {str(e)}"
        }
        
        return MarketSummary(**error_summary)

@router.get("/kline/{symbol}", response_model=List[KLineData])
async def get_kline_data(
    symbol: str,
    period: str = Query("1m", description="K线周期: 1m,5m,15m,1h,4h,1d,1w"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    limit: int = Query(1000, description="数据条数限制", ge=1, le=10000),
    db: Session = Depends(get_db)
):
    """
    获取K线数据
    
    Args:
        symbol: 交易对符号
        period: K线周期
        start_time: 开始时间
        end_time: 结束时间
        limit: 数据条数限制
    
    Returns:
        K线数据列表
    """
    try:
        app_logger.info(f"获取K线数据 - 开始处理请求: symbol={symbol}, period={period}, limit={limit}")
        
        # 设置默认时间范围
        if not end_time:
            end_time = datetime.utcnow()
        if not start_time:
            start_time = end_time - timedelta(days=7)
        
        # 获取K线数据
        kline_data = MarketService.get_kline_data(
            db=db,
            symbol=symbol,
            period=period,
            start_time=start_time,
            end_time=end_time,
            limit=limit
        )
        
        # 如果数据库中没有数据，返回示例数据
        if not kline_data:
            app_logger.warning(f"数据库中未找到K线数据，生成示例数据: symbol={symbol}")
            kline_data = generate_sample_kline_data()
        
        app_logger.info(f"获取K线数据 - 处理成功: symbol={symbol}, 返回数据条数={len(kline_data)}")
        return kline_data
        
    except Exception as e:
        log_exception(e, f"获取K线数据失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"获取K线数据失败: {str(e)}")

def generate_sample_kline_data() -> List[KLineData]:
    """
    生成示例K线数据（当数据库中没有数据时使用）
    
    Returns:
        示例K线数据列表
    """
    sample_data = []
    base_price = 10000.0
    now = datetime.utcnow()
    
    for i in range(50):
        time = now - timedelta(hours=i)
        open_price = base_price + (i * 10) + (i % 3 * 50) - 75
        close_price = open_price + (i % 5 * 20) - 50
        high_price = max(open_price, close_price) + (i % 7 * 10)
        low_price = min(open_price, close_price) - (i % 4 * 15)
        volume = 1000000 + (i * 50000)
        
        sample_data.append(KLineData(
            timestamp=time,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=int(volume),
            symbol="BTC_USDT",
            period="1h"
        ))
    
    # 按时间排序
    return sorted(sample_data, key=lambda x: x.timestamp)

@router.get("/simple-kline/{symbol}", response_model=List[SimpleKLineData])
async def get_simple_kline_data(
    symbol: str,
    interval: str = Query("1d", description="K线间隔: 1d,1w,1M"),
    limit: int = Query(50, description="数据条数限制", ge=1, le=100)
):
    """
    获取简化版A股K线数据（用于前端显示）
    
    Args:
        symbol: 股票代码
        interval: K线间隔
        limit: 数据条数限制
    
    Returns:
        简化版K线数据列表
    """
    try:
        app_logger.info(f"获取简化版K线数据 - 开始处理请求: symbol={symbol}, interval={interval}, limit={limit}")
        
        # 生成A股示例数据
        sample_data = []
        
        # 根据不同的股票代码设置基准价格
        base_price = 3000.0  # 默认上证指数基准
        if symbol == "000001.SH":
            base_price = 3000.0  # 上证指数
        elif symbol == "000300.SH":
            base_price = 3800.0  # 沪深300
        elif symbol == "000001.SZ":
            base_price = 10000.0  # 深证成指
        elif symbol == "399001.SZ":
            base_price = 2000.0  # 创业板指
        
        now = datetime.utcnow()
        
        for i in range(limit):
            # 模拟股票价格波动
            days_offset = i * (7 if interval == "1w" else 30 if interval == "1M" else 1)
            time = now - timedelta(days=days_offset)
            
            # 生成更符合A股特征的价格
            trend_factor = 1 + (i % 20 - 10) * 0.005  # ±2.5%的长期趋势
            volatility_factor = 1 + (i % 5 - 2) * 0.015  # ±2.25%的日内波动
            
            base_trend_price = base_price * trend_factor
            
            open_price = base_trend_price * volatility_factor
            close_price = open_price * (1 + ((i % 3 - 1) * 0.01))  # ±1%涨跌
            high_price = max(open_price, close_price) * (1 + (i % 7 * 0.005))
            low_price = min(open_price, close_price) * (1 - (i % 4 * 0.006))
            
            # A股交易量以手为单位（1手=100股），但这里用实际数值模拟
            base_volume = 100000000  # 1亿股
            volume = base_volume * (1 + (i * 0.05)) * volatility_factor
            
            sample_data.append(SimpleKLineData(
                time=time.isoformat(),
                open=round(open_price, 2),
                high=round(high_price, 2),
                low=round(low_price, 2),
                close=round(close_price, 2),
                volume=float(round(volume))
            ))
        
        # 按时间正序排列
        sample_data.sort(key=lambda x: x.time)
        
        app_logger.info(f"获取简化版K线数据 - 处理成功: symbol={symbol}, 返回数据条数={len(sample_data)}")
        return sample_data
        
    except Exception as e:
        log_exception(e, f"获取简化版K线数据失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"获取K线数据失败: {str(e)}")

@router.get("/simple-orderbook/{symbol}", response_model=dict)
async def get_simple_order_book(
    symbol: str,
    depth: int = Query(10, description="盘口深度", ge=1, le=20)
):
    """
    获取简化版A股盘口数据（用于前端显示）
    
    Args:
        symbol: 股票代码
        depth: 盘口深度
    
    Returns:
        简化版盘口数据
    """
    try:
        app_logger.info(f"获取简化版盘口数据 - 开始处理请求: symbol={symbol}, depth={depth}")
        
        # 根据股票代码设置基准价格
        base_price = 3000.0  # 默认上证指数基准
        if symbol == "000001.SH":
            base_price = 3025.67  # 上证指数
        elif symbol == "000300.SH":
            base_price = 3824.15  # 沪深300
        elif symbol == "000001.SZ":
            base_price = 10124.56  # 深证成指
        elif symbol == "399001.SZ":
            base_price = 2015.34  # 创业板指
        else:
            # 个股价格
            if symbol.endswith(".SH") or symbol.endswith(".SZ"):
                base_price = 10.0 + len(symbol) % 50
        
        bids = []
        asks = []
        
        # 生成A股盘口数据（A股最小变动单位通常为0.01元）
        for i in range(depth):
            # 卖单（asks）价格高于当前价
            ask_price = round(base_price * (1 + (i + 1) * 0.001), 2)
            ask_amount = round(1000 + i * 500 + (i % 3 * 200), 0)  # 以股为单位
            
            # 买单（bids）价格低于当前价
            bid_price = round(base_price * (1 - (i + 1) * 0.001), 2)
            bid_amount = round(1200 + i * 600 + (i % 4 * 250), 0)  # 以股为单位
            
            # A股盘口通常以手为单位（1手=100股），但这里用股为单位
            bids.append({
                "price": bid_price,
                "amount": float(bid_amount),
                "total": round(bid_price * bid_amount, 2)
            })
            
            asks.append({
                "price": ask_price,
                "amount": float(ask_amount),
                "total": round(ask_price * ask_amount, 2)
            })
        
        # A股盘口通常是卖单按价格升序（低价在前），买单按价格降序（高价在前）
        bids.sort(key=lambda x: x["price"], reverse=True)  # 买单从高到低
        asks.sort(key=lambda x: x["price"])               # 卖单从低到高
        
        result = {
            "symbol": symbol,
            "timestamp": datetime.utcnow().isoformat(),
            "current_price": base_price,
            "bids": bids,
            "asks": asks
        }
        
        app_logger.info(f"获取简化版盘口数据 - 处理成功: symbol={symbol}, depth={depth}")
        return result
        
    except Exception as e:
        log_exception(e, f"获取简化版盘口数据失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"获取盘口数据失败: {str(e)}")

# ... existing code ...

@router.get("/orderbook/{symbol}", response_model=OrderBookData)
async def get_order_book(
    symbol: str,
    depth: int = Query(10, description="盘口深度", ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    获取盘口数据
    
    Args:
        symbol: 交易对符号
        depth: 盘口深度
    
    Returns:
        盘口数据
    """
    try:
        app_logger.info(f"获取盘口数据 - 开始处理请求: symbol={symbol}, depth={depth}")
        
        order_book = MarketService.get_order_book(
            db=db,
            symbol=symbol,
            depth=depth
        )
        
        if not order_book:
            app_logger.warning(f"盘口数据不存在: symbol={symbol}")
            raise HTTPException(status_code=404, detail="盘口数据不存在")
        
        app_logger.info(f"获取盘口数据 - 处理成功: symbol={symbol}")
        return order_book
        
    except HTTPException:
        raise
    except Exception as e:
        log_exception(e, f"获取盘口数据失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"获取盘口数据失败: {str(e)}")

# ... existing code ...

@router.get("/tickers", response_model=List[MarketTickerData])
async def get_market_tickers(
    market_type: Optional[str] = Query(None, description="市场类型: stock/crypto/futures"),
    sort_by: str = Query("volume", description="排序字段: volume/change_percent/turnover"),
    sort_order: str = Query("desc", description="排序顺序: asc/desc"),
    limit: int = Query(100, description="返回条数", ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    获取行情列表
    
    Args:
        market_type: 市场类型
        sort_by: 排序字段
        sort_order: 排序顺序
        limit: 返回条数
    
    Returns:
        行情数据列表
    """
    try:
        app_logger.info(f"获取行情列表 - 开始处理请求: market_type={market_type}, sort_by={sort_by}, limit={limit}")
        
        tickers = MarketService.get_market_tickers(
            db=db,
            market_type=market_type,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit
        )
        
        app_logger.info(f"获取行情列表 - 处理成功: 返回数据条数={len(tickers)}")
        return tickers
        
    except Exception as e:
        log_exception(e, f"获取行情列表失败 - market_type={market_type}")
        raise HTTPException(status_code=500, detail=f"获取行情列表失败: {str(e)}")

# ... existing code ...

@router.get("/symbols", response_model=List[str])
async def get_symbols(
    market_type: Optional[str] = Query(None, description="市场类型: stock/crypto/futures"),
    db: Session = Depends(get_db)
):
    """
    获取交易对列表
    
    Args:
        market_type: 市场类型
    
    Returns:
        交易对符号列表
    """
    try:
        app_logger.info(f"获取交易对列表 - 开始处理请求: market_type={market_type}")
        
        symbols = MarketService.get_symbols(
            db=db,
            market_type=market_type
        )
        
        app_logger.info(f"获取交易对列表 - 处理成功: 返回符号数量={len(symbols)}")
        return symbols
        
    except Exception as e:
        log_exception(e, f"获取交易对列表失败 - market_type={market_type}")
        raise HTTPException(status_code=500, detail=f"获取交易对列表失败: {str(e)}")

# ... existing code ...

@router.get("/symbols/{symbol}/info")
async def get_symbol_info(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    获取交易对详细信息
    
    Args:
        symbol: 交易对符号
    
    Returns:
        交易对详细信息
    """
    try:
        app_logger.info(f"获取交易对信息 - 开始处理请求: symbol={symbol}")
        
        symbol_info = MarketService.get_symbol_info(db=db, symbol=symbol)
        
        if not symbol_info:
            app_logger.warning(f"交易对不存在: symbol={symbol}")
            raise HTTPException(status_code=404, detail="交易对不存在")
        
        app_logger.info(f"获取交易对信息 - 处理成功: symbol={symbol}")
        return symbol_info
        
    except HTTPException:
        raise
    except Exception as e:
        log_exception(e, f"获取交易对信息失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"获取交易对信息失败: {str(e)}")

# ... existing code ...

@router.get("/search")
async def search_symbols(
    query: str = Query(..., description="搜索关键词"),
    limit: int = Query(10, description="返回条数", ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    搜索交易对
    
    Args:
        query: 搜索关键词
        limit: 返回条数
    
    Returns:
        匹配的交易对列表
    """
    try:
        app_logger.info(f"搜索交易对 - 开始处理请求: query={query}, limit={limit}")
        
        results = MarketService.search_symbols(
            db=db,
            query=query,
            limit=limit
        )
        
        app_logger.info(f"搜索交易对 - 处理成功: 返回结果数量={len(results)}")
        return results
        
    except Exception as e:
        log_exception(e, f"搜索交易对失败 - query={query}")
        raise HTTPException(status_code=500, detail=f"搜索交易对失败: {str(e)}")

# ... existing code ...

@router.post("/update/{symbol}")
async def update_market_data(
    symbol: str,
    data_source: str = Query("tushare", description="数据源: yahoo/binance/tushare/baostock"),
    period: str = Query("1d", description="数据周期: 1d/1w/1M/1h/1m"),
    db: Session = Depends(get_db)
):
    """
    手动更新指定交易对的市场数据
    
    Args:
        symbol: 交易对符号
        data_source: 数据源
        period: 数据周期
    
    Returns:
        更新结果
    """
    try:
        app_logger.info(f"手动更新市场数据 - 开始处理请求: symbol={symbol}, data_source={data_source}, period={period}")
        
        # 调用MarketService的更新方法
        result = MarketService.update_market_data(
            db=db,
            symbol=symbol,
            data_source=data_source,
            period=period
        )
        
        if result.get("success"):
            app_logger.info(f"手动更新市场数据 - 处理成功: symbol={symbol}, 更新数据条数={result.get('data_count', 0)}")
            return result
        else:
            app_logger.warning(f"手动更新市场数据 - 处理失败: symbol={symbol}, 错误信息={result.get('message')}")
            raise HTTPException(status_code=400, detail=result.get("message"))
        
    except HTTPException:
        raise
    except Exception as e:
        log_exception(e, f"手动更新市场数据失败 - symbol={symbol}")
        raise HTTPException(status_code=500, detail=f"更新市场数据失败: {str(e)}")

@router.post("/update/batch")
async def update_batch_market_data(
    symbols: List[str] = Query(..., description="交易对符号列表，多个用逗号分隔"),
    data_source: str = Query("tushare", description="数据源: yahoo/binance/tushare/baostock"),
    period: str = Query("1d", description="数据周期: 1d/1w/1M/1h/1m"),
    db: Session = Depends(get_db)
):
    """
    批量更新多个交易对的市场数据
    
    Args:
        symbols: 交易对符号列表
        data_source: 数据源
        period: 数据周期
    
    Returns:
        批量更新结果
    """
    try:
        app_logger.info(f"批量更新市场数据 - 开始处理请求: symbols={symbols}, data_source={data_source}, period={period}")
        
        # 调用MarketService的批量更新方法
        result = MarketService.update_batch_market_data(
            db=db,
            symbols=symbols,
            data_source=data_source,
            period=period
        )
        
        app_logger.info(f"批量更新市场数据 - 处理成功: 成功更新{result.get('success_count', 0)}/{result.get('total_count', 0)}个交易对")
        return result
        
    except Exception as e:
        log_exception(e, f"批量更新市场数据失败 - symbols={symbols}")
        raise HTTPException(status_code=500, detail=f"批量更新市场数据失败: {str(e)}")

@router.post("/realtime/start")
async def start_realtime_update(
    symbols: List[str] = Query(..., description="交易对符号列表，多个用逗号分隔"),
    update_interval: int = Query(60, description="更新间隔（秒）", ge=10, le=3600),
    db: Session = Depends(get_db)
):
    """
    启动实时数据更新任务
    
    Args:
        symbols: 交易对符号列表
        update_interval: 更新间隔（秒）
    
    Returns:
        实时更新任务状态
    """
    try:
        app_logger.info(f"启动实时数据更新任务 - 开始处理请求: symbols={symbols}, update_interval={update_interval}s")
        
        # 调用MarketService启动实时更新
        result = MarketService.start_realtime_update(
            db=db,
            symbols=symbols,
            update_interval=update_interval
        )
        
        if result.get("success"):
            app_logger.info(f"启动实时数据更新任务 - 处理成功: task_id={result.get('task_id')}")
            return result
        else:
            app_logger.warning(f"启动实时数据更新任务 - 处理失败: 错误信息={result.get('message')}")
            raise HTTPException(status_code=400, detail=result.get("message"))
        
    except HTTPException:
        raise
    except Exception as e:
        log_exception(e, f"启动实时数据更新任务失败 - symbols={symbols}")
        raise HTTPException(status_code=500, detail=f"启动实时更新任务失败: {str(e)}")

@router.get("/update/status")
async def get_update_status(
    task_id: Optional[str] = Query(None, description="任务ID（可选）"),
    db: Session = Depends(get_db)
):
    """
    获取数据更新任务状态
    
    Args:
        task_id: 任务ID（可选）
    
    Returns:
        更新任务状态信息
    """
    try:
        app_logger.info(f"获取数据更新任务状态 - 开始处理请求: task_id={task_id}")
        
        # 调用MarketService获取更新状态
        result = MarketService.get_update_status(db=db, task_id=task_id)
        
        app_logger.info(f"获取数据更新任务状态 - 处理成功")
        return result
        
    except Exception as e:
        log_exception(e, f"获取数据更新任务状态失败 - task_id={task_id}")
        raise HTTPException(status_code=500, detail=f"获取更新状态失败: {str(e)}")

# ... existing code ...

@router.get("/health")
async def market_health_check(db: Session = Depends(get_db)):
    """
    市场数据服务健康检查
    
    Returns:
        服务状态信息
    """
    try:
        app_logger.info("市场数据服务健康检查 - 开始处理请求")
        
        # 检查数据库连接
        db.execute("SELECT 1")
        
        # 检查数据可用性
        latest_data = db.query(MarketData).order_by(MarketData.timestamp.desc()).first()
        
        result = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "data_available": latest_data is not None,
            "last_update": latest_data.timestamp.isoformat() if latest_data else None
        }
        
        app_logger.info(f"市场数据服务健康检查 - 处理成功: data_available={result['data_available']}")
        return result
        
    except Exception as e:
        log_exception(e, "市场数据服务健康检查失败")
        raise HTTPException(status_code=503, detail=f"市场数据服务异常: {str(e)}")