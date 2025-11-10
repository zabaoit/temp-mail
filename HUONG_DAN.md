# TempMail - Trình Tạo Email Tạm Thời

Ứng dụng web full-stack để tạo địa chỉ email tạm thời với hỗ trợ nhiều nhà cung cấp dịch vụ. Được xây dựng với backend FastAPI (Python), frontend React và cơ sở dữ liệu MySQL.

## 🌟 Tính Năng

- ✉️ **Tự động tạo email tạm** - Tự động tạo email mới khi bạn mở ứng dụng
- ⏰ **Hết hạn sau 10 phút** - Email tự động hết hạn sau 10 phút
- 🔄 **Tự động làm mới** - Tự động tạo email mới khi email hiện tại hết hạn
- 📧 **Nhiều nhà cung cấp**: Mail.tm, 1secmail, Mail.gw, Guerrilla Mail
- 💾 **Lưu email** - Lưu các email quan trọng để xem lại sau
- 📜 **Lịch sử email** - Xem email đã hết hạn với đầy đủ tin nhắn
- 🎨 **Giao diện hiện đại** - Theme tối đẹp mắt với hiệu ứng mượt mà
- 🔐 **Xem nội dung HTML/Text** - Hỗ trợ đầy đủ email HTML và văn bản thuần

## 🛠️ Công Nghệ Sử Dụng

**Backend:**
- FastAPI (Python 3.9+)
- MySQL 8.0+ với SQLAlchemy ORM
- httpx cho async API calls
- Background tasks cho tự động hết hạn email

**Frontend:**
- React 18
- Tailwind CSS
- Axios cho API calls
- Lucide React icons
- Sonner cho toast notifications

## 📋 Yêu Cầu Hệ Thống

Trước khi bắt đầu, đảm bảo bạn đã cài đặt:

1. **Python 3.9 hoặc cao hơn**
   - Tải từ: https://www.python.org/downloads/
   - Kiểm tra: `python --version` hoặc `python3 --version`

2. **Node.js 18 hoặc cao hơn & Yarn**
   - Tải Node.js từ: https://nodejs.org/
   - Cài Yarn: `npm install -g yarn`
   - Kiểm tra: `node --version` && `yarn --version`

3. **MySQL 8.0 hoặc cao hơn**
   - Tải từ: https://dev.mysql.com/downloads/mysql/
   - Hoặc dùng package manager:
     - macOS: `brew install mysql`
     - Ubuntu/Debian: `sudo apt install mysql-server`
     - Windows: Tải installer từ trang web MySQL

## 🚀 Hướng Dẫn Cài Đặt Nhanh

### Bước 1: Cấu Hình MySQL

1. Khởi động dịch vụ MySQL:
```bash
# macOS
brew services start mysql

# Ubuntu/Debian
sudo systemctl start mysql

# Windows
# Khởi động MySQL từ Services hoặc MySQL Workbench
```

2. Tạo database:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Nếu dùng credentials khác, cập nhật file backend/.env
-- Credentials mặc định: root / 190705
```

### Bước 2: Cài Đặt Backend

1. Chuyển đến thư mục backend:
```bash
cd backend
```

2. Tạo và kích hoạt virtual environment:
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Kiểm tra biến môi trường trong file `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

5. Khởi tạo database:
```bash
python init_db.py
```

6. Chạy backend server:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Backend sẽ chạy tại: **http://localhost:8001**  
API documentation: **http://localhost:8001/docs**

### Bước 3: Cài Đặt Frontend

1. Mở terminal mới và chuyển đến thư mục frontend:
```bash
cd frontend
```

2. Cài đặt dependencies:
```bash
yarn install
```

3. Kiểm tra biến môi trường trong file `.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=3000
```

4. Chạy frontend development server:
```bash
yarn start
```

Frontend sẽ chạy tại: **http://localhost:3000**

### Bước 4: Sử Dụng Ứng Dụng

1. Mở trình duyệt và truy cập: **http://localhost:3000**
2. Email tạm sẽ được tạo tự động
3. Copy địa chỉ email và sử dụng để test/đăng ký
4. Nhấn làm mới để kiểm tra tin nhắn mới
5. Click vào tin nhắn để xem nội dung HTML/text

## 📁 Cấu Trúc Project

```
/app/
├── backend/
│   ├── server.py              # Ứng dụng FastAPI chính
│   ├── database.py            # Kết nối MySQL & session
│   ├── models.py              # SQLAlchemy models (TempEmail, EmailHistory, SavedEmail)
│   ├── background_tasks.py   # Background task tự động hết hạn
│   ├── init_db.py            # Script khởi tạo database
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Cấu hình backend
├── frontend/
│   ├── src/
│   │   ├── App.js           # Component React chính
│   │   ├── App.css          # Styles
│   │   └── index.js         # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   └── .env                 # Cấu hình frontend
├── README.md                # Tài liệu tiếng Anh
└── HUONG_DAN.md            # Tài liệu này (tiếng Việt)
```

## 🗄️ Cấu Trúc Database

### Bảng: `temp_emails`
```sql
CREATE TABLE temp_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
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

### Bảng: `email_history`
```sql
CREATE TABLE email_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    token TEXT,
    account_id VARCHAR(255),
    created_at DATETIME,
    expired_at DATETIME NOT NULL,
    message_count INT DEFAULT 0,
    provider VARCHAR(50),
    username VARCHAR(100),
    domain VARCHAR(100)
);
```

### Bảng: `saved_emails`
```sql
CREATE TABLE saved_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_id INT NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    from_address VARCHAR(255),
    from_name VARCHAR(255),
    subject TEXT,
    html_content LONGTEXT,
    text_content LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API Endpoints

### Email Hiện Tại
- `POST /api/emails/create` - Tạo email tạm mới
- `GET /api/emails` - Danh sách email đang hoạt động
- `GET /api/emails/{id}` - Chi tiết email
- `GET /api/emails/{id}/messages` - Lấy tin nhắn cho email
- `POST /api/emails/{id}/refresh` - Làm mới tin nhắn
- `DELETE /api/emails/{id}` - Xóa email
- `POST /api/emails/{id}/extend-time` - Gia hạn email thêm 10 phút

### Lịch Sử
- `GET /api/emails/history/list` - Danh sách email đã hết hạn
- `GET /api/emails/history/{id}/messages` - Lấy tin nhắn từ lịch sử
- `DELETE /api/emails/history/delete` - Xóa email lịch sử (chọn lọc hoặc tất cả)

### Email Đã Lưu
- `POST /api/emails/{id}/messages/{msg_id}/save` - Lưu một tin nhắn
- `GET /api/emails/saved/list` - Danh sách email đã lưu
- `GET /api/emails/saved/{id}` - Chi tiết email đã lưu
- `DELETE /api/emails/saved/delete` - Xóa email đã lưu

### Domains
- `GET /api/domains?service={service}` - Lấy domains có sẵn cho dịch vụ

## 🐛 Xử Lý Lỗi

### Backend không khởi động

**Lỗi: "Can't connect to MySQL server"**
```bash
# Kiểm tra MySQL có đang chạy không
mysql -u root -p

# Kiểm tra credentials trong backend/.env
# Kiểm tra database có tồn tại không
mysql -u root -p -e "SHOW DATABASES;"
```

**Lỗi: "No module named 'httpx'"**
```bash
# Đảm bảo virtual environment đã được kích hoạt
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Cài lại dependencies
pip install -r requirements.txt
```

### Frontend không khởi động

**Lỗi: "Cannot find module"**
```bash
# Xóa node_modules và cài lại
rm -rf node_modules yarn.lock
yarn install
```

**Lỗi: "Port 3000 already in use"**
```bash
# Đổi port trong frontend/.env
PORT=7050
```

### Vấn đề Database

**Reset database:**
```bash
cd backend
python init_db.py --reset
# Gõ 'yes' để xác nhận
```

**Reset database thủ công:**
```sql
mysql -u root -p

DROP DATABASE temp_mail;
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE temp_mail;
```

## 🔧 Mẹo Phát Triển

### Hot Reload
- Backend: Tự động reload khi bạn chỉnh sửa file Python (uvicorn --reload)
- Frontend: Tự động reload khi bạn chỉnh sửa file React

### Xem Logs
```bash
# Backend logs (nếu chạy foreground)
# Logs hiện trong terminal

# Kiểm tra background task logs
# Logs hiện trong terminal backend với timestamp
```

### Test API
- Dùng Swagger UI tích hợp sẵn: http://localhost:8001/docs
- Hoặc dùng curl:
```bash
# Tạo email
curl -X POST http://localhost:8001/api/emails/create

# Lấy danh sách emails
curl http://localhost:8001/api/emails
```

## 🎯 Giải Thích Các Tính Năng

### Tự Động Tạo Email Lần Đầu
Khi bạn mở ứng dụng lần đầu, nó sẽ tự động tạo một email tạm mà không cần bạn click nút nào.

### Bộ Đếm Thời Gian 10 Phút
Mỗi email có thời hạn 10 phút. Bộ đếm thời gian hiển thị ở trên cùng và đếm ngược theo thời gian thực.

### Nút Gia Hạn Thời Gian
Click "Làm mới 10 phút" để reset bộ đếm về 10 phút (không cộng dồn - luôn reset về 10 phút).

### Tự Động Tạo Email Khi Hết Hạn
Khi bộ đếm về 0, email cũ sẽ tự động chuyển vào lịch sử và một email mới được tạo.

### Lịch Sử Email
Xem tất cả email đã hết hạn trong tab "Lịch sử". Bạn vẫn có thể xem tin nhắn từ email đã hết hạn. Dùng checkbox để chọn và xóa lịch sử.

### Lưu Email Quan Trọng
Click nút "Lưu" khi xem tin nhắn để lưu nó vĩnh viễn. Email đã lưu hiện trong tab "Mail đã lưu".

## 💡 Các Lưu Ý Quan Trọng

### Credentials MySQL
- Mặc định: `root / 190705`
- Nếu bạn dùng credentials khác, cập nhật file `backend/.env`

### Port Configuration
- Backend: `8001` (có thể đổi trong uvicorn command)
- Frontend: `3000` (có thể đổi trong `frontend/.env`)

### Multiple Providers
Ứng dụng hỗ trợ nhiều nhà cung cấp email:
- **Mail.tm**: Provider chính, đáng tin cậy
- **1secmail**: Backup provider, nhanh
- **Mail.gw**: Alternative provider
- **Guerrilla Mail**: Không cần đăng ký, dễ dùng

Ứng dụng sẽ tự động chọn provider hoạt động tốt nhất.

### Background Tasks
Backend tự động chạy background task để:
- Kiểm tra email hết hạn mỗi 30 giây
- Tự động chuyển email hết hạn vào lịch sử
- Tự động tạo email mới nếu không còn email active

## 🔐 Bảo Mật

- Email tạm không yêu cầu xác thực cá nhân
- Không lưu trữ thông tin nhạy cảm
- Tất cả email tự động hết hạn sau 10 phút
- Lịch sử có thể xóa bất cứ lúc nào

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra file README.md và HUONG_DAN.md này
2. Xác minh đã cài đặt đầy đủ yêu cầu hệ thống
3. Kiểm tra phần xử lý lỗi
4. Xem backend logs để biết thông báo lỗi chi tiết

## 📄 License

Project này được cung cấp as-is cho mục đích cá nhân và giáo dục.

## 🎨 Giao Diện

Ứng dụng có giao diện hiện đại với:
- **Dark theme** mặc định (có thể chuyển sang light theme)
- **Responsive design** hoạt động trên mọi thiết bị
- **Smooth animations** cho trải nghiệm người dùng tốt hơn
- **Toast notifications** cho feedback tức thời
- **Modern card design** với shadows và hover effects

## 🚀 Tính Năng Nâng Cao

### Chọn Dịch Vụ Email
- Chọn "Tự động" để hệ thống tự chọn provider tốt nhất
- Hoặc chọn provider cụ thể: Mail.tm, 1secmail, Mail.gw, Guerrilla Mail

### Chọn Domain
- Mỗi provider có nhiều domains khác nhau
- Chọn domain yêu thích của bạn từ dropdown

### Làm Mới Tin Nhắn
- Auto-refresh: Tự động kiểm tra tin nhắn mới mỗi 10 giây
- Manual refresh: Click nút "Làm mới" bất cứ lúc nào

### Xem Chi Tiết Tin Nhắn
- Xem nội dung HTML (rendered)
- Xem nội dung text (plain text)
- Thông tin người gửi, tiêu đề, thời gian

---

**Được tạo với ❤️ bằng FastAPI + React + MySQL**
