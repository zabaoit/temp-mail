# 📄 HƯỚNG DẪN SỬ DỤNG FILE .ENV - FRONTEND

## 📁 CÁC FILE .ENV

### 1. `.env` - **File chính**
```
Priority: Trung bình
Mục đích: Config mặc định cho mọi môi trường
Commit: ✅ CÓ (an toàn cho local config)
```

**Nội dung:**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
REACT_APP_NAME=TempMail
REACT_APP_VERSION=1.0.0
REACT_APP_ENV=local
REACT_APP_API_TIMEOUT=30000
REACT_APP_API_RETRY=3
REACT_APP_DEBUG=true
REACT_APP_ENABLE_LOGGING=true
REACT_APP_THEME=light
REACT_APP_LANG=vi
```

---

### 2. `.env.local` - **Local overrides**
```
Priority: CAO NHẤT (override tất cả)
Mục đích: Config riêng cho máy local
Commit: ✅ CÓ (port config)
```

**Nội dung:**
```env
PORT=7050
HOST=0.0.0.0
BROWSER=none
GENERATE_SOURCEMAP=false
FAST_REFRESH=true
CHOKIDAR_USEPOLLING=false
```

---

### 3. `.env.production` - **Production build**
```
Priority: Cao (khi build production)
Mục đích: Config cho production build
Commit: ✅ CÓ (template)
```

**Nội dung:**
```env
REACT_APP_BACKEND_URL=https://api.your-domain.com
REACT_APP_ENV=production
REACT_APP_DEBUG=false
REACT_APP_ENABLE_LOGGING=false
GENERATE_SOURCEMAP=false
```

---

### 4. `.env.example` - **Template**
```
Priority: N/A (chỉ là mẫu)
Mục đích: Template cho người mới
Commit: ✅ CÓ
```

---

## 🔄 THỨ TỰ ƯU TIÊN

React đọc file .env theo thứ tự sau (cao → thấp):

1. **`.env.local`** ← Cao nhất (override tất cả)
2. **`.env.production`** / **`.env.development`** (tùy NODE_ENV)
3. **`.env`** ← Mặc định

**Ví dụ:**
```
PORT trong .env = 3000
PORT trong .env.local = 7050
→ Kết quả: PORT = 7050 ✅
```

---

## 📊 BẢNG SO SÁNH

| File | Khi Nào Dùng | Commit Git | Priority |
|------|--------------|------------|----------|
| `.env` | Mọi môi trường | ✅ CÓ | Thấp |
| `.env.local` | Local dev | ✅ CÓ | **Cao nhất** |
| `.env.production` | Build production | ✅ CÓ | Cao |
| `.env.example` | Template | ✅ CÓ | N/A |

---

## 🎯 CÁCH SỬ DỤNG

### Scenario 1: Chạy Local Development
```bash
cd frontend
yarn start
# hoặc
PORT=7050 yarn start
```

**Files được đọc:**
1. `.env.local` (PORT=7050) ✅
2. `.env` (config mặc định)

**Kết quả:**
- Frontend chạy: http://localhost:7050
- Backend API: http://localhost:8001

---

### Scenario 2: Build Production
```bash
cd frontend
yarn build
```

**Files được đọc:**
1. `.env.production` (production config) ✅
2. `.env` (fallback)

**Kết quả:**
- Build folder: `frontend/build/`
- API URL: Theo `.env.production`
- Debug: Tắt
- Source map: Tắt

---

### Scenario 3: Custom Backend URL
```bash
# Tạm thời override
REACT_APP_BACKEND_URL=http://192.168.1.100:8001 yarn start

# Hoặc thêm vào .env.local
echo "REACT_APP_BACKEND_URL=http://192.168.1.100:8001" >> .env.local
yarn start
```

---

## 🔧 CÁC BIẾN MÔI TRƯỜNG

### Backend Configuration
```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001
```

### App Information
```env
REACT_APP_NAME=TempMail
REACT_APP_VERSION=1.0.0
REACT_APP_ENV=local
```

### API Settings
```env
REACT_APP_API_TIMEOUT=30000    # 30 seconds
REACT_APP_API_RETRY=3          # 3 attempts
```

### Debug & Logging
```env
REACT_APP_DEBUG=true           # Enable debug mode
REACT_APP_ENABLE_LOGGING=true  # Enable console logs
```

### UI Settings
```env
REACT_APP_THEME=light          # light | dark
REACT_APP_LANG=vi              # vi | en
```

### Development Settings
```env
PORT=7050                      # Frontend port
HOST=0.0.0.0                   # Listen on all interfaces
BROWSER=none                   # Don't auto-open browser
GENERATE_SOURCEMAP=false       # Disable source maps
FAST_REFRESH=true              # Enable fast refresh
```

---

## 🔍 CÁCH SỬ DỤNG TRONG CODE

### JavaScript/JSX:
```javascript
// Lấy backend URL
const backendUrl = process.env.REACT_APP_BACKEND_URL;

// Hoặc
import.meta.env.REACT_APP_BACKEND_URL

// Ví dụ:
const apiUrl = `${process.env.REACT_APP_BACKEND_URL}/api/emails`;

fetch(apiUrl)
  .then(res => res.json())
  .then(data => console.log(data));
```

### TypeScript:
```typescript
// Định nghĩa types (tùy chọn)
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_BACKEND_URL: string;
      REACT_APP_NAME: string;
      REACT_APP_VERSION: string;
    }
  }
}

// Sử dụng
const apiUrl: string = process.env.REACT_APP_BACKEND_URL;
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Prefix `REACT_APP_`
```
✅ ĐÚNG: REACT_APP_BACKEND_URL
❌ SAI:  BACKEND_URL (không được đọc)
```

**Lý do:** Create React App chỉ expose biến bắt đầu với `REACT_APP_`

### 2. Restart Server
```bash
# Sau khi thay đổi .env, PHẢI restart
Ctrl+C
yarn start
```

### 3. Build Time vs Runtime
```
.env được inject lúc BUILD TIME
→ Không thể thay đổi sau khi build
→ Muốn thay đổi: phải build lại
```

### 4. Không Lưu Secrets
```
❌ KHÔNG lưu API keys, passwords trong .env
✅ Chỉ lưu config công khai (URL, port, flags)
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: Biến môi trường không đọc được
**Nguyên nhân:**
- Quên prefix `REACT_APP_`
- Chưa restart server

**Giải pháp:**
```bash
# Kiểm tra tên biến
echo $REACT_APP_BACKEND_URL

# Restart server
Ctrl+C
yarn start
```

### Lỗi: .env.local không override
**Nguyên nhân:**
- Tên biến khác nhau
- Có khoảng trắng thừa

**Giải pháp:**
```bash
# Kiểm tra nội dung
cat .env.local

# Đảm bảo không có khoảng trắng
PORT=7050  ✅
PORT = 7050  ❌
```

### Lỗi: Backend không connect được
**Kiểm tra:**
```bash
# 1. Backend có chạy không?
curl http://localhost:8001/health

# 2. .env có đúng URL không?
cat frontend/.env | grep BACKEND_URL

# 3. CORS có được bật không?
# Xem backend/.env → CORS_ORIGINS=*
```

---

## 📚 TÀI LIỆU THAM KHẢO

- [Create React App - Env Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [dotenv Documentation](https://github.com/motdotla/dotenv)

---

## ✅ CHECKLIST

Trước khi chạy app:
- [ ] File `.env` đã có
- [ ] File `.env.local` đã có PORT=7050
- [ ] `REACT_APP_BACKEND_URL` đúng (localhost:8001)
- [ ] Backend đang chạy
- [ ] Đã restart frontend sau khi sửa .env

---

**🎯 Xong! Giờ frontend sẽ chạy port 7050 khi bạn pull code về local!**
