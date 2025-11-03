# ✅ CHECKLIST - Files Cần Có Khi Pull Code Về Local

## 📁 Backend Files

### 1. `/backend/.env`
```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tempmail_user
MYSQL_PASSWORD=tempmail_password_123
MYSQL_DATABASE=tempmail_db

# TempMail API Configuration
TEMPMAIL_API_URL=https://api.mail.tm
```

**Trạng thái**: ✅ Đã có
**Action**: Kiểm tra MySQL credentials có đúng không

---

### 2. `/backend/requirements.txt`
```txt
fastapi==0.115.5
uvicorn[standard]==0.32.1
python-dotenv==1.0.0
httpx==0.28.1
SQLAlchemy==2.0.23
pymysql==1.1.0
cryptography==43.0.3
```

**Trạng thái**: ✅ Đã có
**Action**: Chạy `pip install -r requirements.txt` khi setup

---

## 📁 Frontend Files

### 3. `/frontend/.env`
```env
# Backend URL cho local development
REACT_APP_BACKEND_URL=http://localhost:8001

# Visual edits (tắt cho local)
REACT_APP_ENABLE_VISUAL_EDITS=false

# Health check (tắt cho local)
ENABLE_HEALTH_CHECK=false
```

**Trạng thái**: ✅ Đã cập nhật
**Action**: ⚠️ **QUAN TRỌNG** - File này cần có khi pull về local

---

### 4. `/frontend/.env.local`
```env
# Port cho frontend khi chạy local
PORT=7050
```

**Trạng thái**: ✅ Đã có
**Action**: Đảm bảo port 7050 không bị chiếm

---

### 5. `/frontend/.env.example` (Template)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
```

**Trạng thái**: ✅ Đã tạo
**Action**: File mẫu để tham khảo

---

## 🎨 Favicon & Icons

### 6. Frontend Icons
- ✅ `/frontend/public/favicon.ico`
- ✅ `/frontend/public/logo192.png`
- ✅ `/frontend/public/logo512.png`
- ✅ `/frontend/public/mail-icon.svg`
- ✅ `/frontend/public/manifest.json`

**Trạng thái**: ✅ Tất cả đã có
**Action**: Không cần làm gì thêm

---

## 🚀 Scripts

### 7. Startup Scripts
- ✅ `/start_app.sh` - Menu chính
- ✅ `/start_backend.sh` - Chạy backend
- ✅ `/start_frontend.sh` - Chạy frontend

**Trạng thái**: ✅ Tất cả đã có
**Action**: Chạy `bash start_app.sh` để khởi động

---

## 📖 Documentation

### 8. Hướng Dẫn
- ✅ `/QUICK_START.md` - Hướng dẫn nhanh
- ✅ `/HUONG_DAN_LOCAL.md` - Chi tiết tiếng Việt
- ✅ `/SETUP_GUIDE.md` - English guide
- ✅ `/README.md` - Project overview

**Trạng thái**: ✅ Tất cả đã có

---

## 🎯 QUY TRÌNH PULL CODE VỀ LOCAL

### Bước 1: Clone/Pull Repository
```bash
# Clone lần đầu
git clone https://github.com/kha0305/temp-mail.git
cd temp-mail

# Hoặc pull nếu đã có
cd temp-mail
git pull origin main
```

### Bước 2: Kiểm Tra Files .env
```bash
# Kiểm tra backend .env
cat backend/.env

# Kiểm tra frontend .env
cat frontend/.env
cat frontend/.env.local
```

⚠️ **QUAN TRỌNG**: Nếu thiếu file nào, tạo theo mẫu bên trên!

### Bước 3: Cài Đặt MySQL
```bash
# Ubuntu/Debian
sudo apt install mysql-server
sudo systemctl start mysql

# macOS
brew install mysql
brew services start mysql

# Tạo database
sudo mysql
CREATE DATABASE tempmail_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tempmail_user'@'localhost' IDENTIFIED BY 'tempmail_password_123';
GRANT ALL PRIVILEGES ON tempmail_db.* TO 'tempmail_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Bước 4: Chạy Ứng Dụng
```bash
bash start_app.sh
```

Chọn:
1. **Lần đầu**: `1` (Init DB) → `4` (Run All)
2. **Các lần sau**: `4` (Run All)

### Bước 5: Truy Cập
- Frontend: http://localhost:7050
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

---

## 🔍 TROUBLESHOOTING

### Lỗi: "REACT_APP_BACKEND_URL not defined"
**Nguyên nhân**: Thiếu file `/frontend/.env`

**Giải pháp**:
```bash
cd frontend
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
EOF
```

### Lỗi: "Frontend không chạy port 7050"
**Nguyên nhân**: Thiếu file `/frontend/.env.local`

**Giải pháp**:
```bash
cd frontend
echo "PORT=7050" > .env.local
```

### Lỗi: "Can't connect to backend"
**Kiểm tra**:
1. Backend có đang chạy không? `curl http://localhost:8001/health`
2. File `.env` có đúng URL không?
3. Port 8001 có bị chiếm không? `lsof -i:8001`

---

## 📋 SUMMARY

**Files BẮT BUỘC cần có khi chạy local:**

Backend:
- ✅ `backend/.env` (MySQL config)
- ✅ `backend/requirements.txt`

Frontend:
- ✅ `frontend/.env` (Backend URL = http://localhost:8001)
- ✅ `frontend/.env.local` (PORT=7050)

Icons:
- ✅ `frontend/public/favicon.ico`
- ✅ `frontend/public/logo192.png`
- ✅ `frontend/public/logo512.png`
- ✅ `frontend/public/manifest.json`

Scripts:
- ✅ `start_app.sh`
- ✅ `start_backend.sh`
- ✅ `start_frontend.sh`

---

Nếu thiếu file nào, tạo theo template bên trên hoặc copy từ `.env.example`! 🎯
