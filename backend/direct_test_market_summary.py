#!/usr/bin/env python3
"""
直接测试 MarketService.get_market_summary 函数
用于诊断具体错误
"""

import sys
import os
import traceback

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("直接测试 MarketService.get_market_summary 函数")
print("=" * 60)

try:
    print("1. 导入模块...")
    from app.core.database import SessionLocal, engine, test_connection, create_tables
    from app.models.market import Base
    from app.services.market_service import MarketService
    print("   ✅ 模块导入成功")
    
    print("\n2. 测试数据库连接...")
    if test_connection():
        print("   ✅ 数据库连接成功")
    else:
        print("   ❌ 数据库连接失败")
        
    print("\n3. 创建数据表（如果不存在）...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ 数据表创建/验证成功")
    except Exception as e:
        print(f"   ⚠ 数据表创建失败: {e}")
    
    print("\n4. 创建数据库会话...")
    db = SessionLocal()
    print("   ✅ 数据库会话创建成功")
    
    try:
        print("\n5. 测试查询数据库中的表...")
        # 检查数据库中是否有数据
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"   ✅ 数据库表: {tables}")
        
        if 'symbol_info' in tables:
            # 查询数据数量
            from sqlalchemy import text
            result = db.execute(text("SELECT COUNT(*) FROM symbol_info")).fetchone()
            print(f"   ✅ SymbolInfo 表数据数量: {result[0]}")
        else:
            print("   ⚠ SymbolInfo 表不存在或为空")
            
        print("\n6. 直接调用 MarketService.get_market_summary()...")
        print("   开始执行查询...")
        
        try:
            # 设置超时保护
            import signal
            
            class TimeoutException(Exception):
                pass
            
            def timeout_handler(signum, frame):
                raise TimeoutException("查询超时（30秒）")
            
            # 设置超时（30秒）
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)
            
            summary = MarketService.get_market_summary(db)
            
            # 取消超时
            signal.alarm(0)
            
            print("   ✅ 函数调用成功！")
            print(f"   ✅ 返回数据: {summary}")
            
            # 验证关键字段
            required_fields = [
                'total_symbols',
                'market_type_counts', 
                'price_change_stats',
                'latest_update_time',
                'error'
            ]
            
            print("\n7. 验证返回数据字段:")
            for field in required_fields:
                if field in summary:
                    value = summary[field]
                    value_type = type(value).__name__
                    print(f"   ✅ {field}: 存在 (类型: {value_type}, 值: {value})")
                else:
                    print(f"   ❌ {field}: 缺失")
                    
            # 特别检查我们的修复
            if 'market_type_counts' in summary:
                counts = summary['market_type_counts']
                if counts:
                    keys = list(counts.keys())
                    print(f"   ✅ market_type_counts 键: {keys}")
                    if any(key is None for key in keys):
                        print("   ❌ 警告：存在 None 键（需要我们的修复）")
                    else:
                        print("   ✅ 所有键都是字符串（修复生效）")
                else:
                    print("   ⚠ market_type_counts 为空")
                    
            if 'error' in summary:
                if summary['error'] is None:
                    print("   ✅ error 字段为 None（正常）")
                else:
                    print(f"   ⚠ error 字段有值: {summary['error']}")
                    
            print("\n8. 使用 Pydantic 模型验证...")
            try:
                from app.schemas.market import MarketSummary
                model_instance = MarketSummary(**summary)
                print("   ✅ Pydantic 模型验证通过！")
                print(f"   ✅ 模型实例: {model_instance}")
                
                print("\n" + "=" * 60)
                print("✅ 测试成功！")
                print("✅ MarketService.get_market_summary 函数工作正常")
                print("✅ 我们的修复已生效")
                print("✅ 数据库查询成功")
                
            except Exception as e:
                print(f"   ❌ Pydantic 验证失败: {e}")
                print("   ⚠ 可能是数据类型不匹配或字段缺失")
                
        except TimeoutException as e:
            print(f"   ❌ {e}")
            print("   ⚠ 查询可能遇到死锁或性能问题")
            
        except Exception as e:
            print(f"   ❌ 函数调用失败: {type(e).__name__}")
            print(f"   错误信息: {e}")
            print("\n详细堆栈跟踪:")
            traceback.print_exc()
            
            # 尝试识别常见错误
            error_msg = str(e).lower()
            if "no such table" in error_msg:
                print("\n⚠ 问题识别: 数据表不存在")
                print("   解决方案: 运行数据库迁移或创建表")
            elif "syntax error" in error_msg:
                print("\n⚠ 问题识别: SQL 语法错误")
                print("   可能原因: SQLAlchemy case 表达式语法问题")
            elif "operationalerror" in error_msg:
                print("\n⚠ 问题识别: 数据库操作错误")
                print("   可能原因: 数据库文件权限或损坏")
            else:
                print("\n⚠ 未知错误类型，需要进一步诊断")
                
    finally:
        db.close()
        print("\n   ✅ 数据库会话已关闭")
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("详细堆栈跟踪:")
    traceback.print_exc()
    
except Exception as e:
    print(f"❌ 测试过程中发生错误: {e}")
    print("详细堆栈跟踪:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成！")