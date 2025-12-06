from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Strategy(Base):
    """策略配置表"""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="策略名称")
    description = Column(Text, comment="策略描述")
    code = Column(Text, nullable=False, comment="策略代码")
    parameters = Column(JSON, nullable=False, default=dict, comment="策略参数")
    language = Column(String(20), nullable=False, default="python", comment="策略语言")
    status = Column(String(20), nullable=False, default="active", comment="策略状态")
    category = Column(String(50), comment="策略分类")
    tags = Column(JSON, default=list, comment="策略标签")
    version = Column(String(20), nullable=False, default="1.0.0", comment="策略版本")
    is_public = Column(Boolean, default=False, comment="是否公开")
    created_by = Column(String(50), nullable=False, comment="创建者")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def __repr__(self):
        return f"<Strategy(name={self.name}, version={self.version})>"

class BacktestResult(Base):
    """回测结果表"""
    __tablename__ = "backtest_results"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, nullable=False, index=True, comment="策略ID")
    name = Column(String(100), nullable=False, comment="回测名称")
    start_date = Column(DateTime, nullable=False, comment="回测开始时间")
    end_date = Column(DateTime, nullable=False, comment="回测结束时间")
    symbol = Column(String(50), nullable=False, comment="交易对符号")
    initial_capital = Column(Float(precision=15, decimal_return_scale=2), nullable=False, comment="初始资金")
    final_capital = Column(Float(precision=15, decimal_return_scale=2), nullable=False, comment="最终资金")
    total_return = Column(Float(precision=10, decimal_return_scale=4), nullable=False, comment="总收益率")
    annual_return = Column(Float(precision=10, decimal_return_scale=4), comment="年化收益率")
    sharpe_ratio = Column(Float(precision=10, decimal_return_scale=4), comment="夏普比率")
    max_drawdown = Column(Float(precision=10, decimal_return_scale=4), comment="最大回撤")
    win_rate = Column(Float(precision=10, decimal_return_scale=4), comment="胜率")
    total_trades = Column(Integer, nullable=False, comment="总交易次数")
    profit_factor = Column(Float(precision=10, decimal_return_scale=4), comment="盈亏比")
    parameters = Column(JSON, nullable=False, default=dict, comment="回测参数")
    statistics = Column(JSON, nullable=False, default=dict, comment="详细统计信息")
    equity_curve = Column(JSON, nullable=False, default=list, comment="资金曲线数据")
    trades_data = Column(JSON, nullable=False, default=list, comment="交易记录数据")
    status = Column(String(20), nullable=False, default="completed", comment="回测状态")
    error_message = Column(Text, comment="错误信息")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    completed_at = Column(DateTime, comment="完成时间")
    
    def __repr__(self):
        return f"<BacktestResult(strategy_id={self.strategy_id}, total_return={self.total_return})>"

class TradeRecord(Base):
    """交易记录表"""
    __tablename__ = "trade_records"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, nullable=False, index=True, comment="策略ID")
    backtest_id = Column(Integer, index=True, comment="回测ID")
    symbol = Column(String(50), nullable=False, comment="交易对符号")
    direction = Column(String(10), nullable=False, comment="交易方向（buy/sell）")
    order_type = Column(String(20), nullable=False, default="market", comment="订单类型")
    quantity = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="数量")
    price = Column(Float(precision=15, decimal_return_scale=4), nullable=False, comment="价格")
    commission = Column(Float(precision=15, decimal_return_scale=4), nullable=False, default=0, comment="手续费")
    timestamp = Column(DateTime, nullable=False, index=True, comment="交易时间")
    profit_loss = Column(Float(precision=15, decimal_return_scale=4), comment="盈亏金额")
    profit_loss_ratio = Column(Float(precision=10, decimal_return_scale=4), comment="盈亏比例")
    holding_period = Column(Float(precision=10, decimal_return_scale=2), comment="持仓周期（天）")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<TradeRecord(strategy_id={self.strategy_id}, symbol={self.symbol}, direction={self.direction})>"

class StrategyExecution(Base):
    """策略执行记录表"""
    __tablename__ = "strategy_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, nullable=False, index=True, comment="策略ID")
    execution_type = Column(String(20), nullable=False, comment="执行类型（backtest/simulation）")
    status = Column(String(20), nullable=False, default="running", comment="执行状态")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    progress = Column(Float(precision=5, decimal_return_scale=2), default=0, comment="执行进度")
    parameters = Column(JSON, nullable=False, default=dict, comment="执行参数")
    result_data = Column(JSON, comment="执行结果数据")
    error_message = Column(Text, comment="错误信息")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<StrategyExecution(strategy_id={self.strategy_id}, type={self.execution_type})>"