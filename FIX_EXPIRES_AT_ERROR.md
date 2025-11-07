# ⚠️ FIX: Unknown column 'expires_at' Error

## Vấn đề

Nếu bạn thấy lỗi này khi chạy backend:
```
ERROR - Unknown column 'temp_emails.expires_at' in 'field list'
```

**Nguyên nhân:** Database của bạn đã tồn tại từ trước với schema cũ (không có column `expires_at`)

---

## ✅ Giải pháp - Chạy Migration Script

### Bước 1: Dừng backend

Nếu backend đang chạy, nhấn `Ctrl+C` để dừng.

### Bước 2: Chạy migration script

```bash
cd backend
python migrate_db.py
```

**Output mong đợi:**
```
============================================================
DATABASE MIGRATION SCRIPT
============================================================
Host: localhost:3306
Database: temp_mail
User: root

✅ Connected to MySQL database

🔍 Checking temp_emails table...
⚠️  Column 'expires_at' not found in temp_emails
➕ Adding expires_at column...
✅ Added expires_at column to temp_emails

🔍 Checking email_history table...
⚠️  Table 'email_history' not found
➕ Creating email_history table...
✅ Created email_history table

📋 Current table structure:

temp_emails:
  - id: varchar(36)
  - address: varchar(255)
  - password: varchar(255)
  - token: text
  - account_id: varchar(255)
  - created_at: datetime
  - expires_at: datetime
  - message_count: int

email_history:
  - id: varchar(36)
  - address: varchar(255)
  - password: varchar(255)
  - token: text
  - account_id: varchar(255)
  - created_at: datetime
  - expired_at: datetime
  - message_count: int

============================================================
✅ MIGRATION COMPLETED SUCCESSFULLY!
============================================================
```

### Bước 3: Restart backend

```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🔄 Giải pháp thay thế: Xóa và tạo lại database

**⚠️ Cảnh báo:** Cách này sẽ **XÓA TẤT CẢ DỮ LIỆU** hiện có!

### Bước 1: Xóa database cũ

```bash
mysql -u root -p190705 -e "DROP DATABASE IF EXISTS temp_mail;"
```

### Bước 2: Tạo lại database

```bash
cd backend
python init_db.py
```

### Bước 3: Restart backend

```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🧪 Kiểm tra

Sau khi chạy migration, backend logs sẽ hiển thị:

```
✅ Database 'temp_mail' is ready!
✅ Loaded .env file from: /app/backend/.env
✅ DB credentials loaded - User: root, Database: temp_mail
INFO:     Application started with background tasks (MySQL)
INFO:     Background tasks started
```

**KHÔNG còn lỗi** về `expires_at`!

---

## 📋 Migration Script làm gì?

1. **Kiểm tra** column `expires_at` có tồn tại không
2. **Thêm** column `expires_at` nếu chưa có
3. **Update** các record cũ: `expires_at = created_at + 10 phút`
4. **Tạo** table `email_history` nếu chưa có
5. **Hiển thị** structure của tables

---

## ❓ Nếu vẫn gặp lỗi

### Lỗi: "Can't connect to MySQL"

```bash
# Kiểm tra MySQL đang chạy
mysql -u root -p190705

# Windows
services.msc → MySQL → Start

# Mac
mysql.server start

# Linux
sudo systemctl start mysql
```

### Lỗi: "Access denied"

Kiểm tra file `backend/.env`:
```env
DB_USER=root
DB_PASSWORD=190705
```

### Lỗi: "Database doesn't exist"

```bash
cd backend
python init_db.py
```

---

## 💡 Tóm tắt

**Nếu thấy lỗi `expires_at`:**
```bash
cd backend
python migrate_db.py
python -m uvicorn server:app --reload
```

**Hoặc reset toàn bộ:**
```bash
mysql -u root -p190705 -e "DROP DATABASE IF EXISTS temp_mail;"
cd backend
python init_db.py
python -m uvicorn server:app --reload
```

✅ Xong!
