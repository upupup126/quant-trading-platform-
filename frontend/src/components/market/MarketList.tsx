import React from 'react'
import { Table, Tag, Button } from 'antd'
import { RiseOutlined, FallOutlined, StarOutlined } from '@ant-design/icons'
import './MarketList.css'

interface MarketItem {
  symbol: string
  name: string
  price: number
  change: number
  changePercent: number
  volume: number
  turnover: number
  marketCap?: number
  tags?: string[]
}

interface MarketListProps {
  data: MarketItem[]
}

const MarketList: React.FC<MarketListProps> = ({ data }) => {
  // 默认数据
  const defaultData: MarketItem[] = [
    { symbol: '000001.SH', name: '上证指数', price: 3250.42, change: 15.67, changePercent: 0.48, volume: 2500000000, turnover: 812500000000, marketCap: 40000000000000, tags: ['指数'] },
    { symbol: '399001.SZ', name: '深证成指', price: 11800.32, change: 32.45, changePercent: 0.28, volume: 1800000000, turnover: 212400000000, marketCap: 35000000000000, tags: ['指数'] },
    { symbol: '000300.SH', name: '沪深300', price: 4100.15, change: 8.92, changePercent: 0.22, volume: 1200000000, turnover: 492000000000, marketCap: 45000000000000, tags: ['指数'] },
    { symbol: '600036.SH', name: '招商银行', price: 33.8, change: 0.85, changePercent: 2.58, volume: 50000000, turnover: 1690000000, marketCap: 850000000000, tags: ['银行', '权重股'] },
    { symbol: '000858.SZ', name: '五粮液', price: 155.6, change: 4.8, changePercent: 3.18, volume: 20000000, turnover: 3112000000, marketCap: 605000000000, tags: ['白酒', '消费'] },
    { symbol: '000002.SZ', name: '万科A', price: 9.32, change: -0.08, changePercent: -0.85, volume: 80000000, turnover: 745600000, marketCap: 108000000000, tags: ['地产'] },
    { symbol: '601318.SH', name: '中国平安', price: 48.5, change: -0.32, changePercent: -0.66, volume: 60000000, turnover: 2910000000, marketCap: 886000000000, tags: ['保险', '金融'] },
    { symbol: '000063.SZ', name: '中兴通讯', price: 28.7, change: 1.2, changePercent: 4.36, volume: 45000000, turnover: 1291500000, marketCap: 136000000000, tags: ['通信', '科技'] },
    { symbol: '000725.SZ', name: '京东方A', price: 4.12, change: 0.11, changePercent: 2.74, volume: 150000000, turnover: 618000000, marketCap: 157000000000, tags: ['面板', '科技'] },
    { symbol: '002415.SZ', name: '海康威视', price: 35.8, change: -0.42, changePercent: -1.16, volume: 30000000, turnover: 1074000000, marketCap: 337000000000, tags: ['安防', '科技'] }
  ]
  
  const displayData = data.length > 0 ? data : defaultData
  
  const columns = [
    {
      title: '排名',
      key: 'rank',
      width: 60,
      render: (_: any, __: any, index: number) => {
        if (index < 3) {
          return (
            <div className={`rank-badge rank-${index + 1}`}>
              {index + 1}
            </div>
          )
        }
        return <span className="rank-text">{index + 1}</span>
      }
    },
    {
      title: '代码/名称',
      key: 'symbol',
      render: (_: any, record: MarketItem) => (
        <div className="symbol-cell">
          <div className="symbol-info">
            <div className="symbol-code">{record.symbol}</div>
            <div className="symbol-name">{record.name}</div>
          </div>
          <div className="symbol-tags">
            {record.tags?.map((tag, idx) => (
              <Tag key={idx} size="small" className="market-tag">
                {tag}
              </Tag>
            ))}
          </div>
        </div>
      )
    },
    {
      title: '最新价',
      dataIndex: 'price',
      key: 'price',
      align: 'right' as const,
      render: (price: number) => `¥${price.toFixed(2)}`
    },
    {
      title: '涨跌幅',
      key: 'change',
      align: 'right' as const,
      render: (_: any, record: MarketItem) => (
        <div className={`change-cell ${record.changePercent >= 0 ? 'positive' : 'negative'}`}>
          <div className="change-percent">
            {record.changePercent >= 0 ? <RiseOutlined /> : <FallOutlined />}
            {Math.abs(record.changePercent).toFixed(2)}%
          </div>
          <div className="change-amount">
            {record.change >= 0 ? '+' : ''}{record.change.toFixed(2)}
          </div>
        </div>
      )
    },
    {
      title: '成交量',
      dataIndex: 'volume',
      key: 'volume',
      align: 'right' as const,
      render: (volume: number) => {
        if (volume >= 1000000000) {
          return (volume / 1000000000).toFixed(1) + '亿'
        } else if (volume >= 10000) {
          return (volume / 10000).toFixed(1) + '万'
        }
        return volume.toLocaleString()
      }
    },
    {
      title: '成交额',
      dataIndex: 'turnover',
      key: 'turnover',
      align: 'right' as const,
      render: (turnover: number) => {
        if (turnover >= 100000000) {
          return (turnover / 100000000).toFixed(1) + '亿'
        }
        return turnover.toLocaleString()
      }
    },
    {
      title: '操作',
      key: 'action',
      align: 'center' as const,
      width: 80,
      render: () => (
        <Button 
          type="link" 
          size="small" 
          icon={<StarOutlined />}
          className="watchlist-button"
        />
      )
    }
  ]
  
  return (
    <div className="market-list">
      <div className="list-header">
        <h3 className="list-title">涨跌排行</h3>
        <div className="list-tabs">
          <span className="tab active">涨幅榜</span>
          <span className="tab">跌幅榜</span>
          <span className="tab">成交额榜</span>
          <span className="tab">换手率榜</span>
        </div>
      </div>
      
      <Table
        columns={columns}
        dataSource={displayData.sort((a, b) => b.changePercent - a.changePercent)}
        rowKey="symbol"
        pagination={false}
        size="small"
        className="market-table"
        rowClassName={(record) => record.changePercent >= 0 ? 'positive-row' : 'negative-row'}
      />
    </div>
  )
}

export default MarketList