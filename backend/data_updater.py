#!/usr/bin/env python3
"""
数据定时更新脚本

功能：
1. 定时从各个数据源获取最新市场数据
2. 更新数据库中的市场数据
3. 支持手动触发和定时自动更新
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.core.database import SessionLocal
from app.services.market_service import MarketService
from app.core.logging_config import get_app_logger

# 配置日志
logger = get_app_logger()

class DataUpdater:
    """数据定时更新器"""
    
    def __init__(self):
        """初始化数据更新器"""
        self.db = SessionLocal()
        self.is_running = False
        self.tasks = {}
        
        # 默认配置
        self.config = {
            "update_interval": 300,  # 默认5分钟更新一次
            "symbols": ["BTCUSDT", "ETHUSDT", "AAPL", "GOOGL"],  # 默认更新的交易对
            "data_sources": {
                "crypto": "binance",
                "stock": "yahoo"
            }
        }
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if self.db:
            self.db.close()
    
    async def update_single_symbol(self, symbol: str, data_source: str) -> Dict[str, Any]:
        """
        更新单个交易对的数据
        
        Args:
            symbol: 交易对符号
            data_source: 数据源
        
        Returns:
            更新结果
        """
        try:
            logger.info(f"开始更新交易对: {symbol}, 数据源: {data_source}")
            
            result = MarketService.update_market_data(
                db=self.db,
                symbol=symbol,
                data_source=data_source,
                period="1d"
            )
            
            if result.get("success"):
                logger.info(f"交易对 {symbol} 更新成功: {result.get('message')}")
            else:
                logger.warning(f"交易对 {symbol} 更新失败: {result.get('message')}")
            
            return result
            
        except Exception as e:
            logger.error(f"更新交易对 {symbol} 时发生异常: {str(e)}", exc_info=True)
            return {"success": False, "message": f"更新异常: {str(e)}", "symbol": symbol}
    
    async def update_all_symbols(self):
        """更新所有配置的交易对"""
        try:
            logger.info(f"开始批量更新数据，共{len(self.config['symbols'])}个交易对")
            
            tasks = []
            for symbol in self.config["symbols"]:
                # 根据交易对类型选择数据源
                if any(crypto in symbol for crypto in ["BTC", "ETH", "USDT"]):
                    data_source = self.config["data_sources"].get("crypto", "binance")
                else:
                    data_source = self.config["data_sources"].get("stock", "yahoo")
                
                # 创建异步任务
                task = self.update_single_symbol(symbol, data_source)
                tasks.append(task)
            
            # 并发执行所有更新任务
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 统计结果
            success_count = 0
            failure_count = 0
            
            for i, result in enumerate(results):
                symbol = self.config["symbols"][i]
                if isinstance(result, Exception):
                    logger.error(f"交易对 {symbol} 更新任务异常: {str(result)}")
                    failure_count += 1
                elif result.get("success"):
                    success_count += 1
                else:
                    failure_count += 1
            
            logger.info(f"批量更新完成: 成功{success_count}个，失败{failure_count}个，总计{len(self.config['symbols'])}个交易对")
            
            return {
                "success": success_count > 0,
                "message": f"批量更新完成: 成功{success_count}个，失败{failure_count}个",
                "success_count": success_count,
                "failure_count": failure_count,
                "total_count": len(self.config['symbols'])
            }
            
        except Exception as e:
            logger.error(f"批量更新数据时发生异常: {str(e)}", exc_info=True)
            return {"success": False, "message": f"批量更新异常: {str(e)}"}
    
    def scheduled_update(self):
        """定时更新任务"""
        if not self.is_running:
            return
        
        try:
            logger.info("执行定时数据更新任务")
            
            # 异步执行批量更新
            asyncio.run(self.update_all_symbols())
            
            logger.info("定时数据更新任务完成")
            
        except Exception as e:
            logger.error(f"定时更新任务异常: {str(e)}", exc_info=True)
    
    def start_scheduled_updates(self, interval_minutes: int = 5):
        """
        启动定时更新任务
        
        Args:
            interval_minutes: 更新间隔（分钟）
        """
        if self.is_running:
            logger.warning("定时更新任务已经在运行中")
            return
        
        self.is_running = True
        self.config["update_interval"] = interval_minutes * 60  # 转换为秒
        
        # 设置定时任务
        schedule.every(interval_minutes).minutes.do(self.scheduled_update)
        
        logger.info(f"启动定时数据更新任务，每{interval_minutes}分钟执行一次")
        
        # 立即执行一次
        self.scheduled_update()
        
        # 启动调度循环
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop_scheduled_updates(self):
        """停止定时更新任务"""
        if not self.is_running:
            logger.warning("定时更新任务未在运行")
            return
        
        self.is_running = False
        logger.info("停止定时数据更新任务")
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        更新配置
        
        Args:
            new_config: 新的配置
        """
        self.config.update(new_config)
        logger.info(f"更新数据更新器配置: {new_config}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取更新器状态
        
        Returns:
            状态信息
        """
        return {
            "is_running": self.is_running,
            "config": self.config,
            "update_interval": self.config["update_interval"],
            "symbol_count": len(self.config["symbols"]),
            "status": "running" if self.is_running else "stopped",
            "last_update": datetime.utcnow().isoformat()
        }

def manual_update():
    """手动执行数据更新"""
    try:
        logger.info("开始手动数据更新")
        
        updater = DataUpdater()
        
        # 执行一次批量更新
        result = asyncio.run(updater.update_all_symbols())
        
        if result.get("success"):
            logger.info(f"手动数据更新成功: {result.get('message')}")
        else:
            logger.warning(f"手动数据更新失败: {result.get('message')}")
        
        return result
        
    except Exception as e:
        logger.error(f"手动数据更新异常: {str(e)}", exc_info=True)
        return {"success": False, "message": f"手动更新异常: {str(e)}"}

def start_scheduled_updater(interval_minutes: int = 5):
    """启动定时更新器"""
    try:
        logger.info(f"启动定时数据更新器，间隔: {interval_minutes}分钟")
        
        updater = DataUpdater()
        updater.start_scheduled_updates(interval_minutes)
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，停止定时更新器")
        updater.stop_scheduled_updates()
    except Exception as e:
        logger.error(f"启动定时更新器异常: {str(e)}", exc_info=True)

if __name__ == "__main__":
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="数据定时更新脚本")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual", 
                       help="运行模式: manual(手动更新) 或 scheduled(定时更新)")
    parser.add_argument("--interval", type=int, default=5, 
                       help="定时更新间隔（分钟），仅在scheduled模式下有效")
    
    args = parser.parse_args()
    
    if args.mode == "manual":
        # 手动更新模式
        result = manual_update()
        print(f"手动更新结果: {result}")
    elif args.mode == "scheduled":
        # 定时更新模式
        print(f"启动定时数据更新，每{args.interval}分钟执行一次")
        print("按 Ctrl+C 停止")
        start_scheduled_updater(args.interval)