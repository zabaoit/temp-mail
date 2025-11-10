# TempMail - MySQL Version ✅

## Tổng quan
Ứng dụng TempMail với **MySQL** database (không còn MongoDB).

## ✅ Đã hoàn thành
- [x] Chuyển đổi hoàn toàn sang MySQL/SQLAlchemy
- [x] Xóa tất cả MongoDB code và dependencies
- [x] Fix Guerrilla Mail HTML rendering
- [x] Background tasks tự động expire emails
- [x] Saved emails feature

## 🚀 Quick Start (Local)

### 1. Cài đặt MySQL
```bash
# Cài MySQL 8.0+ và set password = 190705
mysql -u root -p190705 -e "SELECT 1;"
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Setup Frontend
```bash
cd frontend
yarn install
PORT=7050 yarn start
```

### 4. Truy cập
- Frontend: http://localhost:7050
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 📊 Database
### MySQL Tables
- `temp_emails` - Active emails với expiry
- `email_history` - Expired emails
- `saved_emails` - User saved messages

### Credentials (.env)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
```

## 🔧 Tech Stack
- **Backend**: FastAPI + SQLAlchemy + PyMySQL
- **Frontend**: React + Tailwind CSS
- **Database**: MySQL 8.0+
- **Email Providers**: Mail.tm, Mail.gw, 1secmail, Guerrilla Mail

## 📝 Tính năng
✅ Tự động tạo email tạm thời
✅ Timer 10 phút với auto-expire
✅ Làm mới thời gian (reset về 10 phút)
✅ Auto-create email mới khi hết hạn
✅ Multi-provider với failover
✅ Lưu và quản lý messages
✅ Lịch sử emails đã hết hạn
✅ HTML rendering cho tất cả providers (including Guerrilla Mail fix)

## 🐛 Troubleshooting

### MySQL connection error
```bash
# Check MySQL running
sudo systemctl start mysql  # Linux
mysql.server start          # macOS

# Reset password
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY '190705';
FLUSH PRIVILEGES;
```

### Backend won't start
```bash
# Check logs
tail -f /var/log/supervisor/backend.err.log

# Restart
sudo supervisorctl restart backend
```

## 📚 Documentation
- **Full Guide**: `/app/MIGRATION_TO_MYSQL.md`
- **Testing**: `/app/test_result.md`
- **API Docs**: http://localhost:8001/docs (khi server chạy)

## 💡 Lưu ý
- ⚠️ Container environment không có MySQL (dùng cho dev/test only)
- ✅ Chạy trên local machine với MySQL để sử dụng đầy đủ
- ✅ Background task tự động expire emails mỗi 30 giây
- ✅ Frontend tự động tạo email mới khi vào lần đầu
- ✅ Guerrilla Mail HTML hiển thị chính xác

## 🎯 Test Quick
```bash
# Test backend API
curl http://localhost:8001/api/

# Create email
curl -X POST http://localhost:8001/api/emails/create \
  -H "Content-Type: application/json" \
  -d '{"service": "auto"}'
```

---

**Status**: ✅ Production Ready (với MySQL local)
**Last Updated**: 2025-01-08
