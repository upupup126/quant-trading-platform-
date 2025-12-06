import React from 'react'
import { Table, Progress } from 'antd'
import './OrderBook.css'

interface OrderBookItem {
  price: number
  quantity: number
  total: number
  side: 'buy' | 'sell'
}

interface OrderBookProps {
  data: OrderBookItem[]
}

const OrderBook: React.FC<OrderBookProps> = ({ data }) => {
  // 如果没有数据，显示默认数据
  const defaultData: OrderBookItem[] = [
    { price: 3251.2, quantity: 1500, total: 4876800, side: 'sell' },
    { price: 3250.8, quantity: 1200, total: 3900960, side: 'sell' },
    { price: 3250.5, quantity: 800, total: 2600400, side: 'sell' },
    { price: 3250.3, quantity: 500, total: 1625150, side: 'sell' },
    { price: 3250.1, quantity: 300, total: 975030, side: 'sell' },
    { price: 3250.0, quantity: 200, total: 650000, side: 'sell' },
    { price: 3249.9, quantity: 500, total: 1624950, side: 'buy' },
    { price: 3249.7, quantity: 800, total: 2599760, side: 'buy' },
    { price: 3249.5, quantity: 1200, total: 3899400, side: 'buy' },
    { price: 3249.3, quantity: 1500, total: 4873950, side: 'buy' },
    { price: 3249.0, quantity: 2000, total: 6498000, side: 'buy' },
    { price: 3248.8, quantity: 2500, total: 8122000, side: 'buy' }
  ]
  
  const displayData = data.length > 0 ? data : defaultData
  
  // 计算最大数量用于进度条
  const maxQuantity = Math.max(...displayData.map(item => item.quantity))
  
  const buyData = displayData.filter(item => item.side === 'buy').sort((a, b) => b.price - a.price)
  const sellData = displayData.filter(item => item.side === 'sell').sort((a, b) => a.price - b.price)
  
  const columns = [
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      render: (price: number, record: OrderBookItem) => (
        <span className={`price-cell ${record.side === 'buy' ? 'buy-price' : 'sell-price'}`}>
          ¥{price.toFixed(2)}
        </span>
      )
    },
    {
      title: '数量',
      dataIndex: 'quantity',
      key: 'quantity',
      render: (quantity: number) => quantity.toLocaleString()
    },
    {
      title: '总额',
      dataIndex: 'total',
      key: 'total',
      render: (total: number) => `¥${total.toLocaleString()}`
    },
    {
      title: '深度',
      key: 'depth',
      render: (_: any, record: OrderBookItem) => (
        <Progress 
          percent={(record.quantity / maxQuantity) * 100}
          showInfo={false}
          strokeColor={record.side === 'buy' ? '#52c41a' : '#ff4d4f'}
          size="small"
          className="order-depth"
        />
      )
    }
  ]
  
  return (
    <div className="order-book">
      <div className="order-book-section">
        <h4 className="section-title sell-title">卖盘</h4>
        <Table
          columns={columns}
          dataSource={sellData}
          rowKey={(record, index) => `sell-${index}`}
          pagination={false}
          size="small"
          className="sell-table"
          showHeader={false}
        />
      </div>
      
      <div className="market-price-section">
        <div className="market-price">
          <span className="price-label">最新价</span>
          <span className="price-value">¥3250.42</span>
          <span className="price-change positive">+0.48%</span>
        </div>
        <div className="market-summary">
          <span>买盘总量: {buyData.reduce((sum, item) => sum + item.quantity, 0).toLocaleString()}</span>
          <span>卖盘总量: {sellData.reduce((sum, item) => sum + item.quantity, 0).toLocaleString()}</span>
        </div>
      </div>
      
      <div className="order-book-section">
        <h4 className="section-title buy-title">买盘</h4>
        <Table
          columns={columns}
          dataSource={buyData}
          rowKey={(record, index) => `buy-${index}`}
          pagination={false}
          size="small"
          className="buy-table"
          showHeader={false}
        />
      </div>
    </div>
  )
}

export default OrderBook