"""MongoDB models for TempMail application"""
from datetime import datetime, timezone
from typing import Optional
import uuid


class TempEmail:
    """Temporary email document for MongoDB"""
    
    @staticmethod
    def create_document(address: str, password: str, token: str, account_id: str, expires_at: datetime) -> dict:
        """Create a new email document"""
        now = datetime.now(timezone.utc)
        return {
            "_id": str(uuid.uuid4()),
            "address": address,
            "password": password,
            "token": token,
            "account_id": account_id,
            "created_at": now,
            "expires_at": expires_at,
            "message_count": 0
        }
    
    @staticmethod
    def to_dict(doc: dict) -> dict:
        """Convert MongoDB document to API response format"""
        return {
            "id": doc["_id"],
            "address": doc["address"],
            "password": doc["password"],
            "token": doc["token"],
            "account_id": doc["account_id"],
            "created_at": doc["created_at"].isoformat() if isinstance(doc["created_at"], datetime) else doc["created_at"],
            "expires_at": doc["expires_at"].isoformat() if isinstance(doc["expires_at"], datetime) else doc["expires_at"],
            "message_count": doc.get("message_count", 0)
        }


class EmailHistory:
    """Email history document for MongoDB"""
    
    @staticmethod
    def create_from_temp_email(email_doc: dict) -> dict:
        """Create history document from temp email"""
        return {
            "_id": email_doc["_id"],
            "address": email_doc["address"],
            "password": email_doc["password"],
            "token": email_doc["token"],
            "account_id": email_doc["account_id"],
            "created_at": email_doc["created_at"],
            "expired_at": email_doc["expires_at"],  # Renamed from expires_at
            "message_count": email_doc.get("message_count", 0)
        }
    
    @staticmethod
    def to_dict(doc: dict) -> dict:
        """Convert MongoDB document to API response format"""
        return {
            "id": doc["_id"],
            "address": doc["address"],
            "password": doc["password"],
            "token": doc["token"],
            "account_id": doc["account_id"],
            "created_at": doc["created_at"].isoformat() if isinstance(doc["created_at"], datetime) else doc["created_at"],
            "expired_at": doc["expired_at"].isoformat() if isinstance(doc["expired_at"], datetime) else doc["expired_at"],
            "message_count": doc.get("message_count", 0)
        }
