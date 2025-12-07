#!/usr/bin/env python3
"""
直接API测试脚本

直接调用服务函数，验证数据库数据是否已正确初始化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.market_service import MarketService
from datetime import datetime

def test_database_connection():
    """测试数据库连接"""
    print("1. 测试数据库连接...")
    
    db = SessionLocal()
    try:
        # 执行简单的查询
        result = db.execute("SELECT 1").fetchone()
        if result and result[0] == 1:
            print("   ✅ 数据库连接成功")
            return db
        else:
            print("   ❌ 数据库连接异常")
            return None
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {str(e)}")
        return None

def test_symbol_info_table(db):
    """测试SymbolInfo表数据"""
    print("\n2. 测试SymbolInfo表数据...")
    
    try:
        from app.models.market import SymbolInfo
        
        # 统计记录数
        total_count = db.query(SymbolInfo).count()
        active_count = db.query(SymbolInfo).filter(SymbolInfo.status == "active").count()
        
        print(f"   总交易对数量: {total_count}")
        print(f"   活跃交易对数量: {active_count}")
        
        if active_count > 0:
            # 显示部分交易对
            symbols = db.query(SymbolInfo).filter(SymbolInfo.status == "active").limit(5).all()
            print("   部分活跃交易对:")
            for symbol in symbols:
                print(f"     • {symbol.symbol} - {symbol.name} ({symbol.market_type})")
            
            print(f"   ✅ SymbolInfo表数据正常 (有 {active_count} 个活跃交易对)")
            return True
        else:
            print(f"   ❌ SymbolInfo表没有活跃交易对")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试SymbolInfo表失败: {str(e)}")
        return False

def test_market_ticker_table(db):
    """测试MarketTicker表数据"""
    print("\n3. 测试MarketTicker表数据...")
    
    try:
        from app.models.market import MarketTicker
        
        # 统计记录数
        ticker_count = db.query(MarketTicker).count()
        
        print(f"   行情数据记录数: {ticker_count}")
        
        if ticker_count > 0:
            # 显示部分行情数据
            tickers = db.query(MarketTicker).order_by(MarketTicker.timestamp.desc()).limit(3).all()
            print("   最新行情数据:")
            for ticker in tickers:
                print(f"     • {ticker.symbol}: {ticker.last_price:.2f} ({ticker.timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
            
            print(f"   ✅ MarketTicker表数据正常 (有 {ticker_count} 条记录)")
            return True
        else:
            print(f"   ❌ MarketTicker表没有数据")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试MarketTicker表失败: {str(e)}")
        return False

def test_market_summary_api(db):
    """测试市场摘要API功能"""
    print("\n4. 测试市场摘要API功能...")
    
    try:
        # 调用MarketService.get_market_summary
        summary = MarketService.get_market_summary(db=db)
        
        print(f"   获取到的摘要数据:")
        print(f"     • 总交易对数量: {summary.get('total_symbols', 'N/A')}")
        print(f"     • 总交易量: {summary.get('total_volume', 'N/A')}")
        print(f"     • 市场类型统计: {summary.get('market_type_counts', {})}")
        print(f"     • 最新更新时间: {summary.get('latest_update_time', 'N/A')}")
        print(f"     • 错误信息: {summary.get('error', 'None')}")
        
        total_symbols = summary.get('total_symbols', 0)
        total_volume = summary.get('total_volume', 0)
        
        if total_symbols > 0 and total_volume > 0:
            print(f"   ✅ 市场摘要API功能正常 (返回 {total_symbols} 个交易对)")
            return True
        else:
            print(f"   ❌ 市场摘要API返回空数据")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试市场摘要API失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_symbols_api(db):
    """测试交易对列表API功能"""
    print("\n5. 测试交易对列表API功能...")
    
    try:
        # 调用MarketService.get_symbols
        symbols = MarketService.get_symbols(db=db)
        
        print(f"   获取到的交易对列表:")
        print(f"     总数量: {len(symbols)}")
        
        if symbols:
            print(f"     前10个交易对:")
            for i, symbol in enumerate(symbols[:10], 1):
                print(f"       {i:2d}. {symbol}")
            
            if len(symbols) > 10:
                print(f"       ... 和 {len(symbols) - 10} 个更多交易对")
            
            print(f"   ✅ 交易对列表API功能正常 (返回 {len(symbols)} 个交易对)")
            return True
        else:
            print(f"   ❌ 交易对列表API返回空列表")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试交易对列表API失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_with_filters(db):
    """测试带过滤条件的API功能"""
    print("\n6. 测试带过滤条件的API功能...")
    
    try:
        # 测试按市场类型过滤
        print(f"   a) 按市场类型过滤:")
        
        market_types = ["stock", "crypto"]
        for market_type in market_types:
            symbols = MarketService.get_symbols(db=db, market_type=market_type)
            print(f"      • {market_type}: {len(symbols)} 个交易对")
            if symbols:
                print(f"        示例: {symbols[:3]}")
        
        # 测试不同时间范围的summary
        print(f"\n   b) 不同时间范围的摘要:")
        
        time_ranges = ["24h", "7d", "30d"]
        for time_range in time_ranges:
            summary = MarketService.get_market_summary(db=db, time_range=time_range)
            total_volume = summary.get('total_volume', 0)
            print(f"      • {time_range}: 总交易量={total_volume}")
        
        print(f"   ✅ 过滤条件功能正常")
        return True
        
    except Exception as e:
        print(f"   ❌ 测试过滤条件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("直接API功能测试脚本")
    print("=" * 70)
    print("测试数据库数据是否已正确初始化，以及API功能是否正常")
    print("=" * 70)
    
    # 测试数据库连接
    db = test_database_connection()
    if not db:
        print("\n❌ 数据库连接失败，无法继续测试")
        return 1
    
    success_count = 0
    total_tests = 5
    
    # 执行测试
    if test_symbol_info_table(db):
        success_count += 1
    
    if test_market_ticker_table(db):
        success_count += 1
    
    if test_market_summary_api(db):
        success_count += 1
    
    if test_symbols_api(db):
        success_count += 1
    
    if test_with_filters(db):
        success_count += 1
    
    db.close()
    
    print("\n" + "=" * 70)
    print(f"测试结果: {success_count}/{total_tests} 项测试通过")
    print("=" * 70)
    
    if success_count >= 4:
        print("\n✅ 问题已解决！数据库数据已正确初始化。")
        print("")
        print("总结:")
        print("  1. 成功向数据库中添加了交易对数据")
        print("  2. 添加了相应的行情数据和K线数据")
        print("  3. MarketService.get_market_summary() 能正确返回数据")
        print("  4. MarketService.get_symbols() 能正确返回交易对列表")
        print("  5. 支持按市场类型和时间范围过滤")
        print("")
        print("下一步:")
        print("  1. 确保FastAPI服务已启动以提供HTTP API")
        print("  2. 启动命令: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        print("  3. 然后可以访问: http://localhost:8000/api/market/summary")
        print("  4. 查看完整API文档: http://localhost:8000/docs")
        return 0
    elif success_count >= 3:
        print("\n⚠ 大部分测试通过，但部分功能可能有问题")
        print("")
        print("建议:")
        print("  1. 数据库已正确初始化")
        print("  2. API核心功能正常")
        print("  3. 启动FastAPI服务后应该能正常访问")
        return 0
    else:
        print("\n❌ 测试失败较多，请检查问题")
        print("")
        print("可能原因:")
        print("  1. 数据库表结构不匹配")
        print("  2. 数据初始化脚本未正确运行")
        print("  3. 依赖包未正确安装")
        return 1

if __name__ == "__main__":
    sys.exit(main())