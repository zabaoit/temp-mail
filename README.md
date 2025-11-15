# TempMail - Unlimited Temporary Email Generator

A full-stack web application for generating disposable email addresses that stay active until you delete them. The stack combines a FastAPI (Python) backend, a modern React frontend, and a MySQL database so you can manage unlimited inboxes, keep history, and save message content for later.

## Features

- Auto-create the first inbox on launch and keep it forever until you remove it manually.
- Manage multiple providers (Mail.tm, Mail.gw, 1secmail) with an auto mode plus manual domain selection.
- Unlimited lifetime inboxes with history and saved tabs so nothing disappears automatically.
- Auto-refresh every 30 seconds plus manual refresh, message previews, and full HTML/Text viewers.
- Save important messages (full HTML/text content) or bookmark entire inboxes directly from the UI.
- Copy-to-clipboard shortcuts, service/domain switchers, and a lightweight timeline showing when messages arrived.
- Dark/light themes, responsive layout, and polished empty states for laptops or mobile browsers.

## Tech Stack

**Backend**
- FastAPI (Python 3.9+)
- MySQL 8.0+ with SQLAlchemy ORM
- httpx for async provider API calls
- Background tasks for provider sync and optional housekeeping

**Frontend**
- React 18
- Tailwind CSS
- Axios for API calls
- Lucide React icons
- Sonner for toast notifications

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.9 or higher**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 18 or higher & Yarn**
   - Download Node.js: https://nodejs.org/
   - Install Yarn: `npm install -g yarn`
   - Verify: `node --version` && `yarn --version`

3. **MySQL 8.0 or higher**
   - Download: https://dev.mysql.com/downloads/mysql/
   - Or install via package manager:
     - macOS: `brew install mysql`
     - Ubuntu/Debian: `sudo apt install mysql-server`
     - Windows: download the MySQL installer

## Quick Start

### Step 1: Configure MySQL

1. Start MySQL service:
```bash
# macOS
brew services start mysql

# Ubuntu/Debian
sudo systemctl start mysql

# Windows
# Start MySQL from Services or MySQL Workbench
```

2. Create database and user:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- If using different credentials, update backend/.env
-- Default credentials: root / 190705
```

### Step 2: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=190705
DB_NAME=temp_mail
CORS_ORIGINS=http://localhost:3000
```

5. Initialize database:
```bash
python init_db.py
```

6. Start backend server:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Backend runs at **http://localhost:8001**  
API docs: **http://localhost:8001/docs**

### Step 3: Frontend Setup

1. Open a new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
yarn install
```

3. Configure `.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
PORT=3000
```

4. Start the development server:
```bash
yarn start
```

Frontend runs at **http://localhost:3000**

### Step 4: Use the Application

1. Browse to **http://localhost:3000**
2. The first unlimited inbox is created automatically
3. Use the provider/domain selectors to create more addresses or switch services
4. Copy addresses, refresh messages, and toggle auto-refresh as needed
5. Save important messages or delete inboxes - history and saved tabs keep everything accessible

## Project Structure

```
/app/
|-- backend/
|   |-- server.py            # FastAPI application and API endpoints
|   |-- database.py          # MySQL connection/session helpers
|   |-- models.py            # SQLAlchemy models (TempEmail, EmailHistory, SavedEmail)
+   |-- background_tasks.py  # Optional housekeeping/background jobs
|   |-- init_db.py           # Database bootstrap script
|   |-- requirements.txt     # Backend dependencies
|   |-- .env                 # Backend configuration
|
|-- frontend/
|   |-- src/
|   |   |-- App.js           # Main React application (unlimited inbox UI)
|   |   |-- TempMail.js      # Secondary/alternate UI (optional)
|   |   |-- App.css          # Global styles
|   |   |-- index.js         # Entry point
|   |-- public/              # Static assets
|   |-- package.json         # Frontend dependencies
|   |-- .env                 # Frontend configuration
|
|-- README.md                # English documentation
|-- HUONG_DAN.md             # Vietnamese documentation
```

## Database Schema

### Table: `temp_emails`
```sql
CREATE TABLE temp_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NULL,          -- kept for backwards compatibility
    message_count INT DEFAULT 0,
    provider VARCHAR(50) NOT NULL,
    mailbox_id VARCHAR(255),
    username VARCHAR(255),
    domain VARCHAR(255)
);
```

### Table: `email_history`
```sql
CREATE TABLE email_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    token TEXT NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    expired_at DATETIME NOT NULL,      -- timestamp when the inbox was archived
    message_count INT DEFAULT 0
);
```

### Table: `saved_emails`
```sql
CREATE TABLE saved_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_address VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    from_address VARCHAR(255),
    from_name VARCHAR(255),
    html LONGTEXT,
    text LONGTEXT,
    created_at DATETIME NOT NULL,
    saved_at DATETIME NOT NULL
);
```

## API Endpoints

Base URL: `http://localhost:8001/api`

### Active Emails
- `POST /emails/create` - Create a new inbox (auto provider or manual selection)
- `GET /emails` - List active inboxes
- `GET /emails/{id}` - Get inbox details
- `POST /emails/{id}/refresh` - Refresh messages for an inbox
- `GET /emails/{id}/messages` - List messages inside an inbox
- `GET /emails/{id}/messages/{message_id}` - Get message detail (HTML/Text)
- `POST /emails/{id}/messages/{message_id}/save` - Save a message to the Saved tab
- `POST /emails/{id}/save` - Bookmark the inbox (metadata only)
- `DELETE /emails/{id}` - Delete an inbox (moves it to history)

### History
- `GET /emails/history/list` - List archived inboxes
- `GET /emails/history/{id}/messages` - List messages of a history entry
- `GET /emails/history/{id}/messages/{message_id}` - Message detail from history
- `DELETE /emails/history/delete` - Delete selected or all history entries

### Saved Emails
- `GET /emails/saved/list` - List saved messages
- `GET /emails/saved/{id}` - Full saved message content
- `DELETE /emails/saved/delete` - Delete selected or all saved messages

### Domains
- `GET /domains?service={service}` - Return available domains for the requested provider

## Troubleshooting

### Backend won't start

**Error: "Can't connect to MySQL server"**
```bash
# Check if MySQL is running
mysql -u root -p

# Verify credentials in backend/.env
# Check if database exists
mysql -u root -p -e "SHOW DATABASES;"
```

**Error: "No module named 'httpx'"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules yarn.lock
yarn install
```

**Error: "Port 3000 already in use"**
```bash
# Change port in frontend/.env
PORT=7050
```

### Database issues

**Reset database**
```bash
cd backend
python init_db.py --reset
# Type 'yes' to confirm
```

**Manual reset**
```sql
mysql -u root -p

DROP DATABASE temp_mail;
CREATE DATABASE temp_mail CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE temp_mail;
```

## Development Tips

### Hot Reload
- Backend: `uvicorn --reload` watches Python files
- Frontend: `yarn start` reloads on file changes

### Viewing Logs
```bash
# Backend logs appear in the terminal running uvicorn
# Frontend build errors appear in the terminal running yarn start
```

### Testing API
- Use Swagger UI: http://localhost:8001/docs
- Or curl:
```bash
# Create inbox
curl -X POST http://localhost:8001/api/emails/create

# List inboxes
curl http://localhost:8001/api/emails

# List saved messages
curl http://localhost:8001/api/emails/saved/list
```

## Features Explained

### Auto-create on First Visit
The application spins up the first inbox automatically so you can copy an address immediately without pressing any buttons.

### Unlimited Lifetime
Inboxes stay active indefinitely until you delete them. The timer badge shows "Unlimited" to reflect that behavior.

### Manage Multiple Addresses
Use the provider/domain selectors and the inbox switcher to rotate between as many addresses as you need. Delete or bookmark any inbox without affecting the others.

### Smart Refresh
Auto-refresh runs every 30 seconds, and you can trigger manual refreshes whenever you expect a verification email. Message previews load quickly and you can open HTML or plain-text tabs for full content.

### Email History
Deleting an inbox moves it to history. You can revisit those inboxes, view all messages that were received, and clean up history in bulk at any time.

### Save Important Emails
Save any message into the Saved tab to keep the full HTML/Text payload indefinitely. Use this for verification steps, receipts, or debugging incoming emails.

## Support

1. Review this README and `HUONG_DAN.md`
2. Verify all prerequisites are installed
3. Check the troubleshooting section
4. Inspect backend logs for specific error messages

## License

This project is provided as-is for personal and educational use.

---

Made with love using FastAPI + React + MySQL
