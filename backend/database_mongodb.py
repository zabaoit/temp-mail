"""MongoDB database configuration for container environment"""
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
ROOT_DIR = Path(__file__).parent
env_path = ROOT_DIR / '.env'
load_dotenv(env_path, override=True)

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = "temp_mail_db"

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]

# Collections
emails_collection = database.get_collection("temp_emails")
history_collection = database.get_collection("email_history")

async def get_database():
    """Get database instance"""
    return database

print(f"✅ MongoDB connected: {MONGO_URL}")
print(f"✅ Database: {DB_NAME}")
