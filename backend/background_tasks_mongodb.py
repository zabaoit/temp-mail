"""Background tasks for MongoDB version"""
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from database_mongodb import client
from models_mongodb import TempEmail, EmailHistory
import httpx
import random
import string

logger = logging.getLogger(__name__)

# Get database
db = client.get_database()
temp_emails_collection = db.temp_emails
history_collection = db.email_history

# Mail.tm Configuration
MAILTM_BASE_URL = "https://api.mail.tm"


async def get_available_domains():
    """Get available domains from Mail.tm"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        try:
            response = await http_client.get(f"{MAILTM_BASE_URL}/domains")
            response.raise_for_status()
            data = response.json()
            domains = data.get("hydra:member", [])
            if domains:
                return domains[0]["domain"]
            return None
        except Exception as e:
            logger.error(f"Error getting domains: {e}")
            return None


async def create_mailtm_account(address: str, password: str):
    """Create account on Mail.tm"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        try:
            response = await http_client.post(
                f"{MAILTM_BASE_URL}/accounts",
                json={"address": address, "password": password}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            return None


async def get_mailtm_token(address: str, password: str):
    """Get authentication token from Mail.tm"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        try:
            response = await http_client.post(
                f"{MAILTM_BASE_URL}/token",
                json={"address": address, "password": password}
            )
            response.raise_for_status()
            return response.json()["token"]
        except Exception as e:
            logger.error(f"Error getting token: {e}")
            return None


async def create_new_email_auto():
    """Automatically create a new temporary email"""
    try:
        # Get available domain
        domain = await get_available_domains()
        if not domain:
            logger.error("No domains available for auto-creation")
            return None
        
        # Generate random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Create account on Mail.tm
        account_data = await create_mailtm_account(address, password)
        if not account_data:
            logger.error("Failed to create Mail.tm account")
            return None
        
        # Get authentication token
        token = await get_mailtm_token(address, password)
        if not token:
            logger.error("Failed to get Mail.tm token")
            return None
        
        # Calculate expiry time (10 minutes from now)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=10)
        
        # Create document
        email_doc = TempEmail.create_document(
            address=address,
            password=password,
            token=token,
            account_id=account_data["id"],
            expires_at=expires_at
        )
        
        # Save to database
        await temp_emails_collection.insert_one(email_doc)
        
        logger.info(f"Auto-created new email: {address}")
        return email_doc
        
    except Exception as e:
        logger.error(f"Error in auto-creating email: {e}")
        return None


async def check_expired_emails():
    """Background task to check and move expired emails to history"""
    while True:
        try:
            now = datetime.now(timezone.utc)
            
            # Find all expired emails
            expired_emails = await temp_emails_collection.find({
                "expires_at": {"$lte": now}
            }).to_list(None)
            
            if expired_emails:
                logger.info(f"Found {len(expired_emails)} expired emails")
                
                for email in expired_emails:
                    try:
                        # Create history document
                        history_doc = EmailHistory.create_from_temp_email(email)
                        
                        # Move to history
                        await history_collection.insert_one(history_doc)
                        await temp_emails_collection.delete_one({"_id": email["_id"]})
                        
                        logger.info(f"Moved email to history: {email['address']}")
                        
                    except Exception as e:
                        logger.error(f"Error moving email {email.get('address')} to history: {e}")
                        continue
                
                # Check if we need to create a new email
                # Only create if there are no active emails left
                active_count = await temp_emails_collection.count_documents({})
                if active_count == 0:
                    logger.info("No active emails, creating new one...")
                    await create_new_email_auto()
            
        except Exception as e:
            logger.error(f"Error in check_expired_emails: {e}")
        
        # Check every 30 seconds
        await asyncio.sleep(30)


def start_background_tasks():
    """Start all background tasks"""
    asyncio.create_task(check_expired_emails())
    logger.info("Background tasks started (MongoDB version)")
