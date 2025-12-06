#!/bin/bash

# 量化交易平台部署脚本
# 使用方法：./scripts/deploy.sh [环境]
# 环境：dev（开发环境）| prod（生产环境）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 帮助信息
show_help() {
    echo "量化交易平台部署脚本"
    echo ""
    echo "用法：$0 [环境] [选项]"
    echo ""
    echo "环境："
    echo "  dev     开发环境部署"
    echo "  prod    生产环境部署"
    echo ""
    echo "选项："
    echo "  -h, --help    显示帮助信息"
    echo "  -b, --build   重新构建镜像"
    echo "  -f, --force   强制部署（跳过确认）"
    echo ""
}

# 参数解析
ENVIRONMENT=""
BUILD=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        dev|prod)
            ENVIRONMENT="$1"
            shift
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查环境参数
if [[ -z "$ENVIRONMENT" ]]; then
    log_error "请指定部署环境 (dev 或 prod)"
    show_help
    exit 1
fi

# 检查Docker和Docker Compose
check_dependencies() {
    log_info "检查依赖环境..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    log_success "依赖环境检查通过"
}

# 环境配置
setup_environment() {
    log_info "设置环境配置..."
    
    if [[ "$ENVIRONMENT" == "prod" ]]; then
        export COMPOSE_PROJECT_NAME="quant-trading-prod"
        export COMPOSE_FILE="docker-compose.yml:docker-compose.prod.yml"
    else
        export COMPOSE_PROJECT_NAME="quant-trading-dev"
        export COMPOSE_FILE="docker-compose.yml:docker-compose.dev.yml"
    fi
    
    # 创建环境文件
    if [[ ! -f ".env" ]]; then
        cp ".env.example" ".env"
        log_warning "已创建.env文件，请根据实际情况修改配置"
    fi
    
    log_success "环境配置完成"
}

# 构建镜像
build_images() {
    if [[ "$BUILD" == true ]]; then
        log_info "开始构建Docker镜像..."
        
        # 构建前端镜像
        log_info "构建前端镜像..."
        docker-compose build frontend
        
        # 构建后端镜像
        log_info "构建后端镜像..."
        docker-compose build backend
        
        log_success "镜像构建完成"
    else
        log_info "跳过镜像构建，使用现有镜像"
    fi
}

# 数据库初始化
init_database() {
    log_info "初始化数据库..."
    
    # 等待数据库启动
    log_info "等待数据库服务启动..."
    sleep 10
    
    # 运行数据库迁移
    log_info "执行数据库迁移..."
    docker-compose exec backend python -c "from app.core.database import create_tables; create_tables()" || {
        log_warning "数据库迁移执行失败，尝试重新创建表结构"
        docker-compose exec backend python -c "from app.core.database import drop_tables, create_tables; drop_tables(); create_tables()"
    }
    
    # 导入初始数据
    log_info "导入初始数据..."
    if [[ -f "./scripts/init_data.sql" ]]; then
        docker-compose exec db psql -U quant_user -d quant_trading -f /docker-entrypoint-initdb.d/init_data.sql
    fi
    
    log_success "数据库初始化完成"
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    # 启动所有服务
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    log_info "检查服务状态..."
    docker-compose ps
    
    log_success "服务启动完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查后端API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "后端API服务正常"
    else
        log_error "后端API服务异常"
        return 1
    fi
    
    # 检查前端服务
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_success "前端服务正常"
    else
        log_error "前端服务异常"
        return 1
    fi
    
    # 检查数据库连接
    if docker-compose exec db pg_isready -U quant_user -d quant_trading > /dev/null 2>&1; then
        log_success "数据库连接正常"
    else
        log_error "数据库连接异常"
        return 1
    fi
    
    log_success "所有服务健康检查通过"
}

# 部署确认
confirm_deployment() {
    if [[ "$FORCE" == false ]]; then
        echo ""
        log_warning "即将部署到 $ENVIRONMENT 环境"
        echo "部署内容："
        echo "- 前端服务 (端口: 3000)"
        echo "- 后端API服务 (端口: 8000)"
        echo "- 数据库服务 (端口: 5432)"
        echo "- Redis缓存服务 (端口: 6379)"
        echo ""
        read -p "确认部署？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "部署已取消"
            exit 0
        fi
    fi
}

# 主函数
main() {
    log_info "开始部署量化交易平台 ($ENVIRONMENT 环境)"
    
    # 确认部署
    confirm_deployment
    
    # 检查依赖
    check_dependencies
    
    # 设置环境
    setup_environment
    
    # 停止现有服务
    log_info "停止现有服务..."
    docker-compose down
    
    # 构建镜像
    build_images
    
    # 启动服务
    start_services
    
    # 初始化数据库
    init_database
    
    # 健康检查
    health_check
    
    # 显示部署结果
    echo ""
    log_success "量化交易平台部署完成！"
    echo ""
    echo "访问地址："
    echo "- 前端应用：http://localhost:3000"
    echo "- API文档：http://localhost:8000/docs"
    echo ""
    echo "服务状态："
    docker-compose ps
    echo ""
    log_info "使用 'docker-compose logs [服务名]' 查看服务日志"
    log_info "使用 'docker-compose down' 停止所有服务"
}

# 执行主函数
main "$@"