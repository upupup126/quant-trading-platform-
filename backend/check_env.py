#!/usr/bin/env python3
"""
环境检查脚本
检查并安装必需的Python依赖
"""

import sys
import subprocess
import os

def check_module(module_name):
    """检查模块是否已安装"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {module_name} 未安装")
        return False

def main():
    """主函数"""
    print("=== 环境依赖检查 ===")
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查必需模块
    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "sqlalchemy.orm",
        "datetime",
        "typing",
        "json"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ 缺少 {len(missing_modules)} 个模块: {', '.join(missing_modules)}")
        print("请执行以下命令安装依赖:")
        print("pip install fastapi uvicorn pydantic sqlalchemy")
        print("\n或直接从requirements.txt安装:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依赖已满足")
        
        # 尝试导入项目模块
        print("\n=== 项目模块检查 ===")
        try:
            # 添加当前目录到Python路径
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            
            # 尝试导入schemas
            from app.schemas.market import KLineData
            print("✅ app.schemas.market 导入成功")
            
            # 尝试导入models
            from app.models.market import MarketData
            print("✅ app.models.market 导入成功")
            
            # 尝试导入services
            from app.services.market_service import MarketService
            print("✅ app.services.market_service 导入成功")
            
            # 尝试导入api
            from app.api.market import router
            print("✅ app.api.market 导入成功")
            
            print("\n🎉 所有项目模块导入成功！")
            return True
            
        except Exception as e:
            print(f"❌ 项目模块导入失败: {e}")
            print("\n请确保:")
            print("1. 所有必需依赖已安装")
            print("2. 项目目录结构完整")
            print("3. 数据库连接配置正确")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)