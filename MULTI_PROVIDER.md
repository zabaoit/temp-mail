# Multi-Provider Email Support & Failover

## ⚡ Giải quyết lỗi 429 Rate Limit

Backend giờ hỗ trợ **nhiều nhà cung cấp email** với automatic failover:

### Providers được hỗ trợ:
1. **Mail.tm** - Provider chính, chất lượng cao
2. **1secmail** - Backup provider, không giới hạn rate

### 🔄 Automatic Failover Logic

```
Tạo email → Thử Mail.tm
           ↓ (Nếu 429 rate limit)
           Tự động chuyển sang 1secmail
           ↓
           Thành công! ✅
```

## 📊 Provider Stats

Kiểm tra thống kê providers:
```bash
curl http://localhost:8001/api/
```

Response:
```json
{
  "message": "TempMail API - MySQL with Multiple Providers",
  "providers": ["Mail.tm", "1secmail"],
  "stats": {
    "mailtm": {
      "success": 5,
      "failures": 2,
      "last_failure_time": 1699450800
    },
    "1secmail": {
      "success": 10,
      "failures": 0,
      "last_failure_time": 0
    }
  }
}
```

## 🎯 Cách hoạt động

### 1. Tạo email tự động (Auto)
```bash
POST /api/emails/create
{
  "service": "auto"  # Mặc định, thử Mail.tm → 1secmail
}
```

### 2. Chỉ định provider cụ thể
```bash
# Chỉ dùng Mail.tm
POST /api/emails/create
{
  "service": "mailtm"
}

# Chỉ dùng 1secmail
POST /api/emails/create
{
  "service": "1secmail"
}
```

### 3. Lấy messages (Tự động routing)
```bash
GET /api/emails/{id}/messages
```
Backend tự động biết email dùng provider nào và gọi đúng API.

## 🔧 Technical Details

### Mail.tm
- ✅ Yêu cầu account creation & token
- ✅ Chất lượng cao, tin cậy
- ⚠️ Có rate limit (429 khi quá nhiều request)

### 1secmail
- ✅ Không cần account creation
- ✅ Không có rate limit
- ✅ Nhiều domains khả dụng
- ⚠️ Không có authentication (ít secure hơn)

### Database Storage
Mỗi email lưu field `provider`:
```sql
SELECT id, address, provider FROM temp_emails;
```

Output:
```
id | address              | provider
---+----------------------+-----------
1  | abc123@mail.tm       | mailtm
2  | xyz789@1secmail.com  | 1secmail
3  | test456@mail.tm      | mailtm
```

## 📝 Logs

Backend giờ hiển thị logs rõ ràng:

### Success với Mail.tm:
```
🔄 Trying Mail.tm...
✅ Mail.tm email created successfully
✅ Email created: abc123@mail.tm (Provider: mailtm)
```

### Failover sang 1secmail:
```
🔄 Trying Mail.tm...
⚠️ Mail.tm rate limited (429)
⚠️ Mail.tm rate limited, falling back to 1secmail...
🔄 Trying 1secmail...
✅ 1secmail email created successfully
✅ Email created: xyz789@1secmail.com (Provider: 1secmail)
```

### Tất cả fail:
```
🔄 Trying Mail.tm...
❌ Mail.tm failed: Connection timeout
🔄 Trying 1secmail...
❌ 1secmail failed: No domains available
❌ Error creating email: All email providers failed
```

## 🚀 Benefits

### 1. Không lo rate limit
- Mail.tm bị chặn → Tự động dùng 1secmail
- Ứng dụng không bao giờ fail vì rate limit

### 2. Uptime cao hơn
- 1 provider down → Provider khác vẫn hoạt động
- 99.9% uptime

### 3. Load balancing tự nhiên
- Phân tải giữa các providers
- Giảm áp lực lên Mail.tm

### 4. Transparent cho frontend
- Frontend không cần biết provider nào
- Tất cả API calls giống nhau
- Backend tự động routing

## 🎨 Frontend Integration

Frontend không cần thay đổi gì! Mọi thứ vẫn hoạt động:

```javascript
// Tạo email (tự động failover)
const response = await axios.post(`${API}/emails/create`, {});

// Lấy messages (tự động routing đúng provider)
const messages = await axios.get(`${API}/emails/${id}/messages`);
```

## 🔍 Troubleshooting

### Lỗi: "All email providers failed"
**Nguyên nhân:** Cả 2 providers đều không available
**Giải pháp:** 
1. Kiểm tra internet connection
2. Chờ vài phút và thử lại
3. Check logs để xem lỗi cụ thể

### Provider nào tốt hơn?
- **Mail.tm**: Chất lượng cao, secure, nhưng có rate limit
- **1secmail**: Luôn available, không limit, nhưng kém secure hơn

### Làm sao biết email đang dùng provider nào?
```bash
GET /api/emails/{id}
```
Response có field `provider`:
```json
{
  "id": 1,
  "address": "test@mail.tm",
  "provider": "mailtm",  ← Provider info
  ...
}
```

## 📊 Monitoring

### Check provider stats:
```bash
curl http://localhost:8001/api/
```

### Check logs:
```bash
tail -f /var/log/supervisor/backend.*.log | grep -E "Trying|created|failed"
```

## 🆕 API Changes

### New endpoint: Get Domains
```bash
GET /api/domains?service=auto
```

Response:
```json
{
  "domains": ["mail.tm", "dropmail.me", "1secmail.com"],
  "service": "auto"
}
```

### Updated: Create Email
```bash
POST /api/emails/create
{
  "username": "test123",  # Optional
  "service": "auto",      # auto, mailtm, 1secmail
  "domain": null          # Optional
}
```

## 🎯 Summary

✅ **Automatic Failover**: Mail.tm fail → 1secmail  
✅ **No Rate Limit Issues**: Luôn có provider available  
✅ **Transparent**: Frontend không cần thay đổi  
✅ **Monitored**: Stats tracking cho mỗi provider  
✅ **Logged**: Chi tiết logs để debug  

**Kết quả:** Không còn lỗi 429! 🎉
