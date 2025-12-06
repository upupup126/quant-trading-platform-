import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Strategy, BacktestResult, StrategyParameter } from '@/types'

interface StrategyState {
  strategies: Strategy[]
  currentStrategy: Strategy | null
  backtestResults: BacktestResult[]
  currentBacktest: BacktestResult | null
  parameters: StrategyParameter[]
  isEditing: boolean
  isRunning: boolean
  loading: boolean
  error: string | null
}

const initialState: StrategyState = {
  strategies: [],
  currentStrategy: null,
  backtestResults: [],
  currentBacktest: null,
  parameters: [],
  isEditing: false,
  isRunning: false,
  loading: false,
  error: null,
}

export const strategySlice = createSlice({
  name: 'strategy',
  initialState,
  reducers: {
    setStrategies: (state, action: PayloadAction<Strategy[]>) => {
      state.strategies = action.payload
    },
    
    addStrategy: (state, action: PayloadAction<Strategy>) => {
      state.strategies.push(action.payload)
    },
    
    updateStrategy: (state, action: PayloadAction<Strategy>) => {
      const index = state.strategies.findIndex(s => s.id === action.payload.id)
      if (index !== -1) {
        state.strategies[index] = action.payload
      }
    },
    
    deleteStrategy: (state, action: PayloadAction<string>) => {
      state.strategies = state.strategies.filter(s => s.id !== action.payload)
    },
    
    setCurrentStrategy: (state, action: PayloadAction<Strategy | null>) => {
      state.currentStrategy = action.payload
    },
    
    setBacktestResults: (state, action: PayloadAction<BacktestResult[]>) => {
      state.backtestResults = action.payload
    },
    
    addBacktestResult: (state, action: PayloadAction<BacktestResult>) => {
      state.backtestResults.push(action.payload)
    },
    
    setCurrentBacktest: (state, action: PayloadAction<BacktestResult | null>) => {
      state.currentBacktest = action.payload
    },
    
    setParameters: (state, action: PayloadAction<StrategyParameter[]>) => {
      state.parameters = action.payload
    },
    
    updateParameter: (state, action: PayloadAction<{ name: string; value: any }>) => {
      const param = state.parameters.find(p => p.name === action.payload.name)
      if (param) {
        param.value = action.payload.value
      }
    },
    
    setIsEditing: (state, action: PayloadAction<boolean>) => {
      state.isEditing = action.payload
    },
    
    setIsRunning: (state, action: PayloadAction<boolean>) => {
      state.isRunning = action.payload
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
  setStrategies,
  addStrategy,
  updateStrategy,
  deleteStrategy,
  setCurrentStrategy,
  setBacktestResults,
  addBacktestResult,
  setCurrentBacktest,
  setParameters,
  updateParameter,
  setIsEditing,
  setIsRunning,
  setLoading,
  setError,
  clearError,
} = strategySlice.actions

export default strategySlice.reducer