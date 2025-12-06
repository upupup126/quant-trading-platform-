from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# 导入API路由
from app.api.market import router as market_router

# 创建FastAPI应用实例
app = FastAPI(
    title="量化交易平台API",
    description="提供量化交易相关功能的REST API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(market_router, prefix="/api/market", tags=["market"])

@app.get("/")
async def root():
    """根路径，返回服务状态"""
    return {
        "message": "量化交易平台API服务运行中",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "apis": {
            "market": "/api/market",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": ["api", "market"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )