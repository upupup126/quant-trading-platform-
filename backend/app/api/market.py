from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.market import MarketData, OrderBook, SymbolInfo, MarketTicker
from app.schemas.market import KLineData, OrderBookData, MarketTickerData, SimpleKLineData, SimpleMarketSummary, SimpleSymbolData, SimpleOrderBookEntry
from app.services.market_service import MarketService
import json

router = APIRouter()

@router.get("/summary", response_model=SimpleMarketSummary)
async def get_market_summary(db: Session = Depends(get_db)):
    """
    获取A股市场摘要数据
    
    Returns:
        A股市场摘要数据
    """
    try:
        # 返回A股市场数据
        return SimpleMarketSummary(
            total_market_cap=80_000_000_000_000,  # 80万亿人民币
            daily_volume=800_000_000_000,         # 8000亿人民币
            btc_dominance=0                        # A股市场不使用BTC主导率
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取市场摘要失败: {str(e)}")

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
            return generate_sample_kline_data()
        
        return kline_data
        
    except Exception as e:
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
        return sample_data
        
    except Exception as e:
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
        
        return {
            "symbol": symbol,
            "timestamp": datetime.utcnow().isoformat(),
            "current_price": base_price,
            "bids": bids,
            "asks": asks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取盘口数据失败: {str(e)}")

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
        order_book = MarketService.get_order_book(
            db=db,
            symbol=symbol,
            depth=depth
        )
        
        if not order_book:
            raise HTTPException(status_code=404, detail="盘口数据不存在")
        
        return order_book
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取盘口数据失败: {str(e)}")

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
        tickers = MarketService.get_market_tickers(
            db=db,
            market_type=market_type,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit
        )
        
        return tickers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行情列表失败: {str(e)}")

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
        symbols = MarketService.get_symbols(
            db=db,
            market_type=market_type
        )
        
        return symbols
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取交易对列表失败: {str(e)}")

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
        symbol_info = MarketService.get_symbol_info(db=db, symbol=symbol)
        
        if not symbol_info:
            raise HTTPException(status_code=404, detail="交易对不存在")
        
        return symbol_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取交易对信息失败: {str(e)}")

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
        results = MarketService.search_symbols(
            db=db,
            query=query,
            limit=limit
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索交易对失败: {str(e)}")

@router.get("/health")
async def market_health_check(db: Session = Depends(get_db)):
    """
    市场数据服务健康检查
    
    Returns:
        服务状态信息
    """
    try:
        # 检查数据库连接
        db.execute("SELECT 1")
        
        # 检查数据可用性
        latest_data = db.query(MarketData).order_by(MarketData.timestamp.desc()).first()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "data_available": latest_data is not None,
            "last_update": latest_data.timestamp.isoformat() if latest_data else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"市场数据服务异常: {str(e)}")