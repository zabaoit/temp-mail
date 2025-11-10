# 🚀 HƯỚNG DẪN CHẠY ỨNG DỤNG TEMPMAIL VỚI MYSQL

## 📋 YÊU CẦU HỆ THỐNG

### Phần mềm cần cài đặt:
- **Python 3.9+** (khuyến nghị Python 3.10 hoặc 3.11)
- **Node.js 18+** và **Yarn**
- **MySQL 8.0+** (Khuyên dùng MySQL 8.0 hoặc mới hơn)
- **Git** (để clone code)

---

## 🔧 BƯỚC 1: CÀI ĐẶT MYSQL

### Windows:
1. Download MySQL Installer: https://dev.mysql.com/downloads/installer/
2. Chọn "MySQL Installer for Windows"
3. Cài đặt với tùy chọn "Developer Default"
4. Khi đặt root password, nhập: **190705** (hoặc password bạn muốn)
5. Kiểm tra MySQL đã chạy:
```cmd
mysql --version
mysql -u root -p190705
```

### macOS:
```bash
# Cài qua Homebrew
brew install mysql

# Khởi động MySQL
brew services start mysql

# Đặt root password (chọn password hoặc để trống)
mysql_secure_installation

# Kết nối MySQL
mysql -u root -p
```

### Linux (Ubuntu/Debian):
```bash
# Cài đặt MySQL Server
sudo apt update
sudo apt install mysql-server

# Khởi động MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Cấu hình MySQL
sudo mysql_secure_installation

# Kết nối MySQL
sudo mysql -u root -p
```

### Tạo User và Database (Quan trọng!):

Kết nối vào MySQL:
```bash
mysql -u root -p
```

Chạy các lệnh SQL sau:
```sql
-- Tạo database
CREATE DATABASE IF NOT EXISTS temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user (nếu cần) hoặc dùng root
-- CREATE USER 'tempmail_user'@'localhost' IDENTIFIED BY '190705';
-- GRANT ALL PRIVILEGES ON temp_mail.* TO 'tempmail_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Kiểm tra database đã tạo
SHOW DATABASES;

-- Thoát
EXIT;
```

**Lưu ý:** Ứng dụng mặc định dùng:
- Username: `root`
- Password: `190705`
- Database: `temp_mail`

---

## 📥 BƯỚC 2: TẢI VÀ GIẢI NÉN CODE

### Cách 1: Download từ Emergent
1. Vào project của bạn trên Emergent
2. Click nút **"Save to Github"** hoặc **"Download"**
3. Giải nén file zip vào thư mục bạn muốn

### Cách 2: Clone từ Github (nếu đã push)
```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## ⚙️ BƯỚC 3: CÀI ĐẶT BACKEND (Python/FastAPI)

### 1. Di chuyển vào thư mục backend:
```bash
cd backend
```

### 2. Tạo Python Virtual Environment:

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Sau khi activate, bạn sẽ thấy `(venv)` ở đầu dòng lệnh.

### 3. Cài đặt dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Cấu hình file .env:

File `/app/backend/.env` đã có sẵn với MySQL config:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

**⚠️ QUAN TRỌNG:** Nếu bạn dùng password khác cho MySQL root, sửa dòng:
```env
DB_PASSWORD=your_mysql_password
```

### 5. Khởi tạo Database (Tạo Tables):

```bash
# Vẫn ở trong thư mục backend với venv đã activate
python init_db.py
```

Nếu thành công, bạn sẽ thấy:
```
✅ Kết nối MySQL thành công!
✅ Database 'temp_mail' đã sẵn sàng!
✅ Tất cả tables đã được tạo thành công!
```

### 6. Khởi động Backend:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Kiểm tra Backend:**
- Mở trình duyệt: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Nếu thấy trang JSON hoặc Swagger UI → Backend đã chạy! ✅

**Giữ cửa sổ terminal này mở!**

---

## 🎨 BƯỚC 4: CÀI ĐẶT FRONTEND (React)

### 1. Mở terminal MỚI (đừng tắt terminal backend)

### 2. Di chuyển vào thư mục frontend:
```bash
cd frontend
```

### 3. Cài đặt Yarn (nếu chưa có):
```bash
npm install -g yarn
```

### 4. Cài đặt dependencies:
```bash
yarn install
```

### 5. Kiểm tra file .env:
File `/app/frontend/.env` đã có sẵn:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=3000
```

### 6. Khởi động Frontend:
```bash
yarn start
```

Sau vài giây, trình duyệt sẽ tự động mở trang: **http://localhost:3000**

**Frontend đã chạy! ✅**

---

## 🎯 SỬ DỤNG ỨNG DỤNG

### Truy cập:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs

### Tính năng chính:
1. **Tạo email tự động:** App tự tạo email ngay khi mở
2. **Chọn Service:** Mail.tm, Mail.gw, Guerrilla Mail, Auto (random)
3. **Chọn Domain:** Dropdown domain theo service đã chọn
4. **Xem tin nhắn:** Click vào email để xem inbox
5. **Làm mới 10 phút:** Extend thời gian email
6. **Lịch sử:** Xem email đã hết hạn
7. **Lưu email:** Lưu email quan trọng vào tab "Mail đã lưu"

---

## 🐛 TROUBLESHOOTING (Xử lý lỗi)

### Lỗi 1: Backend không khởi động - MySQL Connection Error
**Lỗi:** `Can't connect to MySQL server` hoặc `Access denied for user 'root'`

**Giải pháp:**

**a) Kiểm tra MySQL đang chạy:**
```bash
# Windows:
net start MySQL80  # hoặc MySQL57, MySQL tùy version

# macOS:
brew services list | grep mysql
brew services start mysql

# Linux:
sudo systemctl status mysql
sudo systemctl start mysql
```

**b) Test kết nối MySQL:**
```bash
mysql -u root -p190705

# Hoặc nếu không có password:
mysql -u root
```

**c) Sửa password trong .env:**
Mở file `backend/.env` và sửa:
```env
DB_PASSWORD=your_actual_password
```

**d) Tạo lại database:**
```bash
mysql -u root -p
```
```sql
DROP DATABASE IF EXISTS temp_mail;
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Sau đó chạy lại:
```bash
python init_db.py
```

### Lỗi 2: init_db.py thất bại
**Lỗi:** `Table already exists` hoặc `Database not found`

**Giải pháp:**
```bash
# Reset database (XÓA TẤT CẢ DỮ LIỆU!)
python init_db.py --reset
# Nhập "yes" để xác nhận
```

### Lỗi 3: Backend lỗi "ModuleNotFoundError"
**Lỗi:** `No module named 'fastapi'` hoặc module khác

**Giải pháp:**
```bash
# Đảm bảo venv đã activate (có dấu (venv) ở đầu dòng)
pip install -r requirements.txt

# Nếu vẫn lỗi, cài thủ công:
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
```

### Lỗi 4: Frontend không tìm thấy backend
**Lỗi:** `Network Error` hoặc `ERR_CONNECTION_REFUSED`

**Giải pháp:**
1. Kiểm tra backend đang chạy: http://localhost:8001
2. Kiểm tra file `frontend/.env`:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```
3. Restart frontend sau khi sửa .env

### Lỗi 5: Port đã được sử dụng
**Lỗi:** `Address already in use`

**Giải pháp:**

**Cho Backend (port 8001):**
```bash
# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8001 | xargs kill -9
```

**Cho Frontend (port 3000):**
```bash
# Sửa file frontend/.env
PORT=3001  # Đổi sang port khác
```

### Lỗi 6: MySQL không tìm thấy tables
**Lỗi:** `Table 'temp_mail.temp_emails' doesn't exist`

**Giải pháp:**
```bash
cd backend
python init_db.py
```

---

## 🔄 RESTART ỨNG DỤNG

### Tắt ứng dụng:
- Nhấn **Ctrl+C** trong terminal backend
- Nhấn **Ctrl+C** trong terminal frontend

### Chạy lại:

**Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend:**
```bash
cd frontend
yarn start
```

---

## 🗄️ QUẢN LÝ DATABASE

### Xem dữ liệu trong MySQL:
```bash
mysql -u root -p190705
```

```sql
USE temp_mail;

-- Xem tất cả tables
SHOW TABLES;

-- Xem cấu trúc table
DESCRIBE temp_emails;
DESCRIBE email_history;
DESCRIBE saved_emails;

-- Xem dữ liệu
SELECT * FROM temp_emails;
SELECT * FROM email_history ORDER BY expired_at DESC LIMIT 10;
SELECT * FROM saved_emails;

-- Xóa tất cả dữ liệu (CẨNTHẬN!)
TRUNCATE TABLE temp_emails;
TRUNCATE TABLE email_history;
TRUNCATE TABLE saved_emails;

-- Thoát
EXIT;
```

### Reset hoàn toàn database:
```bash
# Cách 1: Dùng init_db.py
cd backend
python init_db.py --reset

# Cách 2: Thủ công
mysql -u root -p190705
```
```sql
DROP DATABASE temp_mail;
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```
```bash
python init_db.py
```

---

## 📂 CẤU TRÚC DATABASE

### Table: temp_emails (Email đang hoạt động)
```sql
id              INT (Primary Key, Auto Increment)
address         VARCHAR(255) UNIQUE
password        VARCHAR(255)
token           TEXT
account_id      VARCHAR(255)
created_at      DATETIME
expires_at      DATETIME
message_count   INT
provider        VARCHAR(50)
username        VARCHAR(255)
domain          VARCHAR(255)
```

### Table: email_history (Email đã hết hạn)
```sql
id              INT (Primary Key, Auto Increment)
address         VARCHAR(255)
token           TEXT
account_id      VARCHAR(255)
expired_at      DATETIME
provider        VARCHAR(50)
username        VARCHAR(255)
domain          VARCHAR(255)
```

### Table: saved_emails (Email đã lưu)
```sql
id              INT (Primary Key, Auto Increment)
email_id        INT
message_id      VARCHAR(255)
subject         TEXT
sender          VARCHAR(255)
saved_at        DATETIME
html_content    LONGTEXT
text_content    LONGTEXT
provider        VARCHAR(50)
```

---

## 📂 CẤU TRÚC THỨ MỤC

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI (MySQL version) ✅
│   ├── server_mongodb.py      # MongoDB backup
│   ├── models.py              # SQLAlchemy models (MySQL)
│   ├── database.py            # MySQL connection
│   ├── init_db.py            # Database initialization
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # MySQL configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles
│   │   └── index.js          # Entry point
│   ├── public/               # Static files
│   ├── package.json          # Node dependencies
│   └── .env                  # Frontend configuration
│
└── HUONG_DAN_MYSQL_LOCAL.md  # File này!
```

---

## ✅ CHECKLIST TRƯỚC KHI CHẠY

- [ ] Python 3.9+ đã cài đặt
- [ ] Node.js 18+ và Yarn đã cài đặt
- [ ] **MySQL 8.0+ đã cài đặt và đang chạy** ✅
- [ ] Database `temp_mail` đã được tạo
- [ ] Code đã download/clone về máy
- [ ] Backend dependencies đã cài (`pip install -r requirements.txt`)
- [ ] Frontend dependencies đã cài (`yarn install`)
- [ ] File `.env` đã cấu hình đúng MySQL credentials
- [ ] **Chạy `python init_db.py` để tạo tables** ✅
- [ ] Port 8001 và 3000 chưa bị sử dụng

---

## 🆘 CẦU GIÚP ĐỠ?

### Kiểm tra logs:
**Backend logs:** Xem trong terminal đang chạy backend
**Frontend logs:** Xem trong terminal frontend hoặc Browser Console (F12)
**MySQL logs:** 
- Windows: `C:\ProgramData\MySQL\MySQL Server 8.0\Data\`
- macOS: `/usr/local/var/mysql/`
- Linux: `/var/log/mysql/error.log`

### Các lệnh hữu ích:

**Kiểm tra MySQL version:**
```bash
mysql --version
```

**Kiểm tra MySQL đang chạy:**
```bash
# Windows:
sc query MySQL80

# macOS:
brew services list | grep mysql

# Linux:
sudo systemctl status mysql
```

**Xem tất cả databases:**
```bash
mysql -u root -p -e "SHOW DATABASES;"
```

**Xem tất cả tables:**
```bash
mysql -u root -p temp_mail -e "SHOW TABLES;"
```

---

## 🔐 BẢO MẬT

**QUAN TRỌNG cho Production:**

1. Đổi MySQL root password phức tạp hơn
2. Tạo user riêng cho app (không dùng root):
```sql
CREATE USER 'tempmail_app'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON temp_mail.* TO 'tempmail_app'@'localhost';
FLUSH PRIVILEGES;
```

3. Cập nhật file `.env`:
```env
DB_USER=tempmail_app
DB_PASSWORD=strong_password_here
```

4. Không commit file `.env` lên Git!

---

## 🎉 CHÚC BẠN THÀNH CÔNG!

Nếu làm theo đúng các bước trên, ứng dụng TempMail với MySQL sẽ chạy mượt mà trên máy local của bạn!

**Ưu điểm của MySQL:**
- ✅ Phổ biến và dễ cài đặt
- ✅ Công cụ quản lý GUI tốt (MySQL Workbench, phpMyAdmin)
- ✅ Performance tốt với relational data
- ✅ Transaction support
- ✅ Foreign key constraints

**Lưu ý quan trọng:**
- ✅ **Mail.tm và Mail.gw:** Tạo email theo đúng domain đã chọn
- ⚠️ **Guerrilla Mail:** API không cho phép chọn domain cụ thể

**Có thắc mắc?** Kiểm tra phần Troubleshooting hoặc xem MySQL logs để debug!
