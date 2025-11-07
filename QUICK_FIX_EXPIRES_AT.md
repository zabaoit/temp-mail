# ⚡ QUICK FIX: Unknown column 'expires_at' Error

## 🎯 Bạn đang thấy lỗi này?

```
ERROR - Unknown column 'temp_emails.expires_at' in 'field list'
```

---

## ✅ Giải pháp 1-command:

```bash
cd backend
python setup_database.py
```

**Xong!** Script này sẽ:
- ✅ Tự động thêm column `expires_at` nếu thiếu
- ✅ Tạo table `email_history` nếu chưa có
- ✅ Cập nhật dữ liệu cũ
- ✅ Không làm mất dữ liệu hiện có

---

## 🚀 Sau khi chạy script:

### 1. Start Backend
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Start Frontend (Terminal mới)
```bash
cd ../frontend
PORT=7050 yarn start
```

### 3. Mở trình duyệt
```
http://localhost:7050
```

---

## ✨ Bạn sẽ thấy:

✅ Email tự động được tạo khi vào trang  
✅ Timer đếm ngược 10 phút  
✅ Khi hết hạn → tự động tạo email mới  
✅ Background tasks chạy không có lỗi  

---

## 📋 Output mong đợi từ setup_database.py:

```
======================================================================
🚀 TEMPMAIL DATABASE SETUP
======================================================================
Host: localhost:3306
Database: temp_mail
User: root

🔌 Connecting to MySQL server...
✅ Connected to MySQL

📦 Creating database...
✅ Database 'temp_mail' is ready

🔍 Checking tables...
✅ Table 'temp_emails' exists
⚠️  Column 'expires_at' missing - running migration...
✅ Added expires_at column and updated existing records

📋 Creating email_history table...
✅ Created email_history table

======================================================================
📊 FINAL DATABASE STRUCTURE
======================================================================

📋 temp_emails:
   • id: varchar(36)
   • address: varchar(255)
   • password: varchar(255)
   • token: text
   • account_id: varchar(255)
   • created_at: datetime
   • expires_at: datetime
   • message_count: int(11)

📋 email_history:
   • id: varchar(36)
   • address: varchar(255)
   • password: varchar(255)
   • token: text
   • account_id: varchar(255)
   • created_at: datetime
   • expired_at: datetime
   • message_count: int(11)

======================================================================
✅ DATABASE SETUP COMPLETED SUCCESSFULLY!
======================================================================
```

---

## ❓ Nếu vẫn gặp lỗi "Can't connect to MySQL"

```bash
# Kiểm tra MySQL đang chạy
mysql -u root -p190705

# Nếu không kết nối được:

# Windows
services.msc → Tìm MySQL → Start

# Mac  
mysql.server start

# Linux
sudo systemctl start mysql
```

---

## 🔄 Giải pháp thay thế: Reset database

**⚠️ Cách này sẽ XÓA tất cả email hiện có!**

```bash
mysql -u root -p190705 -e "DROP DATABASE temp_mail;"
cd backend
python setup_database.py
```

---

**Chỉ 1 command, mọi thứ OK! 🎉**
