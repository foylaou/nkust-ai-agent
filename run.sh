#!/bin/bash
# 啟動 ADK Multi-Agent Web Server
# 用法: ./run.sh [--debug]

set -e

# 切到 src 目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/src"

# 啟動虛擬環境
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
fi

# 解析參數
DEBUG_MODE=0
for arg in "$@"; do
    case $arg in
        --debug) DEBUG_MODE=1 ;;
    esac
done

export DEBUG_MODE=$DEBUG_MODE

echo "🚀 啟動 NKUST Multi-Agent"
echo "   DEBUG_MODE=${DEBUG_MODE}"
echo "   MEMORY_BACKEND=$(grep MEMORY_BACKEND .env 2>/dev/null | cut -d= -f2 || echo 'inmemory')"
echo ""

adk web muilt-agents --memory_service_uri="unified://"
