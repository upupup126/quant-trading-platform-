import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { TradeRecord, Order, AccountInfo, Position } from '@/types'

interface TradeState {
  accountInfo: AccountInfo | null
  positions: Position[]
  orders: Order[]
  tradeHistory: TradeRecord[]
  currentOrder: Order | null
  loading: boolean
  error: string | null
  isPlacingOrder: boolean
  selectedPosition: Position | null
}

const initialState: TradeState = {
  accountInfo: null,
  positions: [],
  orders: [],
  tradeHistory: [],
  currentOrder: null,
  loading: false,
  error: null,
  isPlacingOrder: false,
  selectedPosition: null,
}

export const tradeSlice = createSlice({
  name: 'trade',
  initialState,
  reducers: {
    setAccountInfo: (state, action: PayloadAction<AccountInfo>) => {
      state.accountInfo = action.payload
    },
    
    updateAccountBalance: (state, action: PayloadAction<{ balance: number; available: number }>) => {
      if (state.accountInfo) {
        state.accountInfo.balance = action.payload.balance
        state.accountInfo.available = action.payload.available
        state.accountInfo.totalEquity = action.payload.balance
      }
    },
    
    setPositions: (state, action: PayloadAction<Position[]>) => {
      state.positions = action.payload
    },
    
    addPosition: (state, action: PayloadAction<Position>) => {
      state.positions.push(action.payload)
    },
    
    updatePosition: (state, action: PayloadAction<Position>) => {
      const index = state.positions.findIndex(p => p.symbol === action.payload.symbol)
      if (index !== -1) {
        state.positions[index] = action.payload
      }
    },
    
    removePosition: (state, action: PayloadAction<string>) => {
      state.positions = state.positions.filter(p => p.symbol !== action.payload)
    },
    
    setOrders: (state, action: PayloadAction<Order[]>) => {
      state.orders = action.payload
    },
    
    addOrder: (state, action: PayloadAction<Order>) => {
      state.orders.push(action.payload)
    },
    
    updateOrder: (state, action: PayloadAction<Order>) => {
      const index = state.orders.findIndex(o => o.id === action.payload.id)
      if (index !== -1) {
        state.orders[index] = action.payload
      }
    },
    
    removeOrder: (state, action: PayloadAction<string>) => {
      state.orders = state.orders.filter(o => o.id !== action.payload)
    },
    
    setTradeHistory: (state, action: PayloadAction<TradeRecord[]>) => {
      state.tradeHistory = action.payload
    },
    
    addTradeRecord: (state, action: PayloadAction<TradeRecord>) => {
      state.tradeHistory.push(action.payload)
    },
    
    setCurrentOrder: (state, action: PayloadAction<Order | null>) => {
      state.currentOrder = action.payload
    },
    
    setSelectedPosition: (state, action: PayloadAction<Position | null>) => {
      state.selectedPosition = action.payload
    },
    
    setIsPlacingOrder: (state, action: PayloadAction<boolean>) => {
      state.isPlacingOrder = action.payload
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
    
    clearTradeState: (state) => {
      state.accountInfo = null
      state.positions = []
      state.orders = []
      state.tradeHistory = []
      state.currentOrder = null
      state.selectedPosition = null
    },
  },
})

export const {
  setAccountInfo,
  updateAccountBalance,
  setPositions,
  addPosition,
  updatePosition,
  removePosition,
  setOrders,
  addOrder,
  updateOrder,
  removeOrder,
  setTradeHistory,
  addTradeRecord,
  setCurrentOrder,
  setSelectedPosition,
  setIsPlacingOrder,
  setLoading,
  setError,
  clearError,
  clearTradeState,
} = tradeSlice.actions

export default tradeSlice.reducer