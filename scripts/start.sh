#!/bin/bash

# 量化交易平台启动脚本
# 使用方法：./scripts/start.sh [模式]
# 模式：dev（开发模式）| docker（容器模式）| all（全部模式）

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
    echo "量化交易平台启动脚本"
    echo ""
    echo "用法：$0 [模式] [选项]"
    echo ""
    echo "模式："
    echo "  dev     开发模式（前端和后端分别启动）"
    echo "  docker 容器模式（使用Docker Compose）"
    echo "  all     全部模式（开发模式+容器模式）"
    echo ""
    echo "选项："
    echo "  -h, --help    显示帮助信息"
    echo "  -f, --force   强制启动（跳过检查）"
    echo "  -c, --clean   清理环境后启动"
    echo ""
}

# 参数解析
MODE=""
FORCE=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        dev|docker|all)
            MODE="$1"
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
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

# 默认模式
if [[ -z "$MODE" ]]; then
    MODE="dev"
    log_info "使用默认模式: $MODE"
fi

# 检查依赖
check_dependencies() {
    log_info "检查依赖环境..."
    
    if [[ "$MODE" == "docker" || "$MODE" == "all" ]]; then
        if ! command -v docker &> /dev/null; then
            log_error "Docker未安装，请先安装Docker"
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            log_error "Docker Compose未安装，请先安装Docker Compose"
            exit 1
        fi
    fi
    
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        if ! command -v node &> /dev/null; then
            log_error "Node.js未安装，请先安装Node.js"
            exit 1
        fi
        
        if ! command -v npm &> /dev/null; then
            log_error "npm未安装，请先安装npm"
            exit 1
        fi
        
        if ! command -v python3 &> /dev/null; then
            log_error "Python3未安装，请先安装Python3"
            exit 1
        fi
        
        if ! command -v pip3 &> /dev/null; then
            log_error "pip3未安装，请先安装pip3"
            exit 1
        fi
    fi
    
    log_success "依赖环境检查通过"
}

# 清理环境
clean_environment() {
    log_info "清理环境..."
    
    # 停止Docker服务
    if docker-compose ps > /dev/null 2>&1; then
        log_info "停止Docker服务..."
        docker-compose down
    fi
    
    # 清理前端依赖
    if [[ -d "frontend/node_modules" ]]; then
        log_info "清理前端依赖..."
        rm -rf frontend/node_modules
    fi
    
    # 清理Python虚拟环境
    if [[ -d "backend/venv" ]]; then
        log_info "清理Python虚拟环境..."
        rm -rf backend/venv
    fi
    
    # 清理缓存文件
    log_info "清理缓存文件..."
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
    
    log_success "环境清理完成"
}

# 安装前端依赖
install_frontend_deps() {
    log_info "安装前端依赖..."
    
    cd frontend
    
    if [[ ! -d "node_modules" || "$CLEAN" == true ]]; then
        log_info "执行 npm install..."
        npm install
    else
        log_info "前端依赖已存在，跳过安装"
    fi
    
    cd ..
    
    log_success "前端依赖安装完成"
}

# 安装后端依赖
install_backend_deps() {
    log_info "安装后端依赖..."
    
    cd backend
    
    if [[ ! -d "venv" || "$CLEAN" == true ]]; then
        log_info "创建Python虚拟环境..."
        python3 -m venv venv
        
        log_info "激活虚拟环境并安装依赖..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        log_info "后端依赖已存在，跳过安装"
        source venv/bin/activate
    fi
    
    cd ..
    
    log_success "后端依赖安装完成"
}

# 启动开发模式
start_dev_mode() {
    log_info "启动开发模式..."
    
    # 启动后端服务
    log_info "启动后端API服务..."
    cd backend
    source venv/bin/activate
    nohup python main.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # 等待后端启动
    log_info "等待后端服务启动..."
    sleep 5
    
    # 启动前端服务
    log_info "启动前端开发服务器..."
    cd frontend
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # 保存进程ID
    echo $BACKEND_PID > .backend.pid
    echo $FRONTEND_PID > .frontend.pid
    
    log_success "开发模式启动完成"
}

# 启动容器模式
start_docker_mode() {
    log_info "启动容器模式..."
    
    # 检查Docker服务
    if ! docker ps > /dev/null 2>&1; then
        log_error "Docker服务未启动，请先启动Docker"
        exit 1
    fi
    
    # 启动Docker服务
    log_info "启动Docker Compose服务..."
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    log_success "容器模式启动完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查后端API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "后端API服务正常"
    else
        log_warning "后端API服务异常"
        return 1
    fi
    
    # 检查前端服务
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_success "前端服务正常"
    else
        log_warning "前端服务异常"
        return 1
    fi
    
    log_success "健康检查完成"
}

# 显示服务信息
show_service_info() {
    echo ""
    log_success "量化交易平台启动完成！"
    echo ""
    
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        echo "开发模式服务信息："
        echo "- 前端开发服务器：http://localhost:3000"
        echo "- 后端API服务：http://localhost:8000"
        echo "- API文档：http://localhost:8000/docs"
        echo ""
        echo "日志文件："
        echo "- 后端日志：logs/backend.log"
        echo "- 前端日志：logs/frontend.log"
        echo ""
        echo "停止服务：./scripts/stop.sh"
    fi
    
    if [[ "$MODE" == "docker" || "$MODE" == "all" ]]; then
        echo "容器模式服务信息："
        echo "- 前端应用：http://localhost:3000"
        echo "- 后端API：http://localhost:8000"
        echo "- 数据库：localhost:5432"
        echo "- Redis缓存：localhost:6379"
        echo ""
        echo "管理命令："
        echo "- 查看服务状态：docker-compose ps"
        echo "- 查看服务日志：docker-compose logs [服务名]"
        echo "- 停止服务：docker-compose down"
    fi
    
    echo ""
}

# 主函数
main() {
    log_info "启动量化交易平台 ($MODE 模式)"
    
    # 创建日志目录
    mkdir -p logs
    
    # 检查依赖
    check_dependencies
    
    # 清理环境
    if [[ "$CLEAN" == true ]]; then
        clean_environment
    fi
    
    # 安装依赖
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        install_frontend_deps
        install_backend_deps
    fi
    
    # 启动服务
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        start_dev_mode
    fi
    
    if [[ "$MODE" == "docker" || "$MODE" == "all" ]]; then
        start_docker_mode
    fi
    
    # 健康检查
    if [[ "$FORCE" == false ]]; then
        health_check
    fi
    
    # 显示服务信息
    show_service_info
}

# 执行主函数
main "$@"