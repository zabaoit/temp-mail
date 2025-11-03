# 🚀 Hướng Dẫn Cài Đặt và Chạy TempMail Application (Local)

## 📋 Yêu Cầu Hệ Thống

Trước khi bắt đầu, đảm bảo máy của bạn đã cài đặt:

### 1. Python 3.11 hoặc cao hơn
```bash
# Kiểm tra version
python3 --version

# Cài đặt (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Cài đặt (macOS)
brew install python@3.11

# Cài đặt (Windows)
# Download từ https://www.python.org/downloads/
```

### 2. Node.js 16+ và Yarn
```bash
# Kiểm tra version
node --version
yarn --version

# Cài đặt Node.js (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Cài đặt Yarn
npm install -g yarn

# Cài đặt (macOS)
brew install node
brew install yarn

# Cài đặt (Windows)
# Download từ https://nodejs.org/
```

### 3. MySQL 8.0+
```bash
# Kiểm tra MySQL đã cài đặt chưa
mysql --version

# Cài đặt (Ubuntu/Debian)
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Cài đặt (macOS)
brew install mysql
brew services start mysql

# Cài đặt (Windows)
# Download từ https://dev.mysql.com/downloads/installer/
```

### 4. Cấu hình MySQL
```bash
# Đăng nhập MySQL
mysql -u root -p

# Tạo user và database (nếu cần)
CREATE DATABASE garena_creator_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON garena_creator_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 🔧 Cài Đặt

### Bước 1: Cấu hình Backend

1. Mở file `/app/backend/.env` và kiểm tra thông tin MySQL:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=garena_creator_db
CORS_ORIGINS=*
```

2. Điều chỉnh thông tin nếu cần (đặc biệt là `DB_PASSWORD`)

### Bước 2: Cấu hình Frontend

1. File `/app/frontend/.env` đã được cấu hình sẵn:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=443
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
```

### Bước 3: Khởi tạo Database

```bash
cd /app
bash start_app.sh
# Chọn option 4 để khởi tạo database
```

Hoặc chạy trực tiếp:
```bash
cd /app/backend
python3 init_db.py
```

---

## 🚀 Chạy Ứng Dụng

### Cách 1: Chạy tự động (Khuyến nghị)

```bash
cd /app
bash start_app.sh
```

Chọn option:
- **Option 1**: Chạy Backend only (http://localhost:8001)
- **Option 2**: Chạy Frontend only (http://localhost:3000)
- **Option 3**: Chạy cả Backend và Frontend
- **Option 4**: Khởi tạo Database

### Cách 2: Chạy thủ công

#### Chạy Backend (Terminal 1)
```bash
cd /app/backend

# Tạo virtual environment (lần đầu)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi tạo database (lần đầu)
python3 init_db.py

# Chạy server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Chạy Frontend (Terminal 2)
```bash
cd /app/frontend

# Cài đặt dependencies (lần đầu)
yarn install

# Chạy frontend
yarn start
```

---

## 🌐 Truy Cập Ứng Dụng

Sau khi khởi động thành công:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Alternative API Docs**: http://localhost:8001/redoc

---

## 🧪 Kiểm Tra

### 1. Kiểm tra Backend
```bash
# Test API endpoint
curl http://localhost:8001/api/

# Kết quả mong đợi: {"message":"TempMail API"}
```

### 2. Kiểm tra Database
```bash
mysql -u root -p

USE garena_creator_db;
SHOW TABLES;
# Nên thấy: temp_emails

DESCRIBE temp_emails;
EXIT;
```

### 3. Kiểm tra Frontend
Mở trình duyệt: http://localhost:3000

---

## 📚 Tính Năng Chính

1. **Tạo Email Tạm Thời**: Tạo địa chỉ email tạm thời qua Mail.tm
2. **Nhận Tin Nhắn**: Nhận và đọc email gửi đến
3. **Quản Lý Email**: Xem danh sách, chi tiết, và xóa email
4. **Tự Động Refresh**: Cập nhật tin nhắn mới

---

## 🛠️ Troubleshooting

### Lỗi: Cannot connect to MySQL
**Nguyên nhân**: MySQL chưa chạy hoặc thông tin đăng nhập sai

**Giải pháp**:
```bash
# Kiểm tra MySQL đang chạy
sudo systemctl status mysql  # Linux
brew services list  # macOS

# Khởi động MySQL
sudo systemctl start mysql  # Linux
brew services start mysql  # macOS

# Test kết nối
mysql -u root -p -h localhost
```

### Lỗi: Port already in use
**Nguyên nhân**: Cổng 8001 hoặc 7050 đã được sử dụng

**Giải pháp**:
```bash
# Tìm process đang dùng port
lsof -i :8001
lsof -i :7050

# Kill process
kill -9 <PID>
```

### Lỗi: Module not found
**Nguyên nhân**: Dependencies chưa được cài đặt

**Giải pháp**:
```bash
# Backend
cd /app/backend
pip install -r requirements.txt

# Frontend
cd /app/frontend
yarn install
```

### Lỗi: CORS issues
**Nguyên nhân**: Frontend không thể gọi Backend API

**Giải pháp**: Kiểm tra `REACT_APP_BACKEND_URL` trong `/app/frontend/.env` phải là `http://localhost:8001`

---

## 🔄 Cập Nhật và Bảo Trì

### Xóa dữ liệu cũ
```bash
mysql -u root -p

USE garena_creator_db;
TRUNCATE TABLE temp_emails;
EXIT;
```

### Backup Database
```bash
mysqldump -u root -p garena_creator_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p garena_creator_db < backup.sql
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong terminal
2. Đảm bảo tất cả services (MySQL, Backend, Frontend) đang chạy
3. Kiểm tra cấu hình trong file `.env`
4. Xem lại phần Troubleshooting ở trên

---

## 📝 Ghi Chú

- Ứng dụng sử dụng Mail.tm API để tạo email tạm thời
- Database lưu trữ thông tin email và token xác thực
- Backend chạy FastAPI với SQLAlchemy ORM
- Frontend được xây dựng với React

---

**Happy Coding! 🎉**