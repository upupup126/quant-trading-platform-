#!/usr/bin/env python3
"""
日志配置模块
提供统一的日志配置，支持输出到控制台和文件
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 日志目录
LOG_DIR = PROJECT_ROOT / "logs"

# 确保日志目录存在
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
ERROR_LOG_FILE = LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
DATA_LOG_FILE = LOG_DIR / f"data_{datetime.now().strftime('%Y%m%d')}.log"
API_LOG_FILE = LOG_DIR / f"api_{datetime.now().strftime('%Y%m%d')}.log"

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
CONSOLE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = None, log_file: str = None, level: int = logging.INFO, 
                  max_bytes: int = 10 * 1024 * 1024, backup_count: int = 5) -> logging.Logger:
    """
    设置并返回一个配置好的日志记录器
    
    Args:
        name: 日志记录器名称，默认为模块名
        log_file: 日志文件路径，如果为None则只输出到控制台
        level: 日志级别，默认为INFO
        max_bytes: 单个日志文件最大大小（字节），默认为10MB
        backup_count: 保留的备份文件数量，默认为5个
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_formatter = logging.Formatter(CONSOLE_FORMAT, DATE_FORMAT)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        log_path = Path(log_file)
        # 确保日志文件目录存在
        if not log_path.parent.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用RotatingFileHandler进行日志轮转
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_default_logger() -> logging.Logger:
    """获取默认的应用日志记录器"""
    return setup_logger(
        name="quant_trading_app",
        log_file=str(LOG_FILE),
        level=logging.INFO
    )


def get_error_logger() -> logging.Logger:
    """获取错误日志记录器"""
    return setup_logger(
        name="quant_trading_error",
        log_file=str(ERROR_LOG_FILE),
        level=logging.ERROR
    )


def get_data_logger() -> logging.Logger:
    """获取数据采集日志记录器"""
    return setup_logger(
        name="quant_trading_data",
        log_file=str(DATA_LOG_FILE),
        level=logging.INFO
    )


def get_api_logger() -> logging.Logger:
    """获取API日志记录器"""
    return setup_logger(
        name="quant_trading_api",
        log_file=str(API_LOG_FILE),
        level=logging.INFO
    )


def setup_timed_rotating_logger(name: str, log_file: str, when: str = "midnight", 
                                 interval: int = 1, backup_count: int = 7, 
                                 level: int = logging.INFO) -> logging.Logger:
    """
    设置基于时间轮转的日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        when: 轮转时间单位，可选：'S'（秒）、'M'（分）、'H'（小时）、'D'（天）、'midnight'（午夜）
        interval: 轮转间隔
        backup_count: 保留的备份文件数量
        level: 日志级别
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_formatter = logging.Formatter(CONSOLE_FORMAT, DATE_FORMAT)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 时间轮转文件处理器
    log_path = Path(log_file)
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = TimedRotatingFileHandler(
        log_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d"  # 按日期后缀命名
    logger.addHandler(file_handler)
    
    return logger


class LogManager:
    """日志管理器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.loggers = {}
        self.initialized = False
    
    def initialize(self):
        """初始化日志管理器"""
        if self.initialized:
            return
        
        # 创建默认的日志记录器
        self.loggers["app"] = get_default_logger()
        self.loggers["error"] = get_error_logger()
        self.loggers["data"] = get_data_logger()
        self.loggers["api"] = get_api_logger()
        
        self.initialized = True
        
        # 记录初始化日志
        app_logger = self.get_logger("app")
        app_logger.info("=" * 60)
        app_logger.info("量化交易平台 - 日志系统初始化完成")
        app_logger.info(f"日志目录: {LOG_DIR}")
        app_logger.info("=" * 60)
    
    def get_logger(self, logger_type: str = "app") -> logging.Logger:
        """获取指定类型的日志记录器"""
        if not self.initialized:
            self.initialize()
        
        return self.loggers.get(logger_type, self.loggers["app"])
    
    def log_data_collection(self, symbol: str, data_source: str, status: str, 
                           message: str = "", error: Exception = None):
        """记录数据采集日志"""
        data_logger = self.get_logger("data")
        
        if status == "success":
            data_logger.info(f"数据采集成功 - {symbol} - 数据源: {data_source} - {message}")
        elif status == "warning":
            data_logger.warning(f"数据采集警告 - {symbol} - 数据源: {data_source} - {message}")
        elif status == "error":
            error_msg = message
            if error:
                error_msg += f" - 错误: {str(error)}"
            data_logger.error(f"数据采集错误 - {symbol} - 数据源: {data_source} - {error_msg}")
            
            # 同时记录到错误日志
            error_logger = self.get_logger("error")
            error_logger.error(f"数据采集错误 - {symbol} - 数据源: {data_source} - {error_msg}")
    
    def log_api_request(self, method: str, endpoint: str, status_code: int = None,
                       duration: float = None, client_ip: str = None):
        """记录API请求日志"""
        api_logger = self.get_logger("api")
        
        log_parts = [f"{method} {endpoint}"]
        if status_code:
            log_parts.append(f"状态码: {status_code}")
        if duration is not None:
            log_parts.append(f"耗时: {duration:.3f}s")
        if client_ip:
            log_parts.append(f"客户端IP: {client_ip}")
        
        api_logger.info(" - ".join(log_parts))


# 全局日志管理器实例
log_manager = LogManager()

# 常用的便捷函数
def get_app_logger():
    """获取应用日志记录器"""
    return log_manager.get_logger("app")

def get_data_logger_instance():
    """获取数据采集日志记录器"""
    return log_manager.get_logger("data")

def get_api_logger_instance():
    """获取API日志记录器"""
    return log_manager.get_logger("api")


def log_exception(exc: Exception, context: str = ""):
    """记录异常信息"""
    error_logger = log_manager.get_logger("error")
    
    if context:
        error_msg = f"{context}: {type(exc).__name__}: {str(exc)}"
    else:
        error_msg = f"{type(exc).__name__}: {str(exc)}"
    
    error_logger.error(error_msg, exc_info=True)
    
    # 同时记录到应用日志（警告级别）
    app_logger = log_manager.get_logger("app")
    app_logger.warning(f"发生异常: {error_msg}")


# 初始化日志管理器（在导入时自动初始化）
log_manager.initialize()

if __name__ == "__main__":
    """测试日志配置"""
    print("测试日志配置...")
    
    app_logger = get_app_logger()
    data_logger = get_data_logger_instance()
    api_logger = get_api_logger_instance()
    
    # 测试不同级别的日志
    app_logger.debug("调试信息")
    app_logger.info("应用启动信息")
    app_logger.warning("警告信息")
    app_logger.error("错误信息")
    
    # 测试数据采集日志
    log_manager.log_data_collection("000001.SZ", "tushare", "success", "获取100条日线数据")
    log_manager.log_data_collection("AAPL", "yahoo", "warning", "获取数据延迟较高")
    log_manager.log_data_collection("BTCUSDT", "binance", "error", "API请求失败", 
                                   Exception("网络连接超时"))
    
    # 测试API日志
    log_manager.log_api_request("GET", "/api/market/symbols", 200, 0.125, "127.0.0.1")
    
    print(f"\n日志文件位置：")
    print(f"  - 应用日志: {LOG_FILE}")
    print(f"  - 错误日志: {ERROR_LOG_FILE}")
    print(f"  - 数据日志: {DATA_LOG_FILE}")
    print(f"  - API日志: {API_LOG_FILE}")
    print("\n✅ 日志配置测试完成，请检查上述日志文件")
