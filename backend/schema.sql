-- 量化交易平台数据库表结构
-- 创建时间: 2025-12-07
-- 用途: 解决market_data表不存在的问题

-- 创建market_data表（市场K线数据）
CREATE TABLE IF NOT EXISTS market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL COMMENT '交易对符号',
    timestamp DATETIME NOT NULL COMMENT 'K线时间戳',
    open DECIMAL(15,4) NOT NULL COMMENT '开盘价',
    high DECIMAL(15,4) NOT NULL COMMENT '最高价',
    low DECIMAL(15,4) NOT NULL COMMENT '最低价',
    close DECIMAL(15,4) NOT NULL COMMENT '收盘价',
    volume BIGINT NOT NULL COMMENT '成交量',
    turnover DECIMAL(15,4) COMMENT '成交额',
    period VARCHAR(10) NOT NULL DEFAULT '1m' COMMENT 'K线周期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp),
    INDEX idx_symbol_timestamp (symbol, timestamp)
) COMMENT='市场K线数据表';

-- 创建order_book表（盘口数据）
CREATE TABLE IF NOT EXISTS order_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL COMMENT '交易对符号',
    timestamp DATETIME NOT NULL COMMENT '数据时间戳',
    bids TEXT NOT NULL COMMENT '买单数据（JSON格式）',
    asks TEXT NOT NULL COMMENT '卖单数据（JSON格式）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp)
) COMMENT='盘口数据表';

-- 创建symbol_info表（交易对信息）
CREATE TABLE IF NOT EXISTS symbol_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) UNIQUE NOT NULL COMMENT '交易对符号',
    name VARCHAR(100) NOT NULL COMMENT '交易对名称',
    base_asset VARCHAR(20) NOT NULL COMMENT '基础资产',
    quote_asset VARCHAR(20) NOT NULL COMMENT '计价资产',
    market_type VARCHAR(20) NOT NULL COMMENT '市场类型（stock/crypto/futures）',
    status VARCHAR(10) NOT NULL DEFAULT 'active' COMMENT '状态',
    min_price DECIMAL(15,4) COMMENT '最小价格',
    max_price DECIMAL(15,4) COMMENT '最大价格',
    price_precision INT NOT NULL DEFAULT 2 COMMENT '价格精度',
    quantity_precision INT NOT NULL DEFAULT 2 COMMENT '数量精度',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_symbol (symbol),
    INDEX idx_market_type (market_type)
) COMMENT='交易对信息表';

-- 创建market_ticker表（实时行情数据）
CREATE TABLE IF NOT EXISTS market_ticker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL COMMENT '交易对符号',
    timestamp DATETIME NOT NULL COMMENT '数据时间戳',
    last_price DECIMAL(15,4) NOT NULL COMMENT '最新价',
    price_change DECIMAL(15,4) NOT NULL COMMENT '价格变化',
    price_change_percent DECIMAL(10,2) NOT NULL COMMENT '价格变化百分比',
    high DECIMAL(15,4) NOT NULL COMMENT '24小时最高价',
    low DECIMAL(15,4) NOT NULL COMMENT '24小时最低价',
    volume BIGINT NOT NULL COMMENT '24小时成交量',
    turnover DECIMAL(15,4) NOT NULL COMMENT '24小时成交额',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp)
) COMMENT='实时行情数据表';

-- 使用说明
-- 1. 执行此SQL文件创建所有需要的表：mysql -u username -p quant_trading < schema.sql
-- 2. 或直接复制market_data表的创建语句执行
-- 3. 如果已有部分表存在，可以使用CREATE TABLE IF NOT EXISTS语句避免重复创建

-- 仅创建market_data表的简化版本（如果只需要解决当前错误）
/*
CREATE TABLE IF NOT EXISTS market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    open DECIMAL(15,4) NOT NULL,
    high DECIMAL(15,4) NOT NULL,
    low DECIMAL(15,4) NOT NULL,
    close DECIMAL(15,4) NOT NULL,
    volume BIGINT NOT NULL,
    turnover DECIMAL(15,4),
    period VARCHAR(10) NOT NULL DEFAULT '1m',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp)
);
*/
