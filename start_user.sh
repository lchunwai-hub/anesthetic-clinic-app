#!/bin/bash

# 麻醉診所管理系統 - 啟動用戶介面
# 用途: 快速啟動用戶查看介面

echo "🚀 啟動麻醉診所用戶介面..."
echo "================================"

# 檢查端口 8501 是否被佔用
PORT=8501
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 $PORT 已被佔用，正在清理..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 啟動用戶介面
echo "✅ 在端口 $PORT 啟動用戶介面..."
echo ""
echo "📱 訪問地址:"
echo "   本地: http://localhost:$PORT"
echo "   網路: http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "ℹ️  用戶可以瀏覽產品目錄和價格"
echo ""
echo "按 Ctrl+C 停止服務"
echo "================================"
echo ""

# 啟動 Streamlit
streamlit run user_app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
