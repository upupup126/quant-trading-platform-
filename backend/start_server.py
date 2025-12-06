#!/usr/bin/env python3
"""
后端服务启动脚本
用于启动FastAPI服务器
"""

import sys
import os
import subprocess

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_and_install_deps():
    """检查并提示安装依赖"""
    print("\n=== 依赖检查 ===")
    
    # 尝试导入必需模块
    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy"
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} 已安装")
        except ImportError:
            print(f"❌ {module} 未安装")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️ 缺少以下依赖: {', '.join(missing)}")
        print("\n请执行以下命令安装依赖:")
        print("pip install fastapi uvicorn pydantic sqlalchemy")
        print("\n或从requirements.txt安装:")
        print("pip install -r requirements.txt")
        print("\n安装完成后重新运行此脚本。")
        return False
    
    return True

def start_dev_server():
    """启动开发服务器"""
    print("\n=== 启动后端服务 ===")
    print("服务将运行在: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        # 导入并运行FastAPI应用
        from main import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True
        )
    except Exception as e:
        print(f"\n❌ 启动服务失败: {e}")
        print("\n常见问题解决方案:")
        print("1. 确保所有依赖已安装")
        print("2. 检查端口8000是否被占用")
        print("3. 检查数据库配置是否正确")
        return False
    
    return True

def create_test_data():
    """创建测试数据（如果需要）"""
    print("\n=== 创建测试数据 ===")
    
    # 这里可以添加创建测试数据库或示例数据的代码
    print("测试数据将在首次API调用时自动生成")
    
    # 确保必要的目录存在
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ 创建数据目录: {data_dir}")
    
    return True

def main():
    """主函数"""
    print("🚀 量化交易平台 - 后端服务")
    print("=" * 50)
    
    # 检查依赖
    if not check_and_install_deps():
        return 1
    
    # 创建测试数据
    create_test_data()
    
    # 启动服务
    return 0 if start_dev_server() else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生未预期的错误: {e}")
        sys.exit(1)