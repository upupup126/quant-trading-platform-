#!/bin/bash

# 量化交易平台停止脚本
# 使用方法：./scripts/stop.sh [模式]
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
    echo "量化交易平台停止脚本"
    echo ""
    echo "用法：$0 [模式] [选项]"
    echo ""
    echo "模式："
    echo "  dev     停止开发模式服务"
    echo "  docker 停止容器模式服务"
    echo "  all     停止所有服务"
    echo ""
    echo "选项："
    echo "  -h, --help    显示帮助信息"
    echo "  -f, --force   强制停止（不等待优雅关闭）"
    echo "  -c, --clean   停止后清理环境"
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
    MODE="all"
    log_info "使用默认模式: $MODE"
fi

# 停止开发模式服务
stop_dev_services() {
    log_info "停止开发模式服务..."
    
    # 停止前端服务
    if [[ -f ".frontend.pid" ]]; then
        FRONTEND_PID=$(cat .frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            log_info "停止前端服务 (PID: $FRONTEND_PID)..."
            if [[ "$FORCE" == true ]]; then
                kill -9 $FRONTEND_PID
            else
                kill $FRONTEND_PID
            fi
            sleep 2
            if ! kill -0 $FRONTEND_PID 2>/dev/null; then
                log_success "前端服务已停止"
                rm -f .frontend.pid
            else
                log_warning "前端服务停止失败，尝试强制停止..."
                kill -9 $FRONTEND_PID
                rm -f .frontend.pid
            fi
        else
            log_warning "前端服务进程不存在，清理PID文件"
            rm -f .frontend.pid
        fi
    else
        log_info "前端服务未运行"
    fi
    
    # 停止后端服务
    if [[ -f ".backend.pid" ]]; then
        BACKEND_PID=$(cat .backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            log_info "停止后端服务 (PID: $BACKEND_PID)..."
            if [[ "$FORCE" == true ]]; then
                kill -9 $BACKEND_PID
            else
                kill $BACKEND_PID
            fi
            sleep 3
            if ! kill -0 $BACKEND_PID 2>/dev/null; then
                log_success "后端服务已停止"
                rm -f .backend.pid
            else
                log_warning "后端服务停止失败，尝试强制停止..."
                kill -9 $BACKEND_PID
                rm -f .backend.pid
            fi
        else
            log_warning "后端服务进程不存在，清理PID文件"
            rm -f .backend.pid
        fi
    else
        log_info "后端服务未运行"
    fi
    
    # 检查是否还有相关进程
    log_info "检查残留进程..."
    PIDS=$(pgrep -f "python main.py" || true)
    if [[ -n "$PIDS" ]]; then
        log_warning "发现残留进程: $PIDS"
        if [[ "$FORCE" == true ]]; then
            log_info "强制停止残留进程..."
            kill -9 $PIDS
        fi
    fi
    
    log_success "开发模式服务停止完成"
}

# 停止容器模式服务
stop_docker_services() {
    log_info "停止容器模式服务..."
    
    # 检查Docker是否运行
    if ! command -v docker &> /dev/null; then
        log_warning "Docker未安装，跳过容器服务停止"
        return
    fi
    
    if ! docker ps > /dev/null 2>&1; then
        log_warning "Docker服务未运行，跳过容器服务停止"
        return
    fi
    
    # 检查Docker Compose项目
    if docker-compose ps > /dev/null 2>&1; then
        log_info "停止Docker Compose服务..."
        if [[ "$FORCE" == true ]]; then
            docker-compose down --timeout 0
        else
            docker-compose down
        fi
        
        # 检查是否还有运行的容器
        RUNNING_CONTAINERS=$(docker-compose ps -q)
        if [[ -n "$RUNNING_CONTAINERS" ]]; then
            log_warning "发现运行的容器，强制停止..."
            docker-compose down --timeout 0
        fi
        
        log_success "容器服务停止完成"
    else
        log_info "Docker Compose项目未运行"
    fi
    
    # 清理未使用的容器、网络和镜像
    if [[ "$CLEAN" == true ]]; then
        log_info "清理Docker资源..."
        docker system prune -f
    fi
}

# 清理环境
clean_environment() {
    log_info "清理环境..."
    
    # 清理PID文件
    rm -f .frontend.pid .backend.pid
    
    # 清理日志文件
    if [[ "$CLEAN" == true ]]; then
        log_info "清理日志文件..."
        rm -rf logs/*
        
        # 清理前端构建文件
        if [[ -d "frontend/dist" ]]; then
            rm -rf frontend/dist
        fi
        
        # 清理Python缓存
        find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        
        log_success "环境清理完成"
    else
        log_info "跳过环境清理（使用 -c 选项启用）"
    fi
}

# 检查服务状态
check_service_status() {
    log_info "检查服务状态..."
    
    # 检查开发模式服务
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        if [[ -f ".frontend.pid" ]] && kill -0 $(cat .frontend.pid) 2>/dev/null; then
            log_warning "前端服务仍在运行"
        else
            log_success "前端服务已停止"
        fi
        
        if [[ -f ".backend.pid" ]] && kill -0 $(cat .backend.pid) 2>/dev/null; then
            log_warning "后端服务仍在运行"
        else
            log_success "后端服务已停止"
        fi
    fi
    
    # 检查容器模式服务
    if [[ "$MODE" == "docker" || "$MODE" == "all" ]]; then
        if command -v docker &> /dev/null && docker ps > /dev/null 2>&1; then
            RUNNING_CONTAINERS=$(docker-compose ps -q 2>/dev/null || true)
            if [[ -n "$RUNNING_CONTAINERS" ]]; then
                log_warning "容器服务仍在运行"
                docker-compose ps
            else
                log_success "容器服务已停止"
            fi
        fi
    fi
}

# 主函数
main() {
    log_info "停止量化交易平台 ($MODE 模式)"
    
    # 确认停止
    if [[ "$FORCE" == false ]]; then
        echo ""
        log_warning "即将停止所有服务"
        echo "停止模式：$MODE"
        echo ""
        read -p "确认停止？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "操作已取消"
            exit 0
        fi
    fi
    
    # 停止服务
    if [[ "$MODE" == "dev" || "$MODE" == "all" ]]; then
        stop_dev_services
    fi
    
    if [[ "$MODE" == "docker" || "$MODE" == "all" ]]; then
        stop_docker_services
    fi
    
    # 清理环境
    clean_environment
    
    # 检查服务状态
    check_service_status
    
    log_success "量化交易平台停止完成"
    
    echo ""
    echo "服务状态摘要："
    echo "- 开发模式服务：已停止"
    echo "- 容器模式服务：已停止"
    echo "- 环境清理：$([[ \"$CLEAN\" == true ]] && echo \"已完成\" || echo \"未执行\")"
    echo ""
    
    log_info "如需重新启动，请运行：./scripts/start.sh"
}

# 执行主函数
main "$@"