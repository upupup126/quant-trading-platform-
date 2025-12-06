import { configureStore } from '@reduxjs/toolkit'
import marketReducer from './slices/marketSlice'
import strategyReducer from './slices/strategySlice'
import tradeReducer from './slices/tradeSlice'
import portfolioReducer from './slices/portfolioSlice'

export const store = configureStore({
  reducer: {
    market: marketReducer,
    strategy: strategyReducer,
    trade: tradeReducer,
    portfolio: portfolioReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch