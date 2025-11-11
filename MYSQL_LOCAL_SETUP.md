# ✅ Ứng Dụng Đã Chuyển Hoàn Toàn Sang MySQL

## 📋 Tổng Quan

Ứng dụng TempMail đã được **chuyển đổi hoàn toàn** từ MongoDB sang MySQL/MariaDB.

### ✅ Đã Hoàn Thành

1. **Backend**: Sử dụng SQLAlchemy + MySQL/MariaDB
2. **Database Models**: 3 bảng chính
   - `temp_emails`: Email tạm thời đang active
   - `email_history`: Lịch sử email đã hết hạn
   - `saved_emails`: Email đã được lưu
3. **MongoDB**: Đã hoàn toàn loại bỏ
   - ❌ Không còn import pymongo/motor
   - ❌ MongoDB service đã stopped
   - ❌ Không còn MONGO_URL trong .env
4. **API**: Hoạt động hoàn hảo với MySQL

## 🔧 Cấu Hình Hiện Tại

### Backend Configuration (`.env`)
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

### Database Schema
```sql
-- temp_emails
CREATE TABLE temp_emails (
    id INT PRIMARY KEY AUTO_INCREMENT,
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

-- email_history
CREATE TABLE email_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    expired_at DATETIME NOT NULL,
    message_count INT DEFAULT 0,
    INDEX idx_address (address)
);

-- saved_emails
CREATE TABLE saved_emails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email_address VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    from_address VARCHAR(255),
    from_name VARCHAR(255),
    html TEXT,
    text TEXT,
    created_at DATETIME NOT NULL,
    saved_at DATETIME NOT NULL,
    INDEX idx_email_address (email_address)
);
```

## 🚀 Chạy Trên Máy Local

### Yêu Cầu
- Python 3.8+
- Node.js 18+
- MySQL 8.0+ hoặc MariaDB 10.11+

### Bước 1: Cài Đặt MySQL/MariaDB

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Windows:**
- Download MySQL Community Server từ: https://dev.mysql.com/downloads/mysql/
- Hoặc download MariaDB từ: https://mariadb.org/download/

### Bước 2: Cấu Hình Database

```bash
# Đăng nhập MySQL với user root
sudo mysql -u root

# Hoặc nếu đã set password:
mysql -u root -p
```

```sql
-- Tạo database
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user (optional, hoặc dùng root)
CREATE USER 'tempmail'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON temp_mail.* TO 'tempmail'@'localhost';
FLUSH PRIVILEGES;

-- Kiểm tra
SHOW DATABASES;
```

### Bước 3: Cấu Hình .env

Chỉnh sửa `/app/backend/.env`:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

### Bước 4: Cài Đặt Dependencies

**Backend:**
```bash
cd /app/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd /app/frontend
yarn install
```

### Bước 5: Chạy Ứng Dụng

**Backend:**
```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend:**
```bash
cd /app/frontend
yarn start
```

### Bước 6: Truy Cập

- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/api/
- API Docs: http://localhost:8001/docs

## 🧪 Test MySQL Connection

### Test bằng Python:
```python
import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='190705',
    database='temp_mail'
)

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tables:", tables)

connection.close()
```

### Test bằng Command Line:
```bash
# Kiểm tra kết nối
mysql -u root -p190705 -e "SELECT 1;"

# Xem tables
mysql -u root -p190705 temp_mail -e "SHOW TABLES;"

# Xem dữ liệu
mysql -u root -p190705 temp_mail -e "SELECT * FROM temp_emails LIMIT 5;"
```

### Test bằng API:
```bash
# Health check
curl http://localhost:8001/api/

# Tạo email
curl -X POST http://localhost:8001/api/emails/create \
  -H "Content-Type: application/json" \
  -d '{"service": "auto"}'

# Lấy danh sách emails
curl http://localhost:8001/api/emails
```

## 📊 Database Management

### Backup Database
```bash
mysqldump -u root -p190705 temp_mail > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
mysql -u root -p190705 temp_mail < backup_20250111.sql
```

### Reset Database
```bash
mysql -u root -p190705 temp_mail -e "
  DROP TABLE IF EXISTS temp_emails;
  DROP TABLE IF EXISTS email_history;
  DROP TABLE IF EXISTS saved_emails;
"

# Restart backend để tạo lại tables
```

## 🐛 Troubleshooting

### 1. Lỗi "Can't connect to MySQL server"

**Giải pháp:**
```bash
# Kiểm tra MySQL có chạy không
sudo systemctl status mysql
# hoặc
sudo systemctl status mariadb

# Nếu không chạy, start MySQL
sudo systemctl start mysql
```

### 2. Lỗi "Access denied for user 'root'@'localhost'"

**Giải pháp:**
```bash
# Reset password MySQL root user
sudo mysql -u root

# Trong MySQL shell:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
EXIT;

# Cập nhật password trong .env
```

### 3. Lỗi "Unknown database 'temp_mail'"

**Giải pháp:**
```bash
mysql -u root -p190705 -e "CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 4. Backend không start

**Kiểm tra logs:**
```bash
# Nếu dùng supervisor
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/backend.err.log

# Nếu chạy trực tiếp
cd /app/backend
python -c "from database import engine; print('Database connected!')"
```

## 📝 Lưu Ý Quan Trọng

1. **Password Security**: 
   - Trong production, sử dụng password mạnh hơn
   - Không commit file .env lên git

2. **Performance**:
   - MySQL phù hợp cho production hơn MongoDB cho use case này
   - Tables có index trên các cột thường query

3. **Backup**:
   - Nên backup database định kỳ
   - Sử dụng `mysqldump` hoặc công cụ backup khác

4. **Container vs Local**:
   - Trong container: MySQL có thể không khởi động được do resource limit
   - Trên local machine: MySQL hoạt động tốt hơn

## ✅ Checklist Hoàn Thành

- ✅ Code đã chuyển hoàn toàn sang SQLAlchemy + MySQL
- ✅ Không còn tham chiếu đến MongoDB trong code
- ✅ MongoDB service đã stopped
- ✅ MySQL/MariaDB đã cài đặt và chạy
- ✅ Database `temp_mail` đã được tạo
- ✅ 3 tables đã được tạo tự động
- ✅ API test thành công
- ✅ Data được lưu vào MySQL chính xác

## 🎉 Kết Luận

Ứng dụng TempMail đã **chuyển đổi hoàn toàn từ MongoDB sang MySQL**. Tất cả tính năng hoạt động bình thường với MySQL backend.

Để chạy trên máy local, bạn chỉ cần:
1. Cài MySQL/MariaDB
2. Tạo database `temp_mail`
3. Cấu hình `.env` với thông tin MySQL
4. Chạy backend và frontend

**Ứng dụng đã sẵn sàng để deploy lên production với MySQL!** 🚀
