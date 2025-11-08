# 📝 IMPORTANT NOTE - MySQL Setup

## Current Container Environment

Bạn hiện đang ở trong **Kubernetes Container** với MongoDB.

Để chuyển sang MySQL, bạn cần:

## 🔄 Thay đổi File Server

### Khi download về local, làm theo:

1. **Backup file hiện tại:**
```bash
cd backend
mv server.py server_mongodb.py
```

2. **Chọn version phù hợp:**

Bạn có 2 options:

### Option A: Dùng Server Cũ (Stable nhưng không có random selection)
```bash
mv server_mysql.py server.py
```

### Option B: Dùng Server Mới (Có random selection - RECOMMENDED) ⭐
```bash
# Server này là bản MongoDB đã được modify
# Bạn cần update một số chỗ để dùng SQLAlchemy

# Hoặc tôi sẽ tạo sẵn một version hoàn chỉnh cho bạn
```

## ⚙️ Kiểm tra Requirements

File `/backend/requirements.txt` cần có:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
httpx==0.27.0
pydantic==2.5.0
sqlalchemy==2.0.23
pymysql==1.1.0
```

**KHÔNG CẦN:**
- motor (MongoDB driver)
- pymongo

## 🗄️ Database Models

File `/backend/models.py` đã sẵn sàng với:
- TempEmail model (với expires_at)
- EmailHistory model
- Integer ID (autoincrement)

File `/backend/database.py` đã có:
- MySQL connection config
- SQLAlchemy setup
- Database creation logic

## 🚀 Init Database Script

File `/backend/init_db.py` để tạo tables:

```python
from database import engine, Base
from models import TempEmail, EmailHistory

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ All tables created!")
```

## 📋 Checklist Trước Khi Chạy Local

- [ ] Download toàn bộ code về máy local
- [ ] Cài MySQL 8.0+ và start service
- [ ] Tạo database `temp_mail`
- [ ] Tạo `.env` file với MySQL credentials
- [ ] Chạy `pip install -r requirements.txt`
- [ ] Chạy `python init_db.py` để tạo tables
- [ ] Verify server.py import từ `database` và `models` (không phải database_mongodb)
- [ ] Chạy `uvicorn server:app --reload`

## 🔍 Verify Server File

Mở `/backend/server.py` và check imports:

### ✅ Đúng (MySQL):
```python
from database import engine, get_db, Base
from models import TempEmail as TempEmailModel, EmailHistory as EmailHistoryModel
```

### ❌ Sai (MongoDB):
```python
from database_mongodb import database, emails_collection, history_collection
```

## 🎲 Random Selection Feature

Random selection đã được implement trong:
- `server.py` (MongoDB version - hiện tại trong container)
- `server_mongodb.py` (MongoDB version - có random)

Để có random selection trong MySQL version, code cần có:

```python
else:  # auto - RANDOM SELECTION
    providers_to_try = ["mailtm", "mailgw", "guerrilla"]
    random.shuffle(providers_to_try)
    logging.info(f"🎲 Random provider order: {providers_to_try}")
```

## 💡 Recommendation

Tôi khuyến nghị:

1. **Download code về local**
2. **Kiểm tra server.py imports** (MySQL hay MongoDB)
3. **Nếu import MongoDB** → tôi sẽ tạo một MySQL version hoàn chỉnh cho bạn
4. **Hoặc** tự sửa imports + database operations

---

Bạn có muốn tôi tạo một **server.py hoàn chỉnh với MySQL + Random Selection** không?
