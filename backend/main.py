from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# 导入日志配置
from app.core.logging_config import get_app_logger, log_manager

# 获取应用日志记录器
app_logger = get_app_logger()

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

# 应用启动时记录日志
app_logger.info("=" * 60)
app_logger.info("量化交易平台API服务启动中...")
app_logger.info(f"服务名称: {app.title}")
app_logger.info(f"服务版本: {app.version}")
app_logger.info(f"文档地址: /docs")
app_logger.info(f"服务时间: {datetime.now().isoformat()}")
app_logger.info("=" * 60)

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
    app_logger.info("根路径访问")
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
    app_logger.info("健康检查接口访问")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": ["api", "market"]
    }

if __name__ == "__main__":
    # 记录服务器启动信息
    app_logger.info("启动FastAPI服务器...")
    app_logger.info(f"服务器地址: http://0.0.0.0:8000")
    app_logger.info(f"API文档: http://0.0.0.0:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

    # 服务器关闭时记录
    app_logger.info("FastAPI服务器已停止")