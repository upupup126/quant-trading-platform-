from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'sqlite:///./quant_trading.db'
)

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    poolclass=StaticPool if DATABASE_URL.startswith("sqlite") else None,
    echo=False  # 生产环境设为False
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

def get_db():
    """
    获取数据库会话的依赖函数
    使用示例：
    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        items = db.query(Item).all()
        return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """创建所有数据表"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """删除所有数据表（仅用于测试）"""
    Base.metadata.drop_all(bind=engine)

# 数据库连接测试
def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as conn:
            print("数据库连接成功")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False