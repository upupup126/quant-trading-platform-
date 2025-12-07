-- 创建market_data表的SQL命令
-- 用于解决错误: (pymysql.err.ProgrammingError) (1146, "Table 'quant_trading.market_data' doesn't exist")

-- 使用前请确保:
-- 1. 已经创建了quant_trading数据库
-- 2. 具有创建表的权限

-- 方法1: 直接执行此SQL语句
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='市场K线数据表';

-- 方法2: 使用MySQL命令行执行（如果已经登录）
-- USE quant_trading;
-- CREATE TABLE IF NOT EXISTS market_data (...);

-- 方法3: 通过文件执行
-- mysql -u username -p quant_trading < create_market_data_table.sql

-- 验证表是否创建成功
-- SHOW TABLES LIKE 'market_data';
-- DESCRIBE market_data;

-- 插入测试数据（可选）
/*
INSERT INTO market_data (symbol, timestamp, open, high, low, close, volume, period) 
VALUES 
('000001.SH', '2024-12-06 15:00:00', 3200.50, 3210.75, 3195.25, 3205.30, 150000000, '1d'),
('399001.SZ', '2024-12-06 15:00:00', 11500.20, 11550.80, 11480.40, 11525.60, 80000000, '1d');
*/

-- 注意：
-- 1. 如果使用SQLite数据库，语法会有所不同
-- 2. 根据实际数据库类型调整数据类型
-- 3. 如果已经存在表，CREATE TABLE IF NOT EXISTS会跳过创建
