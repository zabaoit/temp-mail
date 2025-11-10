# Container vs Local Environment Guide

## Current Status ✅

### Container Environment (Emergent Cloud)
- **Database**: MongoDB (Running)
- **Backend**: `server.py` → Uses MongoDB
- **Status**: ✅ Working perfectly
- **No setup needed**: Everything auto-configured

### Local Environment (Your Computer)
- **Database**: MySQL 8.0+
- **Backend**: `server_mysql.py` → Needs to be copied to `server.py`
- **Status**: Ready to deploy
- **Setup needed**: Follow guide below

---

## Quick Switch Guide

### To run in CONTAINER (Current - MongoDB):
```bash
cd /app/backend
cp server_mongodb.py server.py
sudo supervisorctl restart backend
```

### To run LOCAL (MySQL):
```bash
cd backend
cp server_mysql.py server.py
python -m uvicorn server:app --reload
```

---

## Files Structure

```
/app/backend/
├── server.py                    # Active file (currently MongoDB)
├── server_mysql.py              # MySQL version (for local)
├── server_mongodb.py            # MongoDB version (for container)
├── database.py                  # MySQL connection config
├── database_mongodb.py          # MongoDB connection config
├── models.py                    # MySQL models
├── background_tasks.py          # MySQL background tasks
└── background_tasks_mongodb.py  # MongoDB background tasks
```

---

## Environment Variables

### Container (.env) - MongoDB:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=*
```
Note: DB settings not used in container (uses MongoDB internally)

### Local (.env) - MySQL:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

---

## Features Comparison

| Feature | Container (MongoDB) | Local (MySQL) |
|---------|-------------------|---------------|
| Auto email creation | ✅ | ✅ |
| 10-minute timer | ✅ | ✅ |
| Auto-expire | ✅ | ✅ |
| Email history | ✅ | ✅ |
| Saved emails | ✅ | ✅ |
| Provider failover | ✅ | ✅ |
| Background tasks | ✅ | ✅ |

---

## Why Two Versions?

1. **Container Environment**:
   - Uses MongoDB (already installed)
   - No external database setup needed
   - Perfect for cloud deployment
   - Auto-managed by supervisor

2. **Local Environment**:
   - Uses MySQL (user preference)
   - Full control over database
   - Better for development
   - Can backup/restore easily

---

## Migration Path

### From Container to Local:

1. **Download files**:
   ```bash
   # Download entire /app folder from container
   ```

2. **Switch to MySQL**:
   ```bash
   cd backend
   cp server_mysql.py server.py
   ```

3. **Install MySQL**:
   - Windows: MySQL Installer
   - macOS: `brew install mysql`
   - Linux: `apt install mysql-server`

4. **Setup database**:
   ```bash
   python init_db.py
   ```

5. **Run backend**:
   ```bash
   python -m uvicorn server:app --reload
   ```

6. **Update frontend .env**:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8001
   PORT=7050
   ```

7. **Run frontend**:
   ```bash
   cd frontend
   yarn install
   yarn start
   ```

---

## Troubleshooting

### Container Issues:
- Check: `sudo supervisorctl status backend`
- Logs: `tail -f /var/log/supervisor/backend.err.log`
- Restart: `sudo supervisorctl restart backend`

### Local Issues:
- MySQL not running: `mysql -u root -p190705`
- Port conflict: Change port in `uvicorn --port 8001`
- CORS error: Check `REACT_APP_BACKEND_URL` in frontend/.env

---

## Quick Test

### Test Container (MongoDB):
```bash
curl http://localhost:8001/api/ | jq .
curl -X POST http://localhost:8001/api/emails/create | jq .
```

### Test Local (MySQL):
```bash
curl http://localhost:8001/api/ | jq .
curl -X POST http://localhost:8001/api/emails/create | jq .
```

---

## Summary

✅ **Container**: MongoDB, zero setup, working now
📝 **Local**: MySQL, need setup, full guide in `HUONG_DAN_CHAY_LOCAL_MYSQL.md`

Choose based on your needs:
- Quick testing → Use container (current)
- Development → Use local with MySQL
- Production → Either works, user preference

