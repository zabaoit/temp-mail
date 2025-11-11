# 🪟 Hướng Dẫn Chạy TempMail Trên Windows

## ✅ Backend Đã Hoạt Động!

Như log bạn gửi, backend đã chạy thành công trên Windows với MySQL:
```
✅ Loaded .env file from: D:\tool_mail\temp-mail\backend\.env
✅ DB credentials loaded - User: root, Database: temp_mail
✅ Database 'temp_mail' is ready!
✅ Application started with background tasks (MySQL)
✅ Active providers: Mail.tm, 1secmail, Mail.gw, Guerrilla Mail
```

## 🔧 Cấu Hình Hoàn Chỉnh

### 1. Backend (Đã Chạy ✅)
- Port: 8001
- Database: MySQL/MariaDB
- Auto failover: Mail.tm → Mail.gw → Guerrilla → 1secmail

### 2. Frontend (Cần Chạy)

Mở terminal mới (PowerShell hoặc CMD):
```powershell
cd D:\tool_mail\temp-mail\frontend
yarn install  # Nếu chưa install
yarn start
```

Frontend sẽ chạy trên: http://localhost:3000

## 📝 File .env Đã Cấu Hình

### Backend (.env)
```ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```ini
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=7050  # Hoặc 3000
```

**Lưu ý:** Đảm bảo `REACT_APP_BACKEND_URL` trỏ đến backend đúng port (8001)

## 🎯 Rate Limiting & Failover

### Vấn Đề Bạn Gặp
Log cho thấy Mail.tm bị rate limited (429) sau 3-4 requests:
```
2025-11-11 15:07:12,870 - httpx - INFO - HTTP Request: POST https://api.mail.tm/accounts "HTTP/1.1 429 Too Many Requests"
2025-11-11 15:07:12,871 - root - WARNING - ⚠️ Mail.tm rate limited (429)
2025-11-11 15:07:12,871 - root - WARNING - 🔒 mailtm cooldown set for 60s
```

### ✅ Giải Pháp Đã Áp Dụng

**1. Auto Failover:**
- Khi Mail.tm bị rate limit → tự động chuyển sang Mail.gw
- Khi Mail.gw fail → chuyển sang Guerrilla Mail
- Khi Guerrilla fail → chuyển sang 1secmail

**2. Cooldown System:**
- Provider bị rate limit → cooldown 60 giây
- Trong 60s, tự động skip provider đó và dùng provider khác

**3. Random Provider Order:**
```
🎲 Random provider order: ['guerrilla', 'mailgw', '1secmail', 'mailtm']
```
Mỗi lần tạo email sẽ random thứ tự providers để phân tán load.

## 🧪 Test Failover

### Test 1: Tạo Email Liên Tục
```bash
# Request 1
curl -X POST http://localhost:8001/api/emails/create -d '{"service":"auto"}'
# ✅ Mail.tm success

# Request 2-3
# ✅ Mail.tm success

# Request 4
# ⚠️ Mail.tm rate limited → ✅ Tự động chuyển sang Guerrilla Mail

# Request 5-10
# ✅ Guerrilla Mail hoặc Mail.gw
```

### Test 2: Chọn Provider Cụ Thể
```bash
# Chỉ dùng Mail.tm
curl -X POST http://localhost:8001/api/emails/create -d '{"service":"mailtm"}'

# Chỉ dùng Guerrilla
curl -X POST http://localhost:8001/api/emails/create -d '{"service":"guerrilla"}'

# Chỉ dùng Mail.gw
curl -X POST http://localhost:8001/api/emails/create -d '{"service":"mailgw"}'

# Chỉ dùng 1secmail
curl -X POST http://localhost:8001/api/emails/create -d '{"service":"1secmail"}'
```

## 📊 Monitoring Providers

### API Status Endpoint
```bash
curl http://localhost:8001/api/
```

Response:
```json
{
  "message": "TempMail API - MySQL with Multiple Providers",
  "providers": ["Mail.tm", "Mail.gw", "1secmail", "Guerrilla Mail"],
  "stats": {
    "mailtm": {
      "success": 3,
      "failures": 1,
      "cooldown_until": 1699699692,
      "status": "cooldown (55s remaining)",
      "success_rate": "75.0%"
    },
    "mailgw": {
      "success": 0,
      "failures": 0,
      "status": "active",
      "success_rate": "N/A"
    }
  }
}
```

## 🐛 Troubleshooting

### 1. Backend Lỗi "Can't connect to MySQL"

**Kiểm tra MySQL:**
```bash
mysql -u root -p190705 -e "SELECT 1;"
```

**Nếu lỗi, restart MySQL:**
```powershell
# Mở Services (Win + R → services.msc)
# Tìm MySQL hoặc MariaDB → Right click → Restart
```

### 2. Frontend Không Kết Nối Backend

**Kiểm tra file `.env`:**
```ini
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
```

**Kiểm tra CORS:**
```ini
# backend/.env
CORS_ORIGINS=http://localhost:3000
```

### 3. Rate Limiting Quá Nhanh

**Giảm tần suất tạo email:**
- Thay vì spam tạo email liên tục, đợi 2-3 giây giữa các requests
- Hoặc dùng mode "Random" để phân tán load

**Increase cooldown (nếu cần):**
```python
# backend/server.py
PROVIDER_COOLDOWN_SECONDS = 120  # Tăng từ 60s lên 120s
```

### 4. Tất Cả Providers Đều Bị Rate Limit

**Đợi 60 giây:**
- System tự động clear cooldown sau 60s
- Hoặc restart backend để reset cooldown

## 💡 Best Practices

### 1. Development
```bash
# Backend
cd D:\tool_mail\temp-mail\backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Frontend (terminal mới)
cd D:\tool_mail\temp-mail\frontend
yarn start
```

### 2. Production
```bash
# Backend (không dùng --reload)
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4

# Frontend (build static)
yarn build
# Serve static files với nginx hoặc serve
```

### 3. Database Backup
```bash
# Backup
mysqldump -u root -p190705 temp_mail > backup_$(date +%Y%m%d).sql

# Restore
mysql -u root -p190705 temp_mail < backup_20250111.sql
```

## 🎉 Kết Luận

**Ứng dụng của bạn đã chạy hoàn hảo trên Windows!**

✅ Backend: Running on port 8001 with MySQL
✅ Auto failover: Working (Mail.tm → Guerrilla)
✅ Background tasks: Moving expired emails to history
✅ All 4 providers: Ready to use

**Bước tiếp theo:**
1. Mở terminal mới và chạy frontend: `yarn start`
2. Truy cập: http://localhost:3000
3. Enjoy! 🚀

## 📚 Tài Liệu Tham Khảo

- **MYSQL_LOCAL_SETUP.md** - Chi tiết MySQL setup
- **MIGRATION_COMPLETE.md** - Verification report
- **README.md** - Overview và features
