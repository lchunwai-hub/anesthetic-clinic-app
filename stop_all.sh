#!/bin/bash

# 麻醉診所管理系統 - 停止所有服務
# 用途: 停止所有運行中的應用程式

echo "🛑 停止麻醉診所系統..."
echo "================================"

# 停止端口 8501 (用戶介面)
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⏹️  停止用戶介面 (端口 8501)..."
    lsof -ti:8501 | xargs kill -9 2>/dev/null
    echo "   ✅ 已停止"
else
    echo "   ℹ️  用戶介面未運行"
fi

# 停止端口 8502 (管理介面)
if lsof -Pi :8502 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⏹️  停止管理介面 (端口 8502)..."
    lsof -ti:8502 | xargs kill -9 2>/dev/null
    echo "   ✅ 已停止"
else
    echo "   ℹ️  管理介面未運行"
fi

echo ""
echo "================================"
echo "✅ 所有服務已停止"
echo "================================"
