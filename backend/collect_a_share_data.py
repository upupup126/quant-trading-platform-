#!/usr/bin/env python3
"""
A股数据采集示例脚本

这个脚本演示如何使用量化交易平台的数据采集功能获取A股数据
支持Tushare（实时数据）和BaoStock（历史批量数据）

使用前请确保：
1. 已安装依赖：pip install -r requirements.txt
2. 已配置Tushare token（如需使用Tushare功能）
3. 数据库已初始化
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.data_collector import DataCollector
from app.core.logging_config import get_app_logger, log_manager, log_exception

# 获取应用日志记录器
app_logger = get_app_logger()


def log_header(title):
    """记录标题"""
    separator = "=" * 60
    app_logger.info(separator)
    app_logger.info(f" {title}")
    app_logger.info(separator)


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


async def collect_tushare_data():
    """使用Tushare采集A股数据示例"""
    log_header("Tushare A股数据采集示例")
    
    # 检查Tushare token配置
    tushare_token = os.getenv("TUSHARE_TOKEN")
    if not tushare_token:
        app_logger.warning("⚠️ TUSHARE_TOKEN未配置，Tushare功能可能无法使用")
        app_logger.warning("   请在.env文件中设置TUSHARE_TOKEN，或从tushare.pro注册获取")
        return False
    
    db = SessionLocal()
    
    try:
        async with DataCollector(db) as collector:
            # A股主要指数列表
            a_share_indices = [
                "000001.SH",  # 上证指数
                "399001.SZ",  # 深证成指
                "000300.SH",  # 沪深300
                "000905.SH",  # 中证500
                "399006.SZ",  # 创业板指
            ]
            
            # 热门A股股票
            a_share_stocks = [
                "000858.SZ",  # 五粮液
                "000333.SZ",  # 美的集团
                "002415.SZ",  # 海康威视
                "600519.SH",  # 贵州茅台
                "601318.SH",  # 中国平安
            ]
            
            app_logger.info(f"📊 开始采集A股指数数据 ({len(a_share_indices)}个指数)...")
            
            # 采集指数数据（使用Tushare）
            index_results = await collector.collect_batch_data(
                symbols=a_share_indices,
                data_source="tushare",
                start_date="20240101",
                end_date="20241231",
                freq="D",
                period="1d"
            )
            
            app_logger.info("📈 指数数据采集结果:")
            for symbol, success in index_results.items():
                status = "✅ 成功" if success else "❌ 失败"
                app_logger.info(f"    {symbol}: {status}")
            
            app_logger.info(f"\n📊 开始采集A股股票数据 ({len(a_share_stocks)}只股票)...")
            
            # 采集股票数据（使用Tushare）
            stock_results = await collector.collect_batch_data(
                symbols=a_share_stocks,
                data_source="tushare",
                start_date="20240101",
                end_date="20241231",
                freq="D",
                period="1d"
            )
            
            app_logger.info("📈 股票数据采集结果:")
            for symbol, success in stock_results.items():
                status = "✅ 成功" if success else "❌ 失败"
                app_logger.info(f"    {symbol}: {status}")
            
            success_count = sum(index_results.values()) + sum(stock_results.values())
            total_count = len(index_results) + len(stock_results)
            
            app_logger.info(f"\n📋 汇总: {success_count}/{total_count} 个数据源采集成功")
            return success_count > 0
            
    except Exception as e:
        log_exception(e, "Tushare数据采集失败")
        return False
    finally:
        db.close()


async def collect_baostock_data():
    """使用BaoStock采集A股历史数据示例"""
    print_header("BaoStock A股历史数据批量下载示例")
    
    print("📊 BaoStock免费提供A股历史数据，适合批量下载...")
    
    db = SessionLocal()
    
    try:
        async with DataCollector(db) as collector:
            # 选择一些A股股票进行测试
            test_stocks = [
                "000001.SZ",  # 平安银行
                "000002.SZ",  # 万科A
                "600036.SH",  # 招商银行
                "600276.SH",  # 恒瑞医药
                "601888.SH",  # 中国国旅
            ]
            
            print(f"📥 开始批量下载A股历史数据 ({len(test_stocks)}只股票)...")
            
            # 使用BaoStock下载较长时间范围的历史数据
            results = await collector.collect_batch_data(
                symbols=test_stocks,
                data_source="baostock",
                start_date="2020-01-01",
                end_date="2024-12-31",
                frequency="d",  # 日线数据
                period="1d"
            )
            
            print(f"📈 BaoStock数据下载结果:")
            for symbol, success in results.items():
                status = "✅ 成功" if success else "❌ 失败"
                print(f"    {symbol}: {status}")
            
            success_count = sum(results.values())
            total_count = len(results)
            
            print(f"\n📋 汇总: {success_count}/{total_count} 个股票数据下载成功")
            
            if success_count > 0:
                print("\n💡 提示: BaoStock适合批量下载历史数据，Tushare适合获取实时和更多维度的数据")
            
            return success_count > 0
            
    except Exception as e:
        print(f"❌ BaoStock数据采集失败: {e}")
        return False
    finally:
        db.close()


async def test_individual_functions():
    """测试单个数据获取功能"""
    print_header("单个功能测试")
    
    db = SessionLocal()
    
    try:
        async with DataCollector(db) as collector:
            # 测试Tushare单个股票数据获取
            print("🧪 测试Tushare单个股票数据获取...")
            tushare_data = await collector.fetch_tushare_data(
                symbol="000001.SZ",
                start_date="20240101",
                end_date="20240110",
                freq="D"
            )
            
            if tushare_data is not None:
                print(f"✅ Tushare数据获取成功，获取到{len(tushare_data)}条数据")
                if not tushare_data.empty:
                    print(f"   最新数据: {tushare_data.index[-1].date()}, 收盘价: {tushare_data.iloc[-1]['close']:.2f}")
            else:
                print("❌ Tushare数据获取失败")
            
            print("\n🧪 测试BaoStock单个股票数据获取...")
            baostock_data = await collector.fetch_baostock_data(
                symbol="000001.SZ",
                start_date="2024-01-01",
                end_date="2024-01-10",
                frequency="d"
            )
            
            if baostock_data is not None:
                print(f"✅ BaoStock数据获取成功，获取到{len(baostock_data)}条数据")
                if not baostock_data.empty:
                    print(f"   最新数据: {baostock_data.index[-1].date()}, 收盘价: {baostock_data.iloc[-1]['close']:.2f}")
            else:
                print("❌ BaoStock数据获取失败")
                
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
    finally:
        db.close()


async def main():
    """主函数"""
    print_header("量化交易平台 - A股数据采集演示")
    
    print("📋 本演示包含以下功能：")
    print("   1. Tushare A股数据采集（实时和日线数据）")
    print("   2. BaoStock A股历史数据批量下载")
    print("   3. 单个功能测试")
    
    try:
        # 测试单个功能
        await test_individual_functions()
        
        # 用户选择要运行的功能
        print("\n🎯 请选择要运行的功能：")
        print("   1. Tushare数据采集")
        print("   2. BaoStock历史数据下载")
        print("   3. 全部运行")
        print("   4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            await collect_tushare_data()
        elif choice == "2":
            await collect_baostock_data()
        elif choice == "3":
            tushare_success = await collect_tushare_data()
            baostock_success = await collect_baostock_data()
            
            if tushare_success and baostock_success:
                print("\n🎉 所有数据采集任务完成！")
            else:
                print("\n⚠️  部分数据采集任务失败，请检查配置和网络连接")
        else:
            print("👋 退出程序")
            return
        
        print_header("演示完成")
        print("💡 提示:")
        print("   - Tushare: 适合获取实时数据、更多指标和基本面数据")
        print("   - BaoStock: 适合批量下载历史数据，完全免费")
        print("   - 两者结合可以满足大部分A股数据需求")
        
    except KeyboardInterrupt:
        print("\n\n👋 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 设置事件循环策略（Windows兼容性）
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 运行主函数
    asyncio.run(main())