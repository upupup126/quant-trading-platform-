import React from 'react'
import { Row, Col, Card } from 'antd'
import { PieChartOutlined } from '@ant-design/icons'
import './PortfolioPage.css'

const PortfolioPage: React.FC = () => {
  return (
    <div className="portfolio-page">
      <div className="portfolio-header">
        <h1><PieChartOutlined /> 资产监控</h1>
        <div>
          功能开发中...
        </div>
      </div>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <Card title="投资组合概览">
            <div style={{ padding: '20px', textAlign: 'center' }}>
              <h3>总资产</h3>
              <p style={{ fontSize: '24px', color: '#1890ff' }}>¥512,000</p>
              <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '16px' }}>
                <div>
                  <div>总收益</div>
                  <div style={{ color: '#ff4d4f' }}>+¥12,000</div>
                </div>
                <div>
                  <div>收益率</div>
                  <div style={{ color: '#ff4d4f' }}>+2.4%</div>
                </div>
              </div>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} lg={16}>
          <Card title="收益曲线">
            <div style={{ padding: '40px', textAlign: 'center' }}>
              <h3>资产净值变化</h3>
              <p>收益曲线图表将在此处显示</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default PortfolioPage