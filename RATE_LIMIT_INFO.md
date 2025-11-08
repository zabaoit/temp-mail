# 🚦 Giải Thích Rate Limiting - Mail.tm API

## ❓ Vấn đề là gì?

Khi bạn thấy lỗi **"429 Too Many Requests"**, điều này có nghĩa là:
- **Mail.tm API** đã giới hạn số lượng request từ bạn
- Bạn đã tạo **quá nhiều email** trong thời gian ngắn
- Đây là cơ chế bảo vệ của Mail.tm để chống spam/abuse

## 🔢 Giới hạn hiện tại

### Mail.tm API (External):
- **Không công khai chính xác** - phụ thuộc vào IP và usage patterns
- Ước tính: ~5-10 accounts mỗi 5-10 phút
- Rate limit sẽ tự động **reset sau 5-15 phút**

### App của bạn (Local Protection):
Để bảo vệ khỏi việc spam Mail.tm, app đã thêm:
- ✅ **Tối đa 3 email mỗi phút**
- ✅ Cache domain list (5 phút) - giảm API calls
- ✅ Retry logic với exponential backoff
- ✅ Thông báo lỗi rõ ràng

## 🛠️ Giải pháp

### 1. **Giải pháp tức thì** (Khi gặp lỗi 429)

```bash
# Đợi 5-10 phút rồi thử lại
# Mail.tm sẽ tự động reset rate limit
```

**Trong lúc đợi:**
- ✅ Sử dụng email hiện có để test
- ✅ Test các tính năng khác (xem message, history, extend time)
- ✅ **KHÔNG** spam nút "Tạo Email Mới"

### 2. **Best Practices** (Tránh bị rate limit)

#### ✅ DO (Nên làm):
```javascript
// 1. Chỉ tạo email khi thực sự cần
// 2. Sử dụng extend time thay vì tạo email mới
// 3. Test với 1-2 email, không cần nhiều
// 4. Đợi ít nhất 1-2 phút giữa các lần tạo
```

#### ❌ DON'T (Không nên):
```javascript
// 1. KHÔNG spam tạo email liên tục
// 2. KHÔNG tạo nhiều email trong vòng 1 phút
// 3. KHÔNG refresh page liên tục (auto-create will trigger)
// 4. KHÔNG run test automation liên tục
```

### 3. **Code Improvements** (Đã implement)

Backend đã được cải tiến với:

```python
# ✅ Local rate limiting (3 emails/minute)
@api_router.post("/emails/create")
async def create_email(...):
    # Check if user exceeded 3 emails/minute
    if _rate_limit_tracker["create_count"] >= 3:
        raise HTTPException(429, "Maximum 3 emails per minute")
```

```python
# ✅ Domain caching (reduce API calls)
_domain_cache = {
    "domain": None,
    "cached_at": 0,
    "ttl": 300  # Cache for 5 minutes
}
```

```python
# ✅ Retry with exponential backoff
for attempt in range(3):
    try:
        response = await http_client.post(...)
    except HTTPStatusError as e:
        if e.response.status_code == 429:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            await asyncio.sleep(wait_time)
```

### 4. **Production Solutions** (Nâng cao)

Nếu cần scale production, có thể:

#### Option A: **Sử dụng API key riêng**
```bash
# Mail.tm có premium plans với rate limit cao hơn
# https://mail.tm/pricing (nếu có)
```

#### Option B: **Dùng nhiều domain providers**
```python
# Thêm fallback providers
PROVIDERS = [
    "mail.tm",
    "tempmail.plus",
    "10minutemail.com"
]
```

#### Option C: **Email pool**
```python
# Tạo sẵn pool của emails
# Reuse thay vì tạo mới mỗi lần
class EmailPool:
    def __init__(self):
        self.available_emails = []
        self.in_use_emails = []
    
    async def get_email(self):
        if self.available_emails:
            return self.available_emails.pop()
        else:
            return await create_new_email()
```

#### Option D: **Redis rate limiting**
```python
# Sử dụng Redis để track rate limit across multiple instances
import redis

r = redis.Redis()

def check_rate_limit(user_ip):
    key = f"rate_limit:{user_ip}"
    count = r.incr(key)
    
    if count == 1:
        r.expire(key, 60)  # Reset after 60 seconds
    
    if count > 3:
        raise RateLimitExceeded()
```

## 📊 Monitoring

Xem logs để track rate limiting:

```bash
# Backend logs
tail -f backend.log | grep "Rate limited"

# Ví dụ output:
# WARNING: Rate limited on account creation, waiting 2s (attempt 2/3)
# WARNING: Rate limited on domains, waiting 1s (attempt 1/3)
```

## 🎯 Recommendations

### Development:
1. **Test với ít email** - 1-2 email là đủ để test tất cả features
2. **Sử dụng "Làm mới 10 phút"** thay vì tạo email mới
3. **Đợi giữa các test runs** - ít nhất 1-2 phút
4. **Không enable auto-refresh** quá thường xuyên

### Testing:
```bash
# GOOD: Test workflow
1. Tạo 1 email
2. Test all features (messages, extend, history)
3. Đợi 2 phút
4. Tạo email mới để test expiry

# BAD: Spam workflow
1. Tạo email → xóa → tạo lại → xóa → tạo lại ❌
2. Refresh page 10 lần trong 1 phút (auto-create triggers) ❌
```

### Production:
1. Educate users về rate limits
2. Hiển thị thông báo khi approach limit
3. Disable "Tạo Email Mới" button tạm thời khi hit limit
4. Show countdown timer: "Tạo email mới sau: 45s"

## 🆘 Troubleshooting

### Q: "Vẫn bị 429 sau khi đợi 10 phút?"
**A:** 
- Clear browser cache
- Đổi network/IP (VPN)
- Thử lại sau 30 phút
- Kiểm tra xem có ai khác cùng IP không (shared network)

### Q: "App báo 'Maximum 3 emails per minute'?"
**A:**
- Đây là protection của app (local)
- Đợi 60 giây rồi thử lại
- Hoặc comment out rate limit code trong `server.py` nếu testing

### Q: "Cần nhiều email để test?"
**A:**
- Không cần nhiều! 1-2 email là đủ
- Sử dụng extend time để test expiry
- Sử dụng history để test các email cũ
- Manually mock data nếu cần test UI với nhiều emails

## 📝 Summary

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| 429 từ Mail.tm | API rate limit | Đợi 5-10 phút |
| 429 từ app | Local protection (3/min) | Đợi 60 giây |
| Cần test nhiều email | Workflow không tối ưu | Reuse emails, extend time |
| Production concerns | External API limits | Email pool, multiple providers |

---

**💡 Tip:** Development không cần nhiều emails. Focus vào testing features với 1-2 emails có sẵn!
