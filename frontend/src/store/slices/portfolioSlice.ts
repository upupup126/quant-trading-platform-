import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { AccountInfo, Position, BacktestResult, EquityPoint } from '@/types'

interface PortfolioState {
  portfolios: Portfolio[]
  currentPortfolio: Portfolio | null
  accountInfo: AccountInfo | null
  positions: Position[]
  performance: PerformanceMetrics | null
  backtestResults: BacktestResult[]
  equityCurve: EquityPoint[]
  selectedTimeRange: '1d' | '1w' | '1m' | '3m' | '1y' | 'all'
  loading: boolean
  error: string | null
  isRefreshing: boolean
}

interface Portfolio {
  id: string
  name: string
  description: string
  initialCapital: number
  currentValue: number
  createdAt: string
  updatedAt: string
  symbols: string[]
  strategyIds: string[]
}

interface PerformanceMetrics {
  totalReturn: number
  annualReturn: number
  sharpeRatio: number
  maxDrawdown: number
  winRate: number
  totalTrades: number
  profitFactor: number
  averageWin: number
  averageLoss: number
}

const initialState: PortfolioState = {
  portfolios: [],
  currentPortfolio: null,
  accountInfo: null,
  positions: [],
  performance: null,
  backtestResults: [],
  equityCurve: [],
  selectedTimeRange: '1m',
  loading: false,
  error: null,
  isRefreshing: false,
}

export const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    setPortfolios: (state, action: PayloadAction<Portfolio[]>) => {
      state.portfolios = action.payload
    },
    
    addPortfolio: (state, action: PayloadAction<Portfolio>) => {
      state.portfolios.push(action.payload)
    },
    
    updatePortfolio: (state, action: PayloadAction<Portfolio>) => {
      const index = state.portfolios.findIndex(p => p.id === action.payload.id)
      if (index !== -1) {
        state.portfolios[index] = action.payload
      }
    },
    
    deletePortfolio: (state, action: PayloadAction<string>) => {
      state.portfolios = state.portfolios.filter(p => p.id !== action.payload)
    },
    
    setCurrentPortfolio: (state, action: PayloadAction<Portfolio | null>) => {
      state.currentPortfolio = action.payload
    },
    
    setAccountInfo: (state, action: PayloadAction<AccountInfo>) => {
      state.accountInfo = action.payload
    },
    
    setPositions: (state, action: PayloadAction<Position[]>) => {
      state.positions = action.payload
    },
    
    updatePosition: (state, action: PayloadAction<Position>) => {
      const index = state.positions.findIndex(p => p.symbol === action.payload.symbol)
      if (index !== -1) {
        state.positions[index] = action.payload
      }
    },
    
    setPerformance: (state, action: PayloadAction<PerformanceMetrics>) => {
      state.performance = action.payload
    },
    
    setBacktestResults: (state, action: PayloadAction<BacktestResult[]>) => {
      state.backtestResults = action.payload
    },
    
    addBacktestResult: (state, action: PayloadAction<BacktestResult>) => {
      state.backtestResults.push(action.payload)
    },
    
    setEquityCurve: (state, action: PayloadAction<EquityPoint[]>) => {
      state.equityCurve = action.payload
    },
    
    addEquityPoint: (state, action: PayloadAction<EquityPoint>) => {
      state.equityCurve.push(action.payload)
    },
    
    setSelectedTimeRange: (state, action: PayloadAction<'1d' | '1w' | '1m' | '3m' | '1y' | 'all'>) => {
      state.selectedTimeRange = action.payload
    },
    
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    
    setIsRefreshing: (state, action: PayloadAction<boolean>) => {
      state.isRefreshing = action.payload
    },
    
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    
    clearError: (state) => {
      state.error = null
    },
    
    clearPortfolioState: (state) => {
      state.currentPortfolio = null
      state.accountInfo = null
      state.positions = []
      state.performance = null
      state.backtestResults = []
      state.equityCurve = []
    },
  },
})

export const {
  setPortfolios,
  addPortfolio,
  updatePortfolio,
  deletePortfolio,
  setCurrentPortfolio,
  setAccountInfo,
  setPositions,
  updatePosition,
  setPerformance,
  setBacktestResults,
  addBacktestResult,
  setEquityCurve,
  addEquityPoint,
  setSelectedTimeRange,
  setLoading,
  setIsRefreshing,
  setError,
  clearError,
  clearPortfolioState,
} = portfolioSlice.actions

export default portfolioSlice.reducer