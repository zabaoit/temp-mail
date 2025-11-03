# 🎯 HƯỚNG DẪN PUSH CODE LÊN GITHUB VÀ PULL VỀ LOCAL

## ✅ Các File Đã Được Thêm Vào Git

### Environment Files:
- ✅ `backend/.env` - MySQL config cho local
- ✅ `frontend/.env` - Backend URL cho local (http://localhost:8001)  
- ✅ `frontend/.env.local` - Port 7050 config
- ✅ `frontend/.env.example` - Template file

### Icons & Assets:
- ✅ `frontend/public/favicon.ico`
- ✅ `frontend/public/logo192.png`
- ✅ `frontend/public/logo512.png`
- ✅ `frontend/public/mail-icon.svg`
- ✅ `frontend/public/manifest.json`

### Documentation:
- ✅ `CHECKLIST.md` - Checklist files cần có
- ✅ `QUICK_START.md` - Hướng dẫn nhanh
- ✅ `HUONG_DAN_LOCAL.md` - Chi tiết tiếng Việt
- ✅ `.gitignore` - Đã cập nhật để include .env files

---

## 📤 BƯỚC 1: PUSH CODE LÊN GITHUB

### Từ Terminal VSCode của bạn:

```bash
cd /d/tool_mail/temp-mail

# Bước 1: Resolve merge conflict (nếu còn)
git add frontend/public/index.html
git commit -m "Resolved merge conflict - keep local changes"

# Bước 2: Add tất cả files mới
git add .

# Bước 3: Commit
git commit -m "✨ Add favicon, port 7050 config, and local setup files

- Added favicon.ico and logo icons (192px, 512px)
- Configured frontend to run on port 7050
- Updated .env files for local development
- Added comprehensive documentation (CHECKLIST.md, QUICK_START.md)
- Updated .gitignore to include necessary .env files
"

# Bước 4: Push lên GitHub
git push origin main
```

⚠️ **Nếu gặp lỗi merge conflict**, chạy:
```bash
git merge --abort
git pull --rebase origin main
# Resolve conflicts nếu có
git add .
git rebase --continue
git push origin main
```

---

## 📥 BƯỚC 2: PULL CODE VỀ MÁY KHÁC

### Trên máy local mới (hoặc máy khác):

```bash
# Clone repository
git clone https://github.com/kha0305/temp-mail.git
cd temp-mail

# Kiểm tra files .env đã có chưa
ls -la backend/.env
ls -la frontend/.env
ls -la frontend/.env.local
```

### ✅ Nếu files .env đã có (SAU KHI PUSH):
```bash
# Không cần làm gì thêm!
# Chỉ cần chạy app:
bash start_app.sh
```

### ⚠️ Nếu thiếu files .env (TRƯỚC KHI PUSH):
Tạo thủ công theo CHECKLIST.md

---

## 🔍 KIỂM TRA SAU KHI PULL

### 1. Kiểm tra Backend .env:
```bash
cat backend/.env
```

**Cần thấy:**
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tempmail_user
MYSQL_PASSWORD=tempmail_password_123
MYSQL_DATABASE=tempmail_db
TEMPMAIL_API_URL=https://api.mail.tm
```

### 2. Kiểm tra Frontend .env:
```bash
cat frontend/.env
```

**Cần thấy:**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
```

### 3. Kiểm tra Frontend .env.local:
```bash
cat frontend/.env.local
```

**Cần thấy:**
```env
PORT=7050
```

### 4. Kiểm tra Icons:
```bash
ls -lh frontend/public/*.{ico,png,svg,json}
```

**Cần thấy:**
```
favicon.ico
logo192.png
logo512.png
mail-icon.svg
manifest.json
```

---

## 🚀 BƯỚC 3: CHẠY ỨNG DỤNG

### Cài đặt MySQL (nếu chưa có):
```bash
# Ubuntu/Debian
sudo apt install mysql-server
sudo systemctl start mysql

# macOS
brew install mysql
brew services start mysql
```

### Tạo Database:
```bash
sudo mysql

CREATE DATABASE tempmail_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tempmail_user'@'localhost' IDENTIFIED BY 'tempmail_password_123';
GRANT ALL PRIVILEGES ON tempmail_db.* TO 'tempmail_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Chạy App:
```bash
bash start_app.sh
```

**Lần đầu tiên:**
1. Chọn `1` - Khởi tạo Database
2. Chọn `4` - Chạy Backend + Frontend

**Các lần sau:**
- Chọn `4` - Chạy toàn bộ

### Truy cập:
- Frontend: http://localhost:7050 ✅
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

---

## 🎯 TÓM TẮT FLOW

### Máy Development (Hiện tại):
```bash
cd /d/tool_mail/temp-mail
git add .
git commit -m "Add favicon and local config"
git push origin main
```

### Máy Local Khác:
```bash
git clone https://github.com/kha0305/temp-mail.git
cd temp-mail

# Kiểm tra files
cat backend/.env
cat frontend/.env
cat frontend/.env.local

# Setup MySQL
# ... (tạo database)

# Chạy
bash start_app.sh
```

---

## ⚡ TROUBLESHOOTING

### Lỗi: Files .env không có sau khi pull

**Nguyên nhân**: File .gitignore đang ignore .env

**Giải pháp**: 
```bash
# Force add files .env
git add -f backend/.env frontend/.env frontend/.env.local
git commit -m "Add .env files for local development"
git push origin main
```

### Lỗi: Merge conflict khi push

```bash
git status
git add <conflicted-files>
git commit -m "Resolved conflicts"
git push origin main
```

### Lỗi: "Can't connect to MySQL"

**Kiểm tra**:
```bash
# MySQL có chạy không?
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Test connection
mysql -u tempmail_user -p
# Password: tempmail_password_123
```

---

## 📋 CHECKLIST TRƯỚC KHI PUSH

- [ ] Đã resolve tất cả merge conflicts
- [ ] File `.env` đã được add vào git
- [ ] File `.gitignore` đã được cập nhật
- [ ] Đã test commit message
- [ ] Đã kiểm tra `git status` không có files lạ

---

## 📋 CHECKLIST SAU KHI PULL

- [ ] Files `.env` đã có đầy đủ
- [ ] MySQL đã được cài đặt và chạy
- [ ] Database `tempmail_db` đã được tạo
- [ ] Port 7050 và 8001 không bị chiếm
- [ ] `bash start_app.sh` chạy thành công

---

## 💡 LƯU Ý QUAN TRỌNG

1. **Files .env KHÔNG chứa secrets thật**: 
   - Chỉ có config cho localhost
   - An toàn để commit vào git

2. **Production deployment**:
   - Sử dụng environment variables của platform
   - Không dùng files .env trong repo

3. **Mỗi lần pull code mới**:
   - Kiểm tra files .env có thay đổi không
   - Update MySQL credentials nếu cần

---

Chúc bạn pull code thành công! 🎉
