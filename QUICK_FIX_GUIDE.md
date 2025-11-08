# 🚑 QUICK FIX GUIDE - Dual SMTP + Integer ID

## ❌ Vấn đề hiện tại

### 1. SMTPLabs Keys không được load
**Logs hiện tại:**
```
⚠️  SMTPLabs API keys not configured, cannot use as fallback
ERROR: All email providers unavailable
```

**Nguyên nhân:** Server đang chạy TỪ TRƯỚC khi .env được cập nhật.

---

### 2. Frontend Error: `emailId.trim is not a function`
**Nguyên nhân:** ID giờ là `number`, không phải `string`, nên không có method `.trim()`.

---

## ✅ GIẢI PHÁP

### Bước 1: Restart Backend (BẮT BUỘC)

**Windows PowerShell:**
```powershell
# Trong terminal đang chạy backend, nhấn CTRL+C để dừng

# Sau đó chạy lại:
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Xác nhận thành công khi thấy logs:**
```
✅ Loaded SMTPLABS_API_KEY_1
✅ Loaded SMTPLABS_API_KEY_2
📧 SMTPLabs: 2 API key(s) loaded
```

---

### Bước 2: Frontend đã được fix

✅ **Đã sửa:** Removed `.trim()` check trong `refreshMessages()`
```javascript
// CŨ (LỖI):
if (!emailId || emailId.trim() === '') {

// MỚI (ĐÚNG):
if (!emailId) {
```

Frontend sẽ tự động reload khi bạn save, không cần restart.

---

### Bước 3: Reset Database (nếu chưa làm)

**Nếu bạn muốn dùng Integer IDs:**
```powershell
cd backend
python init_db.py --reset
# Nhập "yes" khi được hỏi
```

**Lưu ý:** Lệnh này sẽ XÓA tất cả emails và history hiện tại!

---

## 🧪 TESTING

### Test 1: Verify SMTP Keys Loaded
```bash
# Sau khi restart backend, kiểm tra logs đầu tiên:
# Phải thấy:
✅ Loaded SMTPLABS_API_KEY_1
✅ Loaded SMTPLABS_API_KEY_2
📧 SMTPLabs: 2 API key(s) loaded
```

### Test 2: Create Email khi Mail.tm rate limited
```bash
# Khi Mail.tm bị rate limit, SMTPLabs sẽ tự động được dùng:
🔄 Attempting to create email via Mail.tm...
❌ Mail.tm failed: Rate limit exceeded
🔄 Falling back to SMTPLabs key1... (attempt 1/2)
✅ SMTPLabs account created with key1: test@test.smtp.dev
```

### Test 3: Frontend không còn error
- Mở frontend: http://localhost:7050
- Click "Làm mới" → Không còn error `emailId.trim is not a function`
- Tạo email mới → ID hiển thị là số (1, 2, 3...)

---

## 📊 EXPECTED BEHAVIOR

### Khi Mail.tm hoạt động bình thường:
```
✅ Mail.tm account created
```

### Khi Mail.tm bị rate limited:
```
❌ Mail.tm failed: Rate limit exceeded
🔄 Falling back to SMTPLabs key1...
✅ SMTPLabs account created with key1
```

### Khi SMTPLabs key1 cũng bị rate limited:
```
❌ Mail.tm failed: Rate limit exceeded
🔄 Falling back to SMTPLabs key1... (attempt 1/2)
❌ SMTPLabs key1 failed: Rate limit exceeded
🔄 Falling back to SMTPLabs key2... (attempt 2/2)
✅ SMTPLabs account created with key2
```

---

## ⚠️ TROUBLESHOOTING

### Issue: Vẫn thấy "SMTPLabs API keys not configured"
**Giải pháp:**
1. Kiểm tra file `backend/.env`:
   ```env
   SMTPLABS_API_KEY_1=smtplabs_DEkL4DqWAxMR76XBkN7n3G2yVPeoqusnG8qukhEBXN3meASm
   SMTPLABS_API_KEY_2=smtplabs_DEkL4DqWAxMR76XBkN7n3G2yVPeoqusnG8qukhEBXN3meASm
   ```
2. Đảm bảo không có spaces thừa
3. **QUAN TRỌNG:** Restart backend sau khi sửa .env

### Issue: Frontend vẫn báo lỗi `trim is not a function`
**Giải pháp:**
1. Xóa cache browser (Ctrl+Shift+R hoặc Ctrl+F5)
2. Đảm bảo frontend đã reload sau khi save
3. Check console xem có lỗi build không

### Issue: "Email not found" khi click vào email
**Giải pháp:**
- Chạy `python init_db.py --reset` để tạo lại tables với Integer ID
- Tạo email mới (email cũ với UUID ID không tương thích)

---

## 🎯 CHECKLIST

Sau khi làm theo hướng dẫn, đảm bảo:

- [ ] Backend restart và thấy logs load 2 SMTP keys
- [ ] Frontend không còn error `emailId.trim is not a function`
- [ ] Tạo email mới thành công (ID là số: 1, 2, 3...)
- [ ] Khi Mail.tm rate limited, SMTPLabs tự động được dùng
- [ ] Click "Làm mới" hoạt động bình thường
- [ ] History tab hoạt động với integer IDs

---

## 📝 SUMMARY

**Files đã fix:**
1. ✅ `backend/.env` - Added SMTPLABS_API_KEY_1 and SMTPLABS_API_KEY_2
2. ✅ `backend/server.py` - Multi-key support với round-robin & failover
3. ✅ `backend/models.py` - Integer IDs
4. ✅ `frontend/src/App.js` - Removed `.trim()` check

**Action required:**
1. 🔄 **Restart backend** (CTRL+C → run again)
2. 🗑️ **Reset database** nếu muốn dùng Integer IDs (`python init_db.py --reset`)
3. 🧪 **Test** tạo email khi Mail.tm rate limited

**Expected result:**
- ✅ Dual SMTP keys hoạt động (auto-failover)
- ✅ Integer IDs (1, 2, 3... thay vì UUID)
- ✅ Frontend không còn lỗi
- ✅ Tạo email thành công ngay cả khi Mail.tm rate limited
