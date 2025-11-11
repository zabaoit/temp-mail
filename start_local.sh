#!/bin/bash

# Script tự động khởi động TempMail trên máy local
# Sử dụng: ./start_local.sh

echo "🚀 KHỞI ĐỘNG TEMPMAIL LOCAL"
echo "============================"
echo ""

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kiểm tra MySQL
echo -e "${BLUE}[1/5]${NC} Kiểm tra MySQL..."
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL chưa được cài đặt!${NC}"
    echo "   Vui lòng cài MySQL trước: sudo apt install mysql-server"
    exit 1
fi

# Test MySQL connection
if mysql -u root -p190705 -e "SELECT 1;" &> /dev/null; then
    echo -e "${GREEN}✅ MySQL đang chạy${NC}"
else
    echo -e "${YELLOW}⚠️  Không kết nối được MySQL${NC}"
    echo "   Kiểm tra:"
    echo "   - MySQL có đang chạy không: sudo systemctl status mysql"
    echo "   - Username: root, Password: 190705"
    read -p "   Tiếp tục? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
fi

# Kiểm tra database
echo -e "${BLUE}[2/5]${NC} Kiểm tra database..."
if mysql -u root -p190705 -e "USE temp_mail;" &> /dev/null; then
    echo -e "${GREEN}✅ Database 'temp_mail' đã tồn tại${NC}"
else
    echo -e "${YELLOW}⚠️  Database 'temp_mail' chưa có, đang tạo...${NC}"
    mysql -u root -p190705 -e "CREATE DATABASE IF NOT EXISTS temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    # Khởi tạo tables
    cd backend
    python init_db.py
    cd ..
    echo -e "${GREEN}✅ Database đã được tạo${NC}"
fi

# Kiểm tra Python dependencies
echo -e "${BLUE}[3/5]${NC} Kiểm tra Backend dependencies..."
cd backend

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment chưa có, đang tạo...${NC}"
    python -m venv venv
fi

source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Backend dependencies OK${NC}"

# Kiểm tra Node.js và Yarn
echo -e "${BLUE}[4/5]${NC} Kiểm tra Frontend dependencies..."
cd ../frontend

if ! command -v yarn &> /dev/null; then
    echo -e "${RED}❌ Yarn chưa được cài đặt!${NC}"
    echo "   Cài Yarn: npm install -g yarn"
    exit 1
fi

yarn install > /dev/null 2>&1
echo -e "${GREEN}✅ Frontend dependencies OK${NC}"

cd ..

# Khởi động servers
echo -e "${BLUE}[5/5]${NC} Khởi động servers..."
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 SẴN SÀNG KHỞI ĐỘNG!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Sẽ mở 2 terminal:"
echo "  1. Backend  → http://localhost:8001"
echo "  2. Frontend → http://localhost:7050"
echo ""
echo -e "${YELLOW}Lưu ý: Giữ cả 2 terminal đang chạy!${NC}"
echo ""
read -p "Nhấn Enter để tiếp tục..."

# Khởi động backend trong terminal mới
echo -e "${BLUE}Đang khởi động Backend...${NC}"
gnome-terminal -- bash -c "
    cd $(pwd)/backend
    source venv/bin/activate
    echo '🔥 BACKEND SERVER'
    echo '================'
    echo 'URL: http://localhost:8001'
    echo 'Docs: http://localhost:8001/docs'
    echo ''
    python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
    exec bash
" 2>/dev/null || \
xterm -e "cd $(pwd)/backend && source venv/bin/activate && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload; bash" 2>/dev/null || \
konsole -e "cd $(pwd)/backend && source venv/bin/activate && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload; bash" 2>/dev/null &

sleep 3

# Khởi động frontend trong terminal mới
echo -e "${BLUE}Đang khởi động Frontend...${NC}"
gnome-terminal -- bash -c "
    cd $(pwd)/frontend
    echo '🌐 FRONTEND SERVER'
    echo '=================='
    echo 'URL: http://localhost:7050'
    echo ''
    PORT=7050 yarn start
    exec bash
" 2>/dev/null || \
xterm -e "cd $(pwd)/frontend && PORT=7050 yarn start; bash" 2>/dev/null || \
konsole -e "cd $(pwd)/frontend && PORT=7050 yarn start; bash" 2>/dev/null &

sleep 3

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ KHỞI ĐỘNG THÀNH CÔNG!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📍 URLS:"
echo "   Frontend:  http://localhost:7050"
echo "   Backend:   http://localhost:8001"
echo "   API Docs:  http://localhost:8001/docs"
echo ""
echo "🎯 TÍNH NĂNG TỰ ĐỘNG:"
echo "   ✅ Email tự động tạo khi vào trang"
echo "   ✅ Timer đếm ngược 10 phút"
echo "   ✅ Tự động tạo email mới khi hết hạn"
echo "   ✅ Email cũ tự động vào lịch sử"
echo ""
echo -e "${YELLOW}💡 Tip: Giữ cả 2 terminal đang chạy!${NC}"
echo ""

# Mở trình duyệt tự động (tùy chọn)
sleep 5
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:7050 2>/dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:7050 2>/dev/null &
fi

echo "Nhấn Ctrl+C để dừng script này (backend và frontend vẫn chạy)"
echo ""

# Giữ script chạy
while true; do
    sleep 1
done
