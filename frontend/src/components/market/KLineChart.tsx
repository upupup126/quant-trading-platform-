import React, { useEffect, useRef, useMemo } from 'react'
import * as echarts from 'echarts'
import { KLineData } from '@/types'
import './KLineChart.css'

interface KLineChartProps {
  data: KLineData[]
  period: string
  type: 'kline' | 'line'
  indicators?: string[]
  height?: number
}

const KLineChart: React.FC<KLineChartProps> = ({
  data,
  period,
  type = 'kline',
  indicators = [],
  height = 400
}) => {
  const chartRef = useRef<HTMLDivElement>(null)
  const chartInstance = useRef<echarts.ECharts | null>(null)
  
  // 处理K线数据
  const processedData = useMemo(() => {
    if (type === 'kline') {
      return data.map(item => [
        new Date(item.timestamp).getTime(),
        item.open,
        item.close,
        item.low,
        item.high,
        item.volume
      ])
    } else {
      return data.map(item => [
        new Date(item.timestamp).getTime(),
        item.close
      ])
    }
  }, [data, type])
  
  // 计算技术指标
  const calculateMA = (data: any[], period: number) => {
    const result = []
    for (let i = 0; i < data.length; i++) {
      if (i < period) {
        result.push(null)
        continue
      }
      let sum = 0
      for (let j = 0; j < period; j++) {
        sum += data[i - j][2] // 收盘价
      }
      result.push(sum / period)
    }
    return result
  }
  
  const maData = useMemo(() => {
    if (indicators.includes('MA5')) {
      return calculateMA(processedData, 5)
    }
    return []
  }, [processedData, indicators])
  
  // 配置图表选项
  const getOption = (): echarts.EChartsOption => {
    const baseOption: echarts.EChartsOption = {
      animation: false,
      legend: {
        top: 10,
        left: 'center',
        data: type === 'kline' ? ['K线', 'MA5'] : ['分时线']
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        borderWidth: 1,
        borderColor: '#ccc',
        backgroundColor: 'rgba(255,255,255,0.9)',
        textStyle: {
          color: '#000'
        },
        formatter: (params: any) => {
          const param = params[0]
          const date = new Date(param.value[0])
          const dateStr = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
          
          if (type === 'kline') {
            return `
              <div style="font-weight: bold; margin-bottom: 5px;">${dateStr}</div>
              <div>开盘: ${param.value[1]}</div>
              <div>收盘: ${param.value[2]}</div>
              <div>最低: ${param.value[3]}</div>
              <div>最高: ${param.value[4]}</div>
              <div>成交量: ${param.value[5]}</div>
            `
          } else {
            return `
              <div style="font-weight: bold; margin-bottom: 5px;">${dateStr}</div>
              <div>价格: ${param.value[1]}</div>
            `
          }
        }
      },
      axisPointer: {
        link: [{ xAxisIndex: 'all' }]
      },
      grid: [
        {
          left: '10%',
          right: '8%',
          top: '15%',
          height: '60%'
        },
        {
          left: '10%',
          right: '8%',
          top: '80%',
          height: '15%'
        }
      ],
      xAxis: [
        {
          type: 'time',
          scale: true,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          splitNumber: 20,
          min: 'dataMin',
          max: 'dataMax'
        },
        {
          type: 'time',
          gridIndex: 1,
          scale: true,
          boundaryGap: false,
          axisLine: { onZero: false },
          axisTick: { show: false },
          axisLabel: { show: false },
          splitLine: { show: false },
          splitNumber: 20,
          min: 'dataMin',
          max: 'dataMax'
        }
      ],
      yAxis: [
        {
          scale: true,
          splitArea: { show: true }
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
          start: 0,
          end: 100
        },
        {
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '95%',
          start: 0,
          end: 100
        }
      ]
    }
    
    const series: echarts.SeriesOption[] = []
    
    if (type === 'kline') {
      series.push({
        name: 'K线',
        type: 'candlestick',
        data: processedData,
        itemStyle: {
          color: '#ec0000',
          color0: '#00da3c',
          borderColor: '#8A0000',
          borderColor0: '#008F28'
        }
      })
      
      if (indicators.includes('MA5')) {
        series.push({
          name: 'MA5',
          type: 'line',
          data: maData.map((value, index) => [
            processedData[index][0],
            value
          ]),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        })
      }
    } else {
      series.push({
        name: '分时线',
        type: 'line',
        data: processedData,
        smooth: true,
        lineStyle: {
          color: '#1890ff'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
            { offset: 1, color: 'rgba(24, 144, 255, 0.1)' }
          ])
        }
      })
    }
    
    // 成交量柱状图
    if (type === 'kline') {
      series.push({
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: processedData.map(item => [item[0], item[5]]),
        itemStyle: {
          color: (params: any) => {
            const data = params.data
            return data[1] >= 0 ? '#00da3c' : '#ec0000'
          }
        }
      })
    }
    
    return { ...baseOption, series }
  }
  
  // 初始化图表
  useEffect(() => {
    if (!chartRef.current) return
    
    chartInstance.current = echarts.init(chartRef.current)
    chartInstance.current.setOption(getOption())
    
    const handleResize = () => {
      chartInstance.current?.resize()
    }
    
    window.addEventListener('resize', handleResize)
    
    return () => {
      window.removeEventListener('resize', handleResize)
      chartInstance.current?.dispose()
    }
  }, [])
  
  // 更新图表数据
  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.setOption(getOption())
    }
  }, [data, type, indicators, period])
  
  return (
    <div 
      ref={chartRef} 
      className="kline-chart" 
      style={{ height: `${height}px` }}
    />
  )
}

export default KLineChart