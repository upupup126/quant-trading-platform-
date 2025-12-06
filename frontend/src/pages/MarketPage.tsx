import React, { useState, useEffect, useRef } from 'react'
import { Row, Col, Card, Table, Tag, Spin, Alert, Input, Radio, Checkbox, Space, Select, Empty } from 'antd'
import { LineChartOutlined, ArrowUpOutlined, ArrowDownOutlined, LoadingOutlined, SearchOutlined } from '@ant-design/icons'
import * as echarts from 'echarts'
import './MarketPage.css'

// 接口定义
interface MarketSummary {
  total_market_cap: number
  daily_volume: number
  btc_dominance: number
}

interface SymbolData {
  symbol: string
  name: string
  price: number
  price_change: number
  price_change_percent: number
  volume_24h: number
  market_cap: number
}

interface KLineData {
  timestamp: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

interface OrderBookEntry {
  price: number
  amount: number
  total: number
}

// 技术指标计算辅助函数
const calculateMA = (dayCount: number, data: KLineData[]) => {
  const result = [];
  for (let i = 0, len = data.length; i < len; i++) {
    if (i < dayCount - 1) {
      result.push('-');
      continue;
    }
    let sum = 0;
    for (let j = 0; j < dayCount; j++) {
      sum += data[i - j].close;
    }
    result.push(+(sum / dayCount).toFixed(2));
  }
  return result;
};

const MarketPage: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [marketSummary, setMarketSummary] = useState<MarketSummary>({ total_market_cap: 0, daily_volume: 0, btc_dominance: 0 })
  const [symbolsData, setSymbolsData] = useState<SymbolData[]>([])
  const [filteredSymbols, setFilteredSymbols] = useState<SymbolData[]>([])
  const [klineData, setKlineData] = useState<KLineData[]>([])
  const [orderBook, setOrderBook] = useState<{ bids: OrderBookEntry[], asks: OrderBookEntry[] }>({ bids: [], asks: [] })
  
  // 新增状态
  const [selectedSymbol, setSelectedSymbol] = useState<string>('000001.SH')
  const [selectedSymbolName, setSelectedSymbolName] = useState<string>('上证指数')
  const [period, setPeriod] = useState<string>('1d')
  const [indicators, setIndicators] = useState<string[]>(['MA', 'VOL'])
  const [searchText, setSearchText] = useState<string>('')
  
  const chartRef = useRef<HTMLDivElement>(null)
  const chartInstance = useRef<echarts.ECharts | null>(null)

  // 监听窗口大小变化，调整图表大小
  useEffect(() => {
    const handleResize = () => {
      chartInstance.current?.resize()
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // 初始化图表
  useEffect(() => {
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }
    return () => {
      chartInstance.current?.dispose()
    }
  }, [])

  // 更新图表数据
  useEffect(() => {
    if (!chartInstance.current || klineData.length === 0) return

    const dates = klineData.map(item => item.timestamp.split('T')[0])
    const data = klineData.map(item => [item.open, item.close, item.low, item.high, item.volume])

    const ma5 = calculateMA(5, klineData)
    const ma10 = calculateMA(10, klineData)
    const ma20 = calculateMA(20, klineData)
    const ma30 = calculateMA(30, klineData)

    const option: echarts.EChartsOption = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        textStyle: {
          color: '#000'
        },
      },
      axisPointer: {
        link: [{ xAxisIndex: 'all' }],
        label: {
          backgroundColor: '#777'
        }
      },
      legend: {
        data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
        top: 0,
        left: 'center'
      },
      grid: [
        {
          left: '10%',
          right: '8%',
          height: '60%'
        },
        {
          left: '10%',
          right: '8%',
          top: '75%',
          height: '15%'
        }
      ],
      xAxis: [
        {
          type: 'category',
          data: dates,
          scale: true,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          min: 'dataMin',
          max: 'dataMax',
          axisPointer: {
            z: 100
          }
        },
        {
          type: 'category',
          gridIndex: 1,
          data: dates,
          scale: true,
          boundaryGap: false,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          min: 'dataMin',
          max: 'dataMax'
        }
      ],
      yAxis: [
        {
          scale: true,
          splitArea: {
            show: true
          }
        },
        {
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }
      ],
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 50,
          end: 100
        },
        {
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '92%',
          start: 50,
          end: 100
        }
      ],
      series: [
        {
          name: '日K',
          type: 'candlestick',
          data: data.map(item => item.slice(0, 4)),
          itemStyle: {
            color: '#ef232a',
            color0: '#14b143',
            borderColor: '#ef232a',
            borderColor0: '#14b143'
          },
        },
        {
          name: 'MA5',
          type: 'line',
          data: ma5,
          smooth: true,
          lineStyle: { opacity: 0.5 }
        },
        {
          name: 'MA10',
          type: 'line',
          data: ma10,
          smooth: true,
          lineStyle: { opacity: 0.5 }
        },
        {
          name: 'MA20',
          type: 'line',
          data: ma20,
          smooth: true,
          lineStyle: { opacity: 0.5 }
        },
        {
          name: 'MA30',
          type: 'line',
          data: ma30,
          smooth: true,
          lineStyle: { opacity: 0.5 }
        },
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.map((item, index) => {
            return {
              value: item[4],
              itemStyle: {
                color: item[1] > item[0] ? '#ef232a' : '#14b143'
              }
            }
          })
        }
      ]
    }

    // 根据指标显示/隐藏 Series
    if (!indicators.includes('MA')) {
      option.series = (option.series as any[]).filter(s => s.type !== 'line')
      option.legend = { ...option.legend, selected: { 'MA5': false, 'MA10': false, 'MA20': false, 'MA30': false } }
    }
    
    if (!indicators.includes('VOL')) {
       // 隐藏 Volume Grid 和 Series
       // 简化处理：这里暂时不动态调整 Grid 高度，只是隐藏数据
       const volSeriesIndex = (option.series as any[]).findIndex(s => s.name === 'Volume');
       if (volSeriesIndex > -1) {
         (option.series as any[])[volSeriesIndex].data = [];
       }
    }

    chartInstance.current.setOption(option, true)
  }, [klineData, indicators])

  // 搜索过滤
  useEffect(() => {
    if (!searchText) {
      setFilteredSymbols(symbolsData)
    } else {
      const lowerText = searchText.toLowerCase()
      const filtered = symbolsData.filter(s => 
        s.symbol.toLowerCase().includes(lowerText) || 
        s.name.toLowerCase().includes(lowerText)
      )
      setFilteredSymbols(filtered)
    }
  }, [searchText, symbolsData])

  // 加载数据
  useEffect(() => {
    const loadData = async () => {
      // 仅在首次加载或切换股票时显示 loading，定时刷新时不显示全屏 loading
      if (symbolsData.length === 0) setLoading(true)
      setError(null)
      
      try {
        // 加载市场摘要
        const summaryResponse = await fetch('/api/market/summary')
        if (!summaryResponse.ok) throw new Error('获取市场摘要失败')
        const summaryData = await summaryResponse.json()
        setMarketSummary(summaryData)
        
        // 加载交易对列表
        const tickersResponse = await fetch('/api/market/tickers?limit=50')
        if (!tickersResponse.ok) throw new Error('获取行情列表失败')
        const tickersData = await tickersResponse.json()
        
        const convertedSymbols = tickersData.map((item: any) => ({
          symbol: item.symbol,
          name: item.name || item.symbol,
          price: item.last_price,
          price_change: item.price_change,
          price_change_percent: item.price_change_percent,
          volume_24h: item.volume,
          market_cap: 0 // 后端暂未返回市值
        }))
        setSymbolsData(convertedSymbols)
        
        // 如果当前选中的 symbol 不在列表中（且列表不为空），默认选中第一个
        if (convertedSymbols.length > 0 && !convertedSymbols.find((s: SymbolData) => s.symbol === selectedSymbol)) {
           // 保持当前选中不变，或者切换到第一个？
           // 如果是初始化，可能需要切换。但这里 selectedSymbol 有默认值。
           // 如果默认值 '000001.SH' 不在列表中，可能导致 K 线图加载失败（如果后端也没有这个 symbol 的数据）。
           // 稳妥起见，如果列表里没有当前选中的，就切到第一个。
           // 但考虑到用户可能手动输入了 symbol，或者 symbol 在分页之外，暂时不强制切换，除非是初始状态且默认值无效。
           // 这里简单处理：如果 symbolsData 为空（首次加载），且默认的 '000001.SH' 不在返回列表中，则切换到第一个。
           if (symbolsData.length === 0) {
              const defaultInList = convertedSymbols.find((s: SymbolData) => s.symbol === selectedSymbol)
              if (!defaultInList) {
                  setSelectedSymbol(convertedSymbols[0].symbol)
                  setSelectedSymbolName(convertedSymbols[0].name)
              }
           }
        }

        // 加载K线数据
        // 注意：如果 selectedSymbol 发生变化（上面逻辑触发），这里的 fetch 可能还是用的旧 symbol，
        // 但由于 useEffect 依赖了 selectedSymbol，setSelectedSymbol 会触发新的 effect，所以这里没问题。
        // 不过为了避免竞态，最好使用当前的 selectedSymbol。
        // 但由于 setSelectedSymbol 是异步的，这里还是用的旧值。
        // 实际上，如果 symbol 变了，会触发下一次 useEffect。
        // 所以这里只负责加载当前 selectedSymbol 的数据。
        
        const klineResponse = await fetch(`/api/market/simple-kline/${selectedSymbol}?interval=${period}&limit=100`)
        if (!klineResponse.ok) {
          throw new Error('获取K线数据失败')
        }
        const klineDataRes = await klineResponse.json()
        const convertedKlineData = klineDataRes.map((item: any) => ({
          timestamp: item.time,
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
          volume: item.volume
        }))
        setKlineData(convertedKlineData)
        
        // 加载盘口数据
        const orderBookResponse = await fetch(`/api/market/simple-orderbook/${selectedSymbol}?depth=10`)
        if (!orderBookResponse.ok) {
          throw new Error('获取盘口数据失败')
        }
        const orderBookData = await orderBookResponse.json()
        const convertedBids = orderBookData.bids.map((bid: any) => ({
          price: bid.price,
          amount: bid.amount,
          total: bid.total
        }))
        const convertedAsks = orderBookData.asks.map((ask: any) => ({
          price: ask.price,
          amount: ask.amount,
          total: ask.total
        }))
        setOrderBook({ bids: convertedBids, asks: convertedAsks })
        
      } catch (err) {
        setError(err instanceof Error ? err.message : '加载数据失败')
        console.error('加载市场数据失败:', err)
        // 移除假数据生成逻辑
      } finally {
        setLoading(false)
      }
    }
    
    loadData()
    
    const interval = setInterval(loadData, 30000)
    return () => clearInterval(interval)
  }, [selectedSymbol, period]) // 依赖 selectedSymbol 和 period
  
  // 格式化数字
  const formatNumber = (num: number): string => {
    if (num >= 1000000000000) return `¥${(num / 1000000000000).toFixed(2)}万亿`
    if (num >= 10000000000) return `¥${(num / 10000000000).toFixed(1)}百亿`
    if (num >= 100000000) return `¥${(num / 100000000).toFixed(2)}亿`
    if (num >= 10000) return `¥${(num / 10000).toFixed(2)}万`
    if (num >= 1000) return `¥${(num / 1000).toFixed(2)}千`
    return `¥${num.toFixed(2)}`
  }
  
  // 表格列定义
  const columns = [
    {
      title: '交易对',
      dataIndex: 'symbol',
      key: 'symbol',
      sorter: (a: SymbolData, b: SymbolData) => a.symbol.localeCompare(b.symbol),
      render: (text: string, record: SymbolData) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{record.name}</div>
          <div style={{ fontSize: '12px', color: '#888' }}>{text}</div>
        </div>
      ),
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      sorter: (a: SymbolData, b: SymbolData) => a.price - b.price,
      render: (text: number) => text.toFixed(2),
    },
    {
      title: '涨跌幅',
      dataIndex: 'price_change_percent',
      key: 'price_change_percent',
      sorter: (a: SymbolData, b: SymbolData) => a.price_change_percent - b.price_change_percent,
      render: (percent: number) => (
        <span style={{ color: percent >= 0 ? '#f5222d' : '#52c41a' }}>
          {percent >= 0 ? '+' : ''}{percent.toFixed(2)}%
        </span>
      ),
    },
  ]
  
  const currentPrice = klineData.length > 0 ? klineData[klineData.length - 1].close : 0
  const currentChange = klineData.length > 0 ? 
    ((klineData[klineData.length - 1].close - klineData[klineData.length - 1].open) / klineData[klineData.length - 1].open * 100) : 0
  
  if (loading && symbolsData.length === 0) {
    return (
      <div className="loading-spinner">
        <Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
        <p style={{ marginTop: 16 }}>正在加载行情数据...</p>
      </div>
    )
  }
  
  if (error && symbolsData.length === 0) {
    return (
      <div className="error-message">
        <Alert message="数据加载失败" description={error} type="error" showIcon />
      </div>
    )
  }
  
  return (
    <div className="market-page">
      <div className="market-header">
        <h1><LineChartOutlined /> A股行情中心</h1>
        <div className="market-summary">
          <div className="summary-item">
            <div className="summary-label">A股总市值</div>
            <div className="summary-value">{formatNumber(marketSummary.total_market_cap)}</div>
          </div>
          <div className="summary-item">
            <div className="summary-label">日交易额</div>
            <div className="summary-value">{formatNumber(marketSummary.daily_volume)}</div>
          </div>
          <div className="summary-item">
            <div className="summary-label">上证指数</div>
            <div className="summary-value">
              {symbolsData.find(s => s.symbol === '000001.SH') 
                ? `${symbolsData.find(s => s.symbol === '000001.SH')?.price.toFixed(2)}点` 
                : '--'}
            </div>
          </div>
        </div>
      </div>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Card 
            title={
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span>{selectedSymbolName} ({selectedSymbol})</span>
                <Space>
                  <Radio.Group value={period} onChange={e => setPeriod(e.target.value)} size="small">
                    <Radio.Button value="1m">1分</Radio.Button>
                    <Radio.Button value="5m">5分</Radio.Button>
                    <Radio.Button value="15m">15分</Radio.Button>
                    <Radio.Button value="1h">1小时</Radio.Button>
                    <Radio.Button value="4h">4小时</Radio.Button>
                    <Radio.Button value="1d">日线</Radio.Button>
                  </Radio.Group>
                  <Checkbox.Group 
                    options={['MA', 'VOL']} 
                    value={indicators} 
                    onChange={(vals) => setIndicators(vals as string[])} 
                  />
                </Space>
              </div>
            }
          >
            <div ref={chartRef} style={{ height: '500px', width: '100%' }}></div>
          </Card>
        </Col>
        
        <Col xs={24} lg={8}>
          <Row gutter={[0, 16]}>
            <Col span={24}>
              <Card title="盘口数据" size="small">
                {orderBook.bids.length > 0 ? (
                  <div style={{ display: 'flex', gap: '16px', fontSize: '12px' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#888', marginBottom: 4 }}>
                        <span>价格</span><span>数量</span>
                      </div>
                      {orderBook.asks.slice().reverse().map((ask, index) => (
                        <div key={index} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
                          <span style={{ color: '#f5222d' }}>{ask.price.toFixed(2)}</span>
                          <span>{ask.amount}</span>
                        </div>
                      ))}
                      <div style={{ borderTop: '1px solid #eee', margin: '4px 0' }}></div>
                      {orderBook.bids.map((bid, index) => (
                        <div key={index} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
                          <span style={{ color: '#52c41a' }}>{bid.price.toFixed(2)}</span>
                          <span>{bid.amount}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />}
              </Card>
            </Col>
            <Col span={24}>
              <Card 
                title="市场概览" 
                size="small"
                extra={
                  <Input 
                    placeholder="搜索股票代码/名称" 
                    prefix={<SearchOutlined />} 
                    size="small" 
                    style={{ width: 150 }}
                    onChange={e => setSearchText(e.target.value)}
                  />
                }
              >
                <Table 
                  dataSource={filteredSymbols}
                  columns={columns}
                  pagination={{ pageSize: 10, size: 'small' }}
                  size="small"
                  scroll={{ y: 300 }}
                  rowKey="symbol"
                  onRow={(record) => ({
                    onClick: () => {
                      setSelectedSymbol(record.symbol)
                      setSelectedSymbolName(record.name)
                    },
                    style: { cursor: 'pointer', backgroundColor: selectedSymbol === record.symbol ? '#e6f7ff' : '' }
                  })}
                />
              </Card>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  )
}

export default MarketPage