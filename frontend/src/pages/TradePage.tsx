import React from 'react'
import { Row, Col, Card } from 'antd'
import { ShoppingCartOutlined } from '@ant-design/icons'
import './TradePage.css'

const TradePage: React.FC = () => {
  return (
    <div className="trade-page">
      <div className="trade-header">
        <h1><ShoppingCartOutlined /> 交易终端</h1>
        <div className="account-info">
          <div>账户余额: ¥500,000</div>
          <div>可用资金: ¥350,000</div>
          <div>今日收益: +¥12,000</div>
        </div>
      </div>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <Card title="交易面板">
            <div style={{ padding: '40px', textAlign: 'center' }}>
              <h3>交易功能</h3>
              <p>买入、卖出和订单管理将在此处显示</p>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} lg={16}>
          <Card title="当前持仓">
            <div style={{ padding: '40px', textAlign: 'center' }}>
              <h3>持仓信息</h3>
              <p>当前持仓和订单记录将在此处显示</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default TradePage