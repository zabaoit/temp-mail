"""MongoDB database connection for container environment"""
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection (for container environment)
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
database = client["temp_mail"]

# Collections
emails_collection = database["temp_emails"]
history_collection = database["email_history"]
saved_collection = database["saved_emails"]
