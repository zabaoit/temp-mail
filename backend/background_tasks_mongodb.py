"""Background tasks for MongoDB (container environment)"""
import asyncio
import logging
from datetime import datetime, timezone
from database_mongodb import emails_collection, history_collection
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def check_and_move_expired_emails():
    """Check for expired emails and move them to history"""
    try:
        now = datetime.now(timezone.utc)
        
        # Find all expired emails
        cursor = emails_collection.find({
            "expires_at": {"$lte": now}
        })
        
        expired_count = 0
        async for email in cursor:
            # Move to history
            history_doc = {
                "address": email["address"],
                "password": email.get("password", ""),
                "token": email.get("token", ""),
                "account_id": email.get("account_id", ""),
                "created_at": email["created_at"],
                "expired_at": now,
                "message_count": email.get("message_count", 0),
                "provider": email.get("provider", ""),
                "username": email.get("username", ""),
                "domain": email.get("domain", "")
            }
            
            # Insert into history
            await history_collection.insert_one(history_doc)
            
            # Delete from active emails
            await emails_collection.delete_one({"_id": email["_id"]})
            
            expired_count += 1
            logger.info(f"✅ Moved expired email to history: {email['address']}")
        
        if expired_count > 0:
            logger.info(f"✅ Moved {expired_count} expired email(s) to history")
            
    except Exception as e:
        logger.error(f"❌ Error checking expired emails: {str(e)}")
