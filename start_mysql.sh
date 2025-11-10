#!/bin/bash

# Script tự động chạy TempMail App với MySQL
# Sử dụng: bash start_mysql.sh

echo "🚀 STARTING TEMPMAIL APP (MySQL Version)..."
echo ""

# Màu sắc cho terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kiểm tra MySQL
echo "🗄️  Checking MySQL..."
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL chưa cài đặt!${NC}"
    echo "Vui lòng cài MySQL: https://dev.mysql.com/downloads/mysql/"
    exit 1
fi

echo -e "${GREEN}✅ MySQL $(mysql --version | awk '{print $5}' | cut -d',' -f1)${NC}"

# Kiểm tra MySQL đang chạy
echo "🔍 Checking MySQL service..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! brew services list | grep mysql | grep started > /dev/null; then
        echo -e "${YELLOW}⚠️  MySQL chưa chạy. Đang khởi động...${NC}"
        brew services start mysql
        sleep 3
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if ! sudo systemctl is-active --quiet mysql; then
        echo -e "${YELLOW}⚠️  MySQL chưa chạy. Đang khởi động...${NC}"
        sudo systemctl start mysql
        sleep 3
    fi
else
    echo -e "${YELLOW}⚠️  Không thể tự động kiểm tra MySQL. Vui lòng đảm bảo MySQL đang chạy!${NC}"
fi

echo -e "${GREEN}✅ MySQL service đang chạy${NC}"

# Test MySQL connection
echo "🔐 Testing MySQL connection..."
if mysql -u root -p190705 -e "SELECT 1" &>/dev/null; then
    echo -e "${GREEN}✅ MySQL connection successful (root/190705)${NC}"
else
    echo -e "${RED}❌ Không thể kết nối MySQL với credentials mặc định!${NC}"
    echo -e "${YELLOW}Vui lòng kiểm tra:${NC}"
    echo "  1. MySQL root password có đúng là '190705' không?"
    echo "  2. Sửa file backend/.env nếu password khác"
    echo "  3. Test kết nối: mysql -u root -p"
    exit 1
fi

# Kiểm tra database temp_mail
echo "📊 Checking database 'temp_mail'..."
if mysql -u root -p190705 -e "USE temp_mail" &>/dev/null; then
    echo -e "${GREEN}✅ Database 'temp_mail' exists${NC}"
else
    echo -e "${YELLOW}⚠️  Database chưa tồn tại. Đang tạo...${NC}"
    mysql -u root -p190705 -e "CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo -e "${GREEN}✅ Database 'temp_mail' created${NC}"
fi
echo ""

# Kiểm tra Python
echo "🐍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 chưa cài đặt!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version)${NC}"
echo ""

# Kiểm tra Node.js và Yarn
echo "📦 Checking Node.js and Yarn..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js chưa cài đặt!${NC}"
    exit 1
fi

if ! command -v yarn &> /dev/null; then
    echo -e "${YELLOW}⚠️  Yarn chưa cài. Đang cài đặt...${NC}"
    npm install -g yarn
fi
echo -e "${GREEN}✅ Node $(node --version), Yarn $(yarn --version)${NC}"
echo ""

# Function để cleanup khi thoát
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Đang dừng ứng dụng...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Đã dừng!${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# ============================================
# BACKEND
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔧 STARTING BACKEND (MySQL)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
cd backend

# Tạo virtual environment nếu chưa có
if [ ! -d "venv" ]; then
    echo "Tạo Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Cài đặt dependencies
echo "Cài đặt Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Khởi tạo database tables
echo "Khởi tạo database tables..."
python init_db.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Lỗi khởi tạo database!${NC}"
    exit 1
fi

# Khởi động backend
echo "Khởi động FastAPI server..."
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!

# Đợi backend khởi động
sleep 5

# Kiểm tra backend
if curl -s http://localhost:8001 > /dev/null; then
    echo -e "${GREEN}✅ Backend đang chạy tại http://localhost:8001${NC}"
else
    echo -e "${RED}❌ Backend không khởi động được. Kiểm tra backend.log${NC}"
    tail -20 ../backend.log
    exit 1
fi

cd ..
echo ""

# ============================================
# FRONTEND
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎨 STARTING FRONTEND${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
cd frontend

# Cài đặt dependencies
echo "Cài đặt Node dependencies..."
yarn install --silent

# Khởi động frontend
echo "Khởi động React app..."
yarn start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Đợi frontend compile
echo "Đang compile React app..."
sleep 15

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ ỨNG DỤNG ĐÃ CHẠY THÀNH CÔNG!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📱 Frontend:  http://localhost:3000${NC}"
echo -e "${BLUE}🔧 Backend:   http://localhost:8001${NC}"
echo -e "${BLUE}📚 API Docs:  http://localhost:8001/docs${NC}"
echo -e "${BLUE}🗄️  Database:  MySQL (temp_mail)${NC}"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "  - Xem backend logs: tail -f backend.log"
echo "  - Xem frontend logs: tail -f frontend.log"
echo "  - Quản lý DB: mysql -u root -p190705 temp_mail"
echo ""
echo -e "${YELLOW}⚠️  Nhấn Ctrl+C để dừng ứng dụng${NC}"
echo ""

# Mở trình duyệt (optional)
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000
fi

# Đợi vô hạn (cho đến khi Ctrl+C)
wait
