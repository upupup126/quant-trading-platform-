import React, { useState } from 'react'
import { Layout, Menu, Card, Statistic, Tag, Button, Divider, Tooltip } from 'antd'
import {
  StockOutlined,
  RiseOutlined,
  FallOutlined,
  LineChartOutlined,
  HistoryOutlined,
  SettingOutlined,
  SyncOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons'
import { Link } from 'react-router-dom'
import './AppSidebar.css'

const { Sider } = Layout
const { Meta } = Card

interface MarketData {
  symbol: string
  name: string
  price: number
  change: number
  changePercent: number
  volume: number
}

const AppSidebar: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false)
  const [selectedMarket, setSelectedMarket] = useState('上证指数')
  
  // 示例市场数据
  const marketData: MarketData[] = [
    {
      symbol: '000001.SH',
      name: '上证指数',
      price: 3250.42,
      change: 15.67,
      changePercent: 0.48,
      volume: 2500000000
    },
    {
      symbol: '399001.SZ',
      name: '深证成指',
      price: 11800.32,
      change: 32.45,
      changePercent: 0.28,
      volume: 1800000000
    },
    {
      symbol: '000300.SH',
      name: '沪深300',
      price: 4100.15,
      change: 8.92,
      changePercent: 0.22,
      volume: 1200000000
    },
    {
      symbol: '000905.SH',
      name: '中证500',
      price: 6320.78,
      change: -12.34,
      changePercent: -0.19,
      volume: 850000000
    }
  ]
  
  const quickActions = [
    {
      key: 'new_strategy',
      icon: <LineChartOutlined />,
      label: '新建策略',
      path: '/strategy?action=create'
    },
    {
      key: 'backtest',
      icon: <HistoryOutlined />,
      label: '快速回测',
      path: '/strategy?action=backtest'
    },
    {
      key: 'market_overview',
      icon: <StockOutlined />,
      label: '市场总览',
      path: '/market'
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置',
      path: '/settings'
    }
  ]
  
  const formatVolume = (volume: number) => {
    if (volume >= 1000000000) {
      return (volume / 1000000000).toFixed(1) + '亿'
    } else if (volume >= 10000) {
      return (volume / 10000).toFixed(1) + '万'
    }
    return volume.toString()
  }
  
  const getChangeColor = (changePercent: number) => {
    return changePercent >= 0 ? '#ff4d4f' : '#52c41a'
  }
  
  return (
    <Sider 
      width={300}
      collapsedWidth={80}
      collapsed={collapsed}
      onCollapse={setCollapsed}
      className="app-sidebar"
      style={{ marginTop: '64px' }} // 为Header留出空间
    >
      <div className="sidebar-content">
        {/* 市场概览区域 */}
        <Card 
          size="small" 
          className="market-overview-card"
          title={(
            <div className="card-title">
              <StockOutlined />
              <span>市场概览</span>
              <Tooltip title="刷新数据">
                <Button 
                  type="text" 
                  icon={<SyncOutlined />} 
                  size="small"
                  className="refresh-button"
                />
              </Tooltip>
            </div>
          )}
        >
          <div className="market-list">
            {marketData.map((market) => (
              <div 
                key={market.symbol} 
                className={`market-item ${selectedMarket === market.name ? 'selected' : ''}`}
                onClick={() => setSelectedMarket(market.name)}
              >
                <div className="market-info">
                  <div className="market-name">{market.name}</div>
                  <div className="market-symbol">{market.symbol}</div>
                </div>
                <div className="market-price">
                  <div className="price-value">
                    ¥{market.price.toFixed(2)}
                  </div>
                  <div 
                    className="price-change"
                    style={{ color: getChangeColor(market.changePercent) }}
                  >
                    {market.change >= 0 ? <RiseOutlined /> : <FallOutlined />}
                    {Math.abs(market.changePercent).toFixed(2)}%
                    <span className="change-amount">
                      ({market.change >= 0 ? '+' : ''}{market.change.toFixed(2)})
                    </span>
                  </div>
                </div>
                <div className="market-volume">
                  成交: {formatVolume(market.volume)}
                </div>
              </div>
            ))}
          </div>
          
          <Divider style={{ margin: '12px 0' }} />
          
          {/* 快捷操作 */}
          <div className="quick-actions">
            <div className="section-title">快捷操作</div>
            <div className="action-buttons">
              {quickActions.map((action) => (
                <Tooltip key={action.key} title={action.label}>
                  <Button 
                    type="primary" 
                    icon={action.icon} 
                    className="action-button"
                    onClick={() => {
                      if (action.path) {
                        window.location.href = action.path
                      }
                    }}
                  />
                </Tooltip>
              ))}
            </div>
          </div>
        </Card>
        
        {/* 折叠按钮 */}
        <div className="collapse-handle">
          <Button 
            type="text" 
            icon={collapsed ? <RiseOutlined /> : <FallOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            className="collapse-button"
          />
        </div>
        
        {/* 帮助提示 */}
        <div className="sidebar-help">
          <Tooltip title="帮助中心">
            <QuestionCircleOutlined className="help-icon" />
          </Tooltip>
        </div>
      </div>
    </Sider>
  )
}

export default AppSidebar