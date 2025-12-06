import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import MarketPage from './pages/MarketPage'
import StrategyPage from './pages/StrategyPage'
import TradePage from './pages/TradePage'
import PortfolioPage from './pages/PortfolioPage'
import './App.css'

const { Header, Content } = Layout

function App() {
  return (
    <Layout className="app-layout">
      <Header style={{ background: '#001529', color: 'white', padding: '0 24px' }}>
        <h1 style={{ color: 'white', margin: 0 }}>量化交易平台</h1>
      </Header>
      <Layout>
        <Content className="app-content">
          <Routes>
            <Route path="/" element={<MarketPage />} />
            <Route path="/market" element={<MarketPage />} />
            <Route path="/strategy" element={<StrategyPage />} />
            <Route path="/trade" element={<TradePage />} />
            <Route path="/portfolio" element={<PortfolioPage />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  )
}

export default App