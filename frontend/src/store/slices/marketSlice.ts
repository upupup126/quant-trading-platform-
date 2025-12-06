import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { KLineData, OrderBookData, MarketData } from '@/types'

interface MarketState {
  currentSymbol: string
  klineData: KLineData[]
  orderBook: OrderBookData | null
  marketList: MarketData[]
  selectedPeriod: string
  loading: boolean
  error: string | null
}

const initialState: MarketState = {
  currentSymbol: 'BTCUSDT',
  klineData: [],
  orderBook: null,
  marketList: [],
  selectedPeriod: '1m',
  loading: false,
  error: null,
}

export const marketSlice = createSlice({
  name: 'market',
  initialState,
  reducers: {
    setCurrentSymbol: (state, action: PayloadAction<string>) => {
      state.currentSymbol = action.payload
    },
    
    setKlineData: (state, action: PayloadAction<KLineData[]>) => {
      state.klineData = action.payload
    },
    
    addKlineData: (state, action: PayloadAction<KLineData>) => {
      state.klineData.push(action.payload)
    },
    
    setOrderBook: (state, action: PayloadAction<OrderBookData>) => {
      state.orderBook = action.payload
    },
    
    setMarketList: (state, action: PayloadAction<MarketData[]>) => {
      state.marketList = action.payload
    },
    
    setSelectedPeriod: (state, action: PayloadAction<string>) => {
      state.selectedPeriod = action.payload
    },
    
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    
    clearError: (state) => {
      state.error = null
    },
  },
})

export const {
  setCurrentSymbol,
  setKlineData,
  addKlineData,
  setOrderBook,
  setMarketList,
  setSelectedPeriod,
  setLoading,
  setError,
  clearError,
} = marketSlice.actions

export default marketSlice.reducer