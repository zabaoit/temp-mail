# 🚀 HƯỚNG DẪN CHẠY TEMPMAIL TRÊN MÁY LOCAL

## 📋 YÊU CẦU HỆ THỐNG

### 1. Cài đặt MySQL
- **MySQL 8.0+** hoặc **MariaDB 10.5+**
- Username: `root`
- Password: `190705`
- Port: `3306`

### 2. Cài đặt Python
- **Python 3.9+**
- pip (Python package manager)

### 3. Cài đặt Node.js và Yarn
- **Node.js 18+**
- **Yarn** package manager

---

## 📥 BƯỚC 1: TẢI CODE VỀ MÁY

Nếu code đang ở container, bạn cần tải về máy local:

```bash
# Tải về từ GitHub hoặc copy folder /app về máy local
# Giả sử bạn đã có folder /app trên máy
cd /app
```

---

## 🗄️ BƯỚC 2: SETUP MYSQL

### 2.1. Khởi động MySQL
```bash
# Kiểm tra MySQL đang chạy
sudo systemctl status mysql

# Nếu chưa chạy, khởi động MySQL
sudo systemctl start mysql
```

### 2.2. Tạo Database
```bash
# Đăng nhập MySQL
mysql -u root -p190705

# Tạo database (nếu chưa có)
CREATE DATABASE IF NOT EXISTS temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Thoát MySQL
exit;
```

### 2.3. Khởi tạo Tables
```bash
cd /app/backend
python init_db.py
```

**Output mong đợi:**
```
✅ Kết nối database thành công!
✅ Tất cả tables đã được tạo thành công!
```

---

## 🔧 BƯỚC 3: SETUP BACKEND

### 3.1. Tạo Virtual Environment
```bash
cd /app/backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3.2. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3.3. Kiểm tra file .env
Đảm bảo `/app/backend/.env` có nội dung:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

### 3.4. Chạy Backend Server
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Output mong đợi:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Started server process
INFO:     Waiting for application startup.
✅ Database connected successfully
🔄 Background tasks started
INFO:     Application startup complete.
```

**Kiểm tra:**
- Mở trình duyệt: http://localhost:8001/docs
- Bạn sẽ thấy Swagger API documentation

---

## 💻 BƯỚC 4: SETUP FRONTEND

Mở terminal mới (giữ backend đang chạy):

### 4.1. Cài đặt Dependencies
```bash
cd /app/frontend
yarn install
```

### 4.2. Kiểm tra file .env
Đảm bảo `/app/frontend/.env` có nội dung:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=7050
```

### 4.3. Chạy Frontend
```bash
PORT=7050 yarn start
```

**Output mong đợi:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:7050
  On Your Network:  http://192.168.x.x:7050
```

---

## 🎉 BƯỚC 5: SỬ DỤNG ỨNG DỤNG

### 5.1. Mở Trình duyệt
```
http://localhost:7050
```

### 5.2. Tính năng tự động
✅ **Email tự động tạo khi vào trang lần đầu**
- Không cần click nút "Tạo Email Mới"
- App sẽ tự động tạo email ngay khi load

✅ **Timer đếm ngược 10 phút**
- Email sẽ tự động hết hạn sau 10 phút
- Hiển thị: "9:59, 9:58, 9:57..."

✅ **Tự động tạo email mới khi hết hạn**
- Khi timer về 0:00
- Email cũ chuyển vào "Lịch sử"
- Email mới tự động được tạo
- Timer reset về 10:00

✅ **Nút "Làm mới 10 phút"**
- Click để reset timer về 10 phút
- **KHÔNG cộng dồn** (ví dụ: 3 phút còn lại → click → 10 phút mới)

---

## 🔍 KIỂM TRA LỖI

### Backend không khởi động
```bash
# Kiểm tra MySQL
mysql -u root -p190705 -e "SHOW DATABASES;"

# Kiểm tra port 8001 có bị chiếm không
lsof -i :8001

# Xem log backend
tail -f /app/backend/logs/app.log
```

### Frontend không kết nối được backend
```bash
# Test backend API
curl http://localhost:8001/api/emails

# Kiểm tra .env
cat /app/frontend/.env

# Clear cache và rebuild
cd /app/frontend
rm -rf node_modules/.cache
yarn start
```

### Không tạo được email
Kiểm tra console log trong trình duyệt (F12):
- Nếu thấy "CORS error" → Kiểm tra backend CORS_ORIGINS
- Nếu thấy "404" → Kiểm tra backend có chạy không
- Nếu thấy "All providers failed" → Email providers có thể bị rate limit

---

## 📊 DATABASE SCHEMA

### Table: temp_emails
```sql
CREATE TABLE temp_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT,
    account_id VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    message_count INT DEFAULT 0,
    provider VARCHAR(50),
    username VARCHAR(100),
    domain VARCHAR(100)
);
```

### Table: email_history
```sql
CREATE TABLE email_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    token TEXT,
    account_id VARCHAR(255),
    created_at DATETIME,
    expired_at DATETIME,
    message_count INT DEFAULT 0
);
```

### Table: saved_emails
```sql
CREATE TABLE saved_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_id INT,
    message_id VARCHAR(255),
    subject VARCHAR(500),
    from_address VARCHAR(255),
    html TEXT,
    text TEXT,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 CÁC TÍNH NĂNG CHÍNH

### 1. Tạo Email Tự Động
- Khi vào trang lần đầu → tự động tạo email
- Khi hết 10 phút → tự động tạo email mới
- Không cần click nút

### 2. Multi-Provider Support
- **Mail.tm** - Provider chính
- **Mail.gw** - Dự phòng
- **Guerrilla Mail** - Dự phòng
- Auto-failover: Nếu provider này fail → thử provider khác

### 3. Timer 10 Phút
- Đếm ngược thời gian thực
- Tính từ `expires_at` trong database
- Reset về 10:00 mỗi khi làm mới

### 4. Lịch Sử Email
- Tab "Lịch sử": Xem email đã hết hạn
- Chọn email để xóa (checkbox)
- Xóa tất cả hoặc xóa đã chọn

### 5. Lưu Email
- Nút "Lưu" khi xem chi tiết email
- Tab "Mail đã lưu": Xem email đã save
- Xóa mail đã lưu

---

## 🔥 TIPS QUAN TRỌNG

### Auto-Create Email
- **Lần đầu vào trang**: Tự động tạo email
- **Sau 10 phút**: Email cũ → lịch sử, tự động tạo email mới
- **Click "Tạo Email Mới"**: Tạo thêm email mới (có thể có nhiều email cùng lúc)

### Timer Reset
- **Nút "Làm mới 10 phút"**: Reset về 10:00 (KHÔNG cộng dồn)
- Ví dụ: 
  - Timer còn 3:25
  - Click "Làm mới"
  - Timer = 10:00 (không phải 13:25)

### Background Task
Backend tự động chạy task mỗi 30 giây để:
- Kiểm tra email hết hạn
- Chuyển email hết hạn vào lịch sử
- Tạo email mới nếu không còn email active

---

## 📞 HỖ TRỢ

### Vấn đề thường gặp

**1. "Can't connect to MySQL server"**
```bash
sudo systemctl start mysql
mysql -u root -p190705 -e "SELECT 1;"
```

**2. "ModuleNotFoundError: No module named 'xxx'"**
```bash
cd /app/backend
source venv/bin/activate
pip install -r requirements.txt
```

**3. "yarn: command not found"**
```bash
npm install -g yarn
```

**4. "Port 8001 already in use"**
```bash
lsof -i :8001
kill -9 <PID>
```

**5. "Không tạo được email"**
- Kiểm tra backend logs
- Các email provider có thể bị rate limit
- Thử lại sau vài phút

---

## 🚀 CHẠY NHANH (TÓM TẮT)

```bash
# Terminal 1 - Backend
cd /app/backend
source venv/bin/activate
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend
cd /app/frontend
PORT=7050 yarn start

# Mở trình duyệt
# http://localhost:7050
```

---

## ✅ CHECKLIST

Trước khi chạy, đảm bảo:

- [ ] MySQL đã cài và đang chạy
- [ ] Database `temp_mail` đã được tạo
- [ ] Tables đã được tạo (chạy init_db.py)
- [ ] Python 3.9+ đã cài
- [ ] Node.js 18+ và Yarn đã cài
- [ ] Backend .env đúng config MySQL
- [ ] Frontend .env có REACT_APP_BACKEND_URL=http://localhost:8001
- [ ] Port 8001 và 7050 chưa bị chiếm
- [ ] Virtual environment đã activate

---

**🎊 Chúc bạn sử dụng thành công!**
