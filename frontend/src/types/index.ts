// K线数据接口
export interface KLineData {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  symbol: string;
}

// 盘口数据接口
export interface OrderBookData {
  symbol: string;
  bids: Array<[number, number]>; // [价格, 数量]
  asks: Array<[number, number]>;
  timestamp: string;
}

// 策略接口
export interface Strategy {
  id: string;
  name: string;
  code: string;
  parameters: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

// 策略参数接口
export interface StrategyParameter {
  name: string;
  type: 'number' | 'string' | 'boolean' | 'select';
  value: any;
  min?: number;
  max?: number;
  options?: string[];
  description?: string;
}

// 回测结果接口
export interface BacktestResult {
  id: string;
  strategyId: string;
  startDate: string;
  endDate: string;
  initialCapital: number;
  finalCapital: number;
  totalReturn: number;
  annualReturn: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  totalTrades: number;
  trades: TradeRecord[];
  equityCurve: EquityPoint[];
}

// 交易记录接口
export interface TradeRecord {
  id: string;
  symbol: string;
  direction: 'buy' | 'sell';
  quantity: number;
  price: number;
  timestamp: string;
  commission: number;
  profit?: number;
}

// 资金曲线点接口
export interface EquityPoint {
  timestamp: string;
  equity: number;
}

// 账户信息接口
export interface AccountInfo {
  id: string;
  name: string;
  balance: number;
  available: number;
  frozen: number;
  totalEquity: number;
  positions: Position[];
}

// 持仓信息接口
export interface Position {
  symbol: string;
  quantity: number;
  avgCost: number;
  currentPrice: number;
  marketValue: number;
  profitLoss: number;
  profitLossRatio: number;
}

// 订单接口
export interface Order {
  id: string;
  symbol: string;
  type: 'market' | 'limit' | 'stop';
  direction: 'buy' | 'sell';
  quantity: number;
  price?: number;
  status: 'pending' | 'filled' | 'canceled' | 'rejected';
  createdAt: string;
  filledAt?: string;
  filledPrice?: number;
  filledQuantity?: number;
}

// 市场数据接口
export interface MarketData {
  symbol: string;
  name: string;
  lastPrice: number;
  change: number;
  changePercent: number;
  volume: number;
  turnover: number;
  high: number;
  low: number;
  open: number;
  preClose: number;
}

// API响应格式
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// 分页参数接口
export interface PaginationParams {
  page: number;
  pageSize: number;
  total?: number;
}

// 分页响应接口
export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationParams;
}

// 图表配置接口
export interface ChartConfig {
  type: 'kline' | 'line' | 'bar' | 'candle';
  period: string;
  indicators: string[];
  theme: 'light' | 'dark';
}

// 技术指标接口
export interface TechnicalIndicator {
  name: string;
  type: 'overlay' | 'oscillator';
  parameters: Record<string, any>;
  values: number[];
}