import React from 'react'
import { Card } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import './StrategyPage.css'

const StrategyPage: React.FC = () => {
  return (
    <div className="strategy-page">
      <div className="strategy-header">
        <h1>策略管理</h1>
        <div>
          功能开发中...
        </div>
      </div>
      
      <Card title="我的策略">
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <h3>策略管理功能</h3>
          <p>策略创建、编辑和回测功能将在此处显示</p>
        </div>
      </Card>
    </div>
  )
}

export default StrategyPage