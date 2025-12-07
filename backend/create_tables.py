#!/usr/bin/env python3
"""
自动创建数据库表的脚本
用于解决错误: (pymysql.err.ProgrammingError) (1146, "Table 'quant_trading.market_data' doesn't exist")

使用方法:
1. 确保数据库服务正在运行
2. 配置正确的数据库连接（在.env文件中）
3. 运行此脚本: python create_tables.py
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import create_tables, test_connection
from app.core.database import engine
from sqlalchemy import text


def check_database_exists():
    """检查数据库是否存在"""
    try:
        # 尝试连接到MySQL服务器
        with engine.connect() as conn:
            # 获取当前连接的数据库
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"当前数据库: {db_name}")
            
            # 检查market_data表是否存在
            result = conn.execute(text("SHOW TABLES LIKE 'market_data'"))
            table_exists = result.fetchone() is not None
            
            if table_exists:
                print("✅ market_data表已存在")
                # 显示表结构
                result = conn.execute(text("DESCRIBE market_data"))
                columns = result.fetchall()
                print("表结构:")
                for col in columns:
                    print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            else:
                print("❌ market_data表不存在")
            
            return table_exists
            
    except Exception as e:
        print(f"❌ 检查数据库时出错: {e}")
        return False


def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    try:
        # 从连接URL中提取数据库名称
        url = str(engine.url)
        if 'mysql' in url:
            # 解析连接字符串获取数据库名
            import re
            match = re.search(r'/([^/?]+)(?:\?|$)', url)
            if match:
                db_name = match.group(1)
                print(f"数据库名称: {db_name}")
                
                # 创建临时连接（不带数据库名）
                temp_url = re.sub(r'/[^/?]+(?:\?|$)', '/', url)
                temp_engine = type(engine)(temp_url)
                
                with temp_engine.connect() as conn:
                    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                    print(f"✅ 数据库 {db_name} 已创建或已存在")
                    conn.execute(text(f"USE {db_name}"))
                
                return True
        return False
    except Exception as e:
        print(f"❌ 创建数据库时出错: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("量化交易平台 - 数据库表创建工具")
    print("=" * 60)
    
    # 检查数据库连接
    print("\n1. 检查数据库连接...")
    if not test_connection():
        print("❌ 数据库连接失败")
        print("请检查:")
        print("  1. MySQL服务是否运行: sudo systemctl status mysql")
        print("  2. 数据库连接配置是否正确（.env文件）")
        print("  3. 用户名和密码是否正确")
        
        # 尝试创建数据库
        print("\n尝试创建数据库...")
        if create_database_if_not_exists():
            print("✅ 数据库创建成功，请重新运行此脚本")
        return
    
    print("✅ 数据库连接成功")
    
    # 检查表是否存在
    print("\n2. 检查表状态...")
    table_exists = check_database_exists()
    
    if table_exists:
        print("\n✅ 所有表已存在，无需创建")
        return
    
    # 创建表
    print("\n3. 创建数据表...")
    try:
        create_tables()
        print("✅ 数据表创建成功！")
        
        # 再次检查确认
        print("\n4. 验证表创建...")
        check_database_exists()
        
        print("\n🎉 数据库表创建完成！")
        print("您现在可以运行 collect_a_share_data.py 脚本了")
        
    except Exception as e:
        print(f"❌ 创建表时出错: {e}")
        print("\n可能的解决方案:")
        print("  1. 手动执行SQL文件: mysql -u root -p quant_trading < schema.sql")
        print("  2. 检查数据库权限")
        print("  3. 检查数据库连接配置")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()
