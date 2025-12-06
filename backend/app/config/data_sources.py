"""
数据源配置管理
集中管理所有行情数据源的配置信息
"""

from typing import Dict, List, Optional
from pydantic import BaseSettings
import os

class DataSourceConfig(BaseSettings):
    """数据源配置基类"""
    
    name: str
    enabled: bool = True
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    base_url: str
    rate_limit: int = 10  # 每分钟请求限制
    timeout: int = 30    # 请求超时时间(秒)
    
    class Config:
        env_prefix = "DATA_SOURCE_"

class AlphaVantageConfig(DataSourceConfig):
    """Alpha Vantage配置"""
    
    name: str = "alpha_vantage"
    base_url: str = "https://www.alphavantage.co"
    api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    rate_limit: int = 5  # 免费版限制较严格
    
    # 支持的数据类型
    supported_symbols: List[str] = [
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",  # 美股
        "BTCUSD", "ETHUSD", "XRPUSD",  # 加密货币
        "EURUSD", "GBPUSD", "USDJPY"   # 外汇
    ]

class YahooFinanceConfig(DataSourceConfig):
    """Yahoo Finance配置"""
    
    name: str = "yahoo_finance"
    base_url: str = "https://query1.finance.yahoo.com"
    rate_limit: int = 100
    
    # 支持的市场
    supported_markets: List[str] = ["stocks", "etf", "mutual_funds"]
    
    # 支持的交易所
    supported_exchanges: List[str] = [
        "NYSE", "NASDAQ", "AMEX",  # 美国
        "TSE", "OSE",  # 日本
        "LSE", "FWB", "XETRA"  # 欧洲
    ]

class BinanceConfig(DataSourceConfig):
    """Binance配置"""
    
    name: str = "binance"
    base_url: str = "https://api.binance.com"
    websocket_url: str = "wss://stream.binance.com:9443/ws"
    api_key: str = os.getenv("BINANCE_API_KEY", "")
    api_secret: str = os.getenv("BINANCE_SECRET_KEY", "")
    rate_limit: int = 1200
    
    # 支持的交易对
    supported_symbols: List[str] = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT",
        "LINKUSDT", "LTCUSDT", "BCHUSDT", "XRPUSDT", "EOSUSDT"
    ]
    
    # 支持的K线周期
    supported_intervals: List[str] = [
        "1m", "3m", "5m", "15m", "30m",
        "1h", "2h", "4h", "6h", "8h", "12h",
        "1d", "3d", "1w", "1M"
    ]

class TushareConfig(DataSourceConfig):
    """Tushare配置（A股数据）"""
    
    name: str = "tushare"
    base_url: str = "http://api.tushare.pro"
    api_key: str = os.getenv("TUSHARE_API_KEY", "")
    rate_limit: int = 200
    
    # 支持的市场
    supported_markets: List[str] = ["A股", "港股", "美股", "期货", "基金"]
    
    # 支持的A股交易所
    supported_exchanges: List[str] = ["SSE", "SZSE"]
    
    # 主要指数
    major_indices: List[str] = [
        "000001.SH",  # 上证指数
        "399001.SZ",  # 深证成指
        "000300.SH",  # 沪深300
        "000905.SH",  # 中证500
        "399006.SZ"   # 创业板指
    ]

class AKShareConfig(DataSourceConfig):
    """AKShare配置（中文金融数据）"""
    
    name: str = "akshare"
    base_url: str = "https://www.akshare.xyz"
    rate_limit: int = 100
    
    # 支持的数据类型
    supported_data_types: List[str] = [
        "股票", "基金", "债券", "期货", "期权",
        "外汇", "宏观经济", "行业数据", "财报数据"
    ]

class BaoStockConfig(DataSourceConfig):
    """BaoStock配置（A股历史数据批量下载）"""
    
    name: str = "baostock"
    base_url: str = "http://baostock.com"
    username: str = os.getenv("BAOSTOCK_USERNAME", "")
    password: str = os.getenv("BAOSTOCK_PASSWORD", "")
    rate_limit: int = 100  # 免费版有一定限制
    
    # 支持的数据类型
    supported_data_types: List[str] = [
        "kline", "daily", "minute", "fq", "index", 
        "dividend", "rights_issue", "suspend", "margin_trade"
    ]
    
    # 支持的A股交易所
    supported_exchanges: List[str] = ["sh", "sz"]
    
    # 支持的时间范围
    max_history_days: int = 365 * 5  # 免费版支持5年历史数据
    
    # 支持的K线周期
    supported_intervals: List[str] = [
        "5", "15", "30", "60", "d", "w", "m", "q", "y"
    ]

class WindConfig(DataSourceConfig):
    """Wind配置（付费专业数据）"""
    
    name: str = "wind"
    base_url: str = "https://www.wind.com.cn"
    api_key: str = os.getenv("WIND_API_KEY", "")
    username: str = os.getenv("WIND_USERNAME", "")
    password: str = os.getenv("WIND_PASSWORD", "")
    rate_limit: int = 1000
    
    # 支持的数据范围
    coverage: List[str] = [
        "全球股票", "债券", "期货", "期权",
        "外汇", "基金", "指数", "宏观经济"
    ]

class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources: Dict[str, DataSourceConfig] = {
            "alpha_vantage": AlphaVantageConfig(),
            "yahoo_finance": YahooFinanceConfig(),
            "binance": BinanceConfig(),
            "tushare": TushareConfig(),
            "baostock": BaoStockConfig(),
            "akshare": AKShareConfig(),
            "wind": WindConfig(),
        }
    
    def get_source(self, source_name: str) -> Optional[DataSourceConfig]:
        """获取指定数据源配置"""
        return self.sources.get(source_name)
    
    def get_enabled_sources(self) -> List[DataSourceConfig]:
        """获取所有启用的数据源"""
        return [source for source in self.sources.values() if source.enabled]
    
    def enable_source(self, source_name: str) -> bool:
        """启用数据源"""
        if source_name in self.sources:
            self.sources[source_name].enabled = True
            return True
        return False
    
    def disable_source(self, source_name: str) -> bool:
        """禁用数据源"""
        if source_name in self.sources:
            self.sources[source_name].enabled = False
            return True
        return False
    
    def get_source_by_market(self, market_type: str) -> List[DataSourceConfig]:
        """根据市场类型获取合适的数据源"""
        suitable_sources = []
        
        market_mapping = {
            "stock": ["alpha_vantage", "yahoo_finance", "tushare", "wind"],
            "crypto": ["binance", "alpha_vantage"],
            "forex": ["alpha_vantage", "yahoo_finance", "wind"],
            "futures": ["tushare", "akshare", "wind"],
            "a_share": ["tushare", "baostock", "akshare", "wind"],
            "us_stock": ["alpha_vantage", "yahoo_finance", "wind"],
        }
        
        source_names = market_mapping.get(market_type, [])
        for name in source_names:
            source = self.get_source(name)
            if source and source.enabled:
                suitable_sources.append(source)
        
        return suitable_sources
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """验证API密钥配置"""
        validation_results = {}
        
        for name, source in self.sources.items():
            if source.enabled:
                # 检查必要的API密钥
                if source.api_key and source.api_key not in ["", "demo"]:
                    validation_results[name] = True
                else:
                    validation_results[name] = False
                    print(f"警告: {name} 数据源缺少有效的API密钥")
        
        return validation_results
    
    def get_rate_limit_info(self) -> Dict[str, int]:
        """获取各数据源的速率限制信息"""
        return {name: source.rate_limit for name, source in self.sources.items() if source.enabled}

# 全局数据源管理器实例
data_source_manager = DataSourceManager()

# 数据源选择策略
class DataSourceSelector:
    """数据源选择器"""
    
    @staticmethod
    def select_best_source(symbol: str, data_type: str = "kline") -> Optional[DataSourceConfig]:
        """根据交易对选择最佳数据源"""
        
        # 根据交易对特征判断市场类型
        market_type = DataSourceSelector.detect_market_type(symbol)
        
        # 获取适合该市场类型的数据源
        suitable_sources = data_source_manager.get_source_by_market(market_type)
        
        if not suitable_sources:
            return None
        
        # 优先选择有API密钥的数据源
        for source in suitable_sources:
            if source.api_key and source.api_key not in ["", "demo"]:
                return source
        
        # 如果没有配置API密钥，使用免费数据源
        for source in suitable_sources:
            if source.name in ["yahoo_finance", "binance"]:
                return source
        
        return suitable_sources[0] if suitable_sources else None
    
    @staticmethod
    def detect_market_type(symbol: str) -> str:
        """检测交易对的市场类型"""
        symbol = symbol.upper()
        
        # 加密货币判断（通常以USDT结尾）
        if symbol.endswith("USDT") or symbol.endswith("BTC") or symbol.endswith("ETH"):
            return "crypto"
        
        # A股判断（6位数字代码）
        if len(symbol) == 6 and symbol.isdigit():
            return "a_share"
        
        # A股判断（带交易所后缀）
        if symbol.endswith(".SH") or symbol.endswith(".SZ"):
            return "a_share"
        
        # 美股判断（通常1-5个字母）
        if len(symbol) <= 5 and symbol.isalpha():
            return "us_stock"
        
        # 外汇判断（6位字母对）
        if len(symbol) == 6 and symbol.isalpha():
            return "forex"
        
        # 默认返回股票类型
        return "stock"

# 使用示例
if __name__ == "__main__":
    # 初始化数据源管理器
    manager = DataSourceManager()
    
    # 验证API密钥配置
    validation = manager.validate_api_keys()
    print("API密钥验证结果:", validation)
    
    # 选择最佳数据源
    selector = DataSourceSelector()
    
    test_symbols = ["AAPL", "BTCUSDT", "000001.SH", "EURUSD"]
    
    for symbol in test_symbols:
        best_source = selector.select_best_source(symbol)
        if best_source:
            print(f"{symbol} 的最佳数据源: {best_source.name}")
        else:
            print(f"{symbol} 没有找到合适的数据源")