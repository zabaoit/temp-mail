# Hướng Dẫn Chạy TempMail với MySQL trên Local

## 🎯 Yêu cầu hệ thống

### 1. MySQL 8.0+
```bash
# Kiểm tra MySQL
mysql --version

# Nếu chưa có, cài đặt:
# Windows: https://dev.mysql.com/downloads/mysql/
# Mac: brew install mysql
# Linux: sudo apt install mysql-server
```

### 2. Python 3.9+
```bash
python --version
# hoặc
python3 --version
```

### 3. Node.js 18+ và Yarn
```bash
node --version
yarn --version

# Cài Yarn nếu chưa có:
npm install -g yarn
```

---

## 📥 Bước 1: Download Code

### Option A: Từ Emergent Platform
1. Vào project của bạn trên Emergent
2. Click "Save to GitHub" hoặc download ZIP
3. Extract vào folder trên máy local

### Option B: Clone từ GitHub
```bash
git clone <your-repo-url>
cd tempmail-app
```

---

## 🗄️ Bước 2: Cấu hình MySQL

### 2.1. Start MySQL Service
```bash
# Windows
net start MySQL80

# Mac
brew services start mysql

# Linux
sudo systemctl start mysql
```

### 2.2. Tạo Database và User
```bash
# Login vào MySQL
mysql -u root -p

# Trong MySQL prompt:
CREATE DATABASE IF NOT EXISTS temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Tạo user (optional, hoặc dùng root)
CREATE USER 'tempmail'@'localhost' IDENTIFIED BY '190705';
GRANT ALL PRIVILEGES ON temp_mail.* TO 'tempmail'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

### 2.3. Verify Database
```bash
mysql -u root -p190705 -e "SHOW DATABASES;"
# Should see 'temp_mail' in the list
```

---

## ⚙️ Bước 3: Cấu hình Environment

### 3.1. Backend .env
Tạo file `/backend/.env`:
```env
# MySQL Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail

# CORS
CORS_ORIGINS=*
```

### 3.2. Frontend .env
Tạo file `/frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=7050
```

---

## 🚀 Bước 4: Chạy Backend (Terminal 1)

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi tạo database (tạo tables)
python init_db.py

# Chạy server
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### ✅ Backend Ready
Nếu thành công, bạn sẽ thấy:
```
✅ Loaded .env file from: /path/to/backend/.env
✅ DB credentials loaded - User: root, Database: temp_mail
✅ Database 'temp_mail' is ready!
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
✅ Active providers: Mail.tm, 1secmail, Mail.gw, Guerrilla Mail
```

---

## 🎨 Bước 5: Chạy Frontend (Terminal 2)

```bash
# Mở terminal mới
cd frontend

# Cài đặt dependencies
yarn install

# Chạy development server
yarn start
# hoặc nếu muốn port 7050:
PORT=7050 yarn start
```

### ✅ Frontend Ready
Browser sẽ tự động mở: http://localhost:7050 (hoặc 3000)

---

## 🧪 Bước 6: Test Application

### 6.1. Test Backend API
```bash
# Test health check
curl http://localhost:8001/api/

# Test create email (auto mode with random selection)
curl -X POST http://localhost:8001/api/emails/create \
  -H "Content-Type: application/json" \
  -d '{"service": "auto"}'
```

### 6.2. Test Frontend
1. Mở http://localhost:7050
2. Email sẽ tự động tạo khi load trang
3. Kiểm tra random providers bằng cách tạo email nhiều lần
4. Check backend logs để xem random order:
   ```
   🎲 Random provider order: ['guerrilla', 'mailgw', 'mailtm']
   🎲 Random provider order: ['mailtm', 'mailgw', 'guerrilla']
   🎲 Random provider order: ['mailgw', 'guerrilla', 'mailtm']
   ```

---

## 🎲 Random Provider Selection

### Cách hoạt động
Khi chọn **"Tự động (Tất cả dịch vụ)"** trong dropdown:
- Hệ thống sẽ shuffle ngẫu nhiên thứ tự providers
- Mỗi lần tạo email có thứ tự khác nhau
- Active providers: **Mail.tm, Mail.gw, Guerrilla Mail** (3 providers)

### Xem Random Logs
Backend sẽ log mỗi lần create email:
```
🎲 Random provider order: ['guerrilla', 'mailgw', 'mailtm']
🔄 Trying guerrilla...
✅ Guerrilla email created: abc123@guerrillamailblock.com
```

Lần tiếp theo:
```
🎲 Random provider order: ['mailtm', 'mailgw', 'guerrilla']
🔄 Trying mailtm...
✅ Mail.tm email created: xyz789@txcct.com
```

---

## 🔧 Troubleshooting

### ❌ Lỗi: Can't connect to MySQL server
**Nguyên nhân:** MySQL service chưa chạy hoặc wrong credentials

**Giải pháp:**
```bash
# Check MySQL service
# Windows
net start MySQL80

# Mac
brew services start mysql

# Linux
sudo systemctl status mysql

# Verify credentials
mysql -u root -p190705
```

### ❌ Lỗi: Database 'temp_mail' doesn't exist
**Giải pháp:**
```bash
# Re-run init script
cd backend
python init_db.py

# Or manually create
mysql -u root -p190705 -e "CREATE DATABASE temp_mail;"
```

### ❌ Lỗi: ModuleNotFoundError: No module named 'sqlalchemy'
**Giải pháp:**
```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# Re-install dependencies
pip install -r requirements.txt
```

### ❌ Lỗi: Port 8001 already in use
**Giải pháp:**
```bash
# Find process on port 8001
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8001 | xargs kill -9

# Hoặc dùng port khác
uvicorn server:app --port 8002
```

### ❌ Frontend không kết nối được Backend
**Giải pháp:**
1. Check backend đang chạy: http://localhost:8001/api/
2. Check CORS settings trong backend
3. Verify frontend .env:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```
4. Restart frontend

---

## 📊 Database Schema

### temp_emails table
```sql
CREATE TABLE temp_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    expires_at DATETIME NOT NULL,
    message_count INT DEFAULT 0,
    provider VARCHAR(50) DEFAULT 'mailtm',
    mailbox_id VARCHAR(255),
    username VARCHAR(255),
    domain VARCHAR(255),
    INDEX idx_address (address)
);
```

### email_history table
```sql
CREATE TABLE email_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    expired_at DATETIME NOT NULL,
    provider VARCHAR(50) DEFAULT 'mailtm',
    username VARCHAR(255),
    domain VARCHAR(255)
);
```

---

## 📝 API Endpoints

### Core Email Operations
- `POST /api/emails/create` - Tạo email mới (random provider)
- `GET /api/emails` - List active emails
- `GET /api/emails/{id}` - Get email detail
- `DELETE /api/emails/{id}` - Delete email
- `POST /api/emails/{id}/extend-time` - Extend thêm 10 phút

### Messages
- `GET /api/emails/{id}/messages` - Get inbox messages
- `GET /api/emails/{id}/messages/{msg_id}` - Message detail
- `POST /api/emails/{id}/refresh` - Refresh inbox

### History
- `GET /api/emails/history/list` - List history emails
- `GET /api/emails/history/{id}/messages` - History messages
- `DELETE /api/emails/history/delete` - Delete history (selective or all)

### Utility
- `GET /api/` - Health check & provider stats
- `GET /api/domains?service=auto` - Get available domains

---

## 🎯 Features

✅ **Random Provider Selection**
- Auto mode shuffle providers mỗi request
- Load balancing giữa Mail.tm, Mail.gw, Guerrilla Mail
- Bypass rate limits hiệu quả

✅ **Auto Email Expiry**
- Email tự động hết hạn sau 10 phút
- Tự động chuyển vào lịch sử
- Tự động tạo email mới

✅ **Extend Time**
- Reset về 10 phút (không cộng dồn)
- Click "Làm mới 10 phút"

✅ **Email History**
- Xem email đã hết hạn
- Selective delete với checkbox
- Delete all option

---

## 🔍 Monitoring

### Check Backend Logs
Backend sẽ log tất cả operations:
```
🎲 Random provider order: ['mailgw', 'guerrilla', 'mailtm']
🔄 Trying mailgw...
✅ Mail.gw email created: test@mail.gw
⏸️ Mail.tm is in cooldown (remaining: 45s)
```

### Database Queries
```sql
-- Check active emails
SELECT id, address, provider, created_at, expires_at FROM temp_emails;

-- Check history
SELECT id, address, provider, expired_at FROM email_history ORDER BY expired_at DESC;

-- Provider distribution
SELECT provider, COUNT(*) as count FROM temp_emails GROUP BY provider;
```

---

## 📦 Cấu trúc Project

```
tempmail-app/
├── backend/
│   ├── server.py                      # Main server (với random selection)
│   ├── database.py                    # SQLAlchemy MySQL config
│   ├── models.py                      # SQLAlchemy models
│   ├── init_db.py                     # Database initialization
│   ├── requirements.txt               # Python dependencies
│   └── .env                          # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js                    # Main React component
│   │   ├── App.css                   # Styles
│   │   └── index.js                  # Entry point
│   ├── public/
│   ├── package.json                  # Node dependencies
│   └── .env                          # Frontend config
└── HUONG_DAN_CHAY_MYSQL_LOCAL.md    # This file
```

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Start MySQL
mysql -u root -p190705 -e "CREATE DATABASE IF NOT EXISTS temp_mail;"

# 2. Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# 3. Frontend (Terminal 2)
cd frontend
yarn install
PORT=7050 yarn start

# 4. Open browser
# http://localhost:7050
```

---

## ✅ Success Checklist

- [ ] MySQL 8.0+ installed and running
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ and Yarn installed
- [ ] Database `temp_mail` created
- [ ] Backend .env configured
- [ ] Frontend .env configured
- [ ] Backend running on port 8001
- [ ] Frontend running on port 7050
- [ ] Can create email successfully
- [ ] Random provider selection working
- [ ] Can receive and view messages
- [ ] Timer countdown working
- [ ] Can extend email time
- [ ] History tab working

---

## 📞 Support

Nếu gặp vấn đề, check:
1. Backend logs trong terminal
2. Frontend console (F12 → Console)
3. MySQL connection: `mysql -u root -p190705`
4. Port conflicts: `netstat -ano | findstr :8001`

---

## 🎉 Done!

Application của bạn giờ đang chạy với:
- ✅ MySQL database (localhost:3306)
- ✅ FastAPI backend (localhost:8001)
- ✅ React frontend (localhost:7050)
- ✅ Random provider selection
- ✅ Auto email expiry
- ✅ Email history management

Enjoy! 📧
