#!/bin/bash

# 麻醉診所管理系統 - 同時啟動兩個介面
# 用途: 一次啟動管理和用戶介面

echo "🚀 啟動麻醉診所完整系統..."
echo "================================"

# 清理端口
echo "🧹 清理端口..."
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
lsof -ti:8502 | xargs kill -9 2>/dev/null || true
sleep 2

# 獲取 IP 地址
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "✅ 正在啟動服務..."
echo ""

# 在後台啟動用戶介面
nohup streamlit run user_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    > user_app.log 2>&1 &

USER_PID=$!
sleep 3

# 在後台啟動管理介面
nohup streamlit run admin_app.py \
    --server.port=8502 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    > admin_app.log 2>&1 &

ADMIN_PID=$!
sleep 3

# 顯示信息
echo "================================"
echo "✅ 系統啟動完成！"
echo ""
echo "📱 用戶介面:"
echo "   本地: http://localhost:8501"
echo "   網路: http://${IP}:8501"
echo "   進程 ID: $USER_PID"
echo ""
echo "🔐 管理介面:"
echo "   本地: http://localhost:8502"
echo "   網路: http://${IP}:8502"
echo "   進程 ID: $ADMIN_PID"
echo ""
echo "👤 管理員登入:"
echo "   用戶名: admin"
echo "   密碼: admin123"
echo ""
echo "📋 查看日誌:"
echo "   用戶: tail -f user_app.log"
echo "   管理: tail -f admin_app.log"
echo ""
echo "🛑 停止服務: ./stop_all.sh"
echo "================================"
