<<<<<<< HEAD
"""FastAPI server with MySQL and expiry features"""
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import logging
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import httpx
import random
import string
import asyncio
import time

from database import engine, get_db, Base
from models import TempEmail as TempEmailModel, EmailHistory as EmailHistoryModel
=======
from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import httpx
import secrets
import string

>>>>>>> 9802088c29fbefbb5fe355e8fdb4e970da82d1fe

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

<<<<<<< HEAD
# Create database tables
Base.metadata.create_all(bind=engine)

# Create the main app
=======
# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
>>>>>>> 9802088c29fbefbb5fe355e8fdb4e970da82d1fe
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

<<<<<<< HEAD
# Email Provider Configuration
MAILTM_BASE_URL = "https://api.mail.tm"

# Rate limiting tracking (in-memory)
# In production, use Redis or database
_rate_limit_tracker = {
    "last_create_time": 0,
    "create_count": 0,
    "reset_time": 0
}

# Domain cache to reduce API calls
_domain_cache = {
    "domain": None,
    "cached_at": 0,
    "ttl": 300  # Cache for 5 minutes
}

# Provider tracking
_provider_stats = {
    "mailtm": {"success": 0, "failures": 0, "last_failure": 0}
}


# Pydantic Models
class TempEmailSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    
    id: int
    address: str
    password: str
    token: str
    account_id: str
    created_at: datetime
    expires_at: datetime
    message_count: int = 0


class EmailHistorySchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    
    id: int
    address: str
    password: str
    token: str
    account_id: str
    created_at: datetime
    expired_at: datetime
    message_count: int = 0


class CreateEmailRequest(BaseModel):
    username: Optional[str] = None


class CreateEmailResponse(BaseModel):
    id: int
    address: str
    created_at: datetime
    expires_at: datetime


class DeleteHistoryRequest(BaseModel):
    ids: Optional[List[int]] = None


# Mail.tm Service Functions
async def get_available_domains():
    """Get available domains from Mail.tm with caching"""
    current_time = time.time()
    
    # Check cache first
    if (_domain_cache["domain"] and 
        current_time - _domain_cache["cached_at"] < _domain_cache["ttl"]):
        logging.info(f"Using cached domain: {_domain_cache['domain']}")
        return _domain_cache["domain"]
    
    # Fetch from API with retry
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        for attempt in range(3):
            try:
                response = await http_client.get(f"{MAILTM_BASE_URL}/domains")
                response.raise_for_status()
                data = response.json()
                domains = data.get("hydra:member", [])
                if domains:
                    domain = domains[0]["domain"]
                    # Update cache
                    _domain_cache["domain"] = domain
                    _domain_cache["cached_at"] = current_time
                    logging.info(f"Cached new domain: {domain}")
                    return domain
                return None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logging.warning(f"Rate limited on domains, waiting {wait_time}s (attempt {attempt + 1}/3)")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error(f"Error getting domains: {e}")
                    return None
            except Exception as e:
                logging.error(f"Error getting domains: {e}")
                return None
        
        # All retries failed
        return None


async def create_mailtm_account(address: str, password: str):
    """Create account on Mail.tm with retry logic"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        for attempt in range(3):
            try:
                response = await http_client.post(
                    f"{MAILTM_BASE_URL}/accounts",
                    json={"address": address, "password": password}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.warning(f"Rate limited on account creation, waiting {wait_time}s (attempt {attempt + 1}/3)")
                    
                    if attempt < 2:  # Don't wait on last attempt
                        await asyncio.sleep(wait_time)
                    else:
                        # Last attempt failed
                        raise HTTPException(
                            status_code=429, 
                            detail="Mail.tm API rate limit exceeded. Please wait a few minutes and try again."
                        )
                else:
                    logging.error(f"Error creating account: {e}")
                    raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logging.error(f"Error creating account: {e}")
                raise HTTPException(status_code=400, detail=str(e))


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
            logging.error(f"Error getting token: {e}")
            raise HTTPException(status_code=400, detail=str(e))


async def get_mailtm_messages(token: str):
    """Get messages from Mail.tm"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        try:
            response = await http_client.get(
                f"{MAILTM_BASE_URL}/messages",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("hydra:member", [])
        except Exception as e:
            logging.error(f"Error getting messages: {e}")
            return []


async def get_mailtm_message_detail(token: str, message_id: str):
    """Get message detail from Mail.tm"""
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        try:
            response = await http_client.get(
                f"{MAILTM_BASE_URL}/messages/{message_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error getting message detail: {e}")
            return None




# ============================================================================
# Unified Email Creation - Mail.tm Only
# ============================================================================

async def create_email_with_fallback(username: str = None):
    """
    Create email using Mail.tm (free, no API key needed)
    """
    try:
        logging.info("🔄 Creating email via Mail.tm...")
        
        # Get available domain
        domain = await get_available_domains()
        if not domain:
            raise Exception("No domains available from Mail.tm")
        
        # Generate username
        if not username:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Create account
        account_data = await create_mailtm_account(address, password)
        
        # Get token
        token = await get_mailtm_token(address, password)
        
        _provider_stats["mailtm"]["success"] += 1
        logging.info(f"✅ Mail.tm email created: {address}")
        
        return {
            "provider": "mailtm",
            "address": address,
            "password": password,
            "token": token,
            "account_id": account_data["id"],
            "mailbox_id": None
        }
        
    except Exception as e:
        error_msg = str(e)
        _provider_stats["mailtm"]["failures"] += 1
        _provider_stats["mailtm"]["last_failure"] = time.time()
        logging.error(f"❌ Mail.tm failed: {error_msg}")
        raise HTTPException(
            status_code=503,
            detail=f"Mail.tm unavailable: {error_msg}"
        )



# API Routes
@api_router.get("/")
async def root():
    return {"message": "TempMail API - MySQL with Expiry"}


@api_router.post("/emails/create", response_model=CreateEmailResponse)
async def create_email(request: CreateEmailRequest, db: Session = Depends(get_db)):
    """Create a new temporary email with dual provider fallback (Mail.tm → SMTPLabs)"""
    try:
        # Check local rate limit (max 10 emails per minute for development)
        # TODO: Lower this to 3 for production
        current_time = time.time()
        MAX_EMAILS_PER_MINUTE = 10  # Increase for development/testing
        
        if current_time - _rate_limit_tracker["reset_time"] > 60:
            # Reset counter after 1 minute
            _rate_limit_tracker["create_count"] = 0
            _rate_limit_tracker["reset_time"] = current_time
        
        if _rate_limit_tracker["create_count"] >= MAX_EMAILS_PER_MINUTE:
            wait_seconds = int(60 - (current_time - _rate_limit_tracker["reset_time"]))
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit: Maximum {MAX_EMAILS_PER_MINUTE} emails per minute. Please wait {wait_seconds} seconds."
            )
        
        # Increment counter
        _rate_limit_tracker["create_count"] += 1
        _rate_limit_tracker["last_create_time"] = current_time
        
        # Use unified email creation with fallback
        email_data = await create_email_with_fallback(username=request.username)
        
        # Calculate expiry time (10 minutes from now)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=10)
        
        # Save to database with provider info
        email = TempEmailModel(
            address=email_data["address"],
            password=email_data["password"],
            token=email_data["token"],
            account_id=email_data["account_id"],
            created_at=now,
            expires_at=expires_at,
            message_count=0
        )
        
        db.add(email)
        db.commit()
        db.refresh(email)
        
        return CreateEmailResponse(
            id=email.id,
            address=email.address,
            created_at=email.created_at,
            expires_at=email.expires_at
        )
    except Exception as e:
        logging.error(f"Error creating email: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/emails", response_model=List[TempEmailSchema])
async def get_emails(db: Session = Depends(get_db)):
    """Get all temporary emails"""
    emails = db.query(TempEmailModel).order_by(TempEmailModel.created_at.desc()).all()
    return [email.to_dict() for email in emails]


@api_router.get("/emails/{email_id}")
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get email by ID"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return email.to_dict()


@api_router.get("/emails/{email_id}/messages")
async def get_email_messages(email_id: int, db: Session = Depends(get_db)):
    """Get messages for an email"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Get messages from Mail.tm
    messages = await get_mailtm_messages(email.token)
    
    # Update message count
    email.message_count = len(messages)
    db.commit()
    
    return {"messages": messages, "count": len(messages)}


@api_router.get("/emails/{email_id}/messages/{message_id}")
async def get_message_detail(email_id: int, message_id: str, db: Session = Depends(get_db)):
    """Get message detail"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    message = await get_mailtm_message_detail(email.token, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message


@api_router.post("/emails/{email_id}/refresh")
async def refresh_messages(email_id: int, db: Session = Depends(get_db)):
    """Refresh messages for an email"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    messages = await get_mailtm_messages(email.token)
    
    email.message_count = len(messages)
    db.commit()
    
    return {"messages": messages, "count": len(messages)}


@api_router.delete("/emails/{email_id}")
async def delete_email(email_id: int, db: Session = Depends(get_db)):
    """Delete a temporary email"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    db.delete(email)
    db.commit()
    
    return {"status": "deleted"}


@api_router.post("/emails/{email_id}/extend-time")
async def extend_email_time(email_id: int, db: Session = Depends(get_db)):
    """Extend email expiry time by resetting to 10 minutes from now"""
    email = db.query(TempEmailModel).filter(TempEmailModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Reset expires_at to 10 minutes from now (not add to existing time)
    now = datetime.now(timezone.utc)
    new_expires_at = now + timedelta(minutes=10)
    
    email.expires_at = new_expires_at
    db.commit()
    db.refresh(email)
    
    return {
        "status": "extended",
        "expires_at": new_expires_at.isoformat()
    }


@api_router.get("/emails/history/list", response_model=List[EmailHistorySchema])
async def get_email_history(db: Session = Depends(get_db)):
    """Get all emails in history"""
    history = db.query(EmailHistoryModel).order_by(EmailHistoryModel.expired_at.desc()).all()
    return [email.to_dict() for email in history]


@api_router.get("/emails/history/{email_id}/messages")
async def get_history_email_messages(email_id: int, db: Session = Depends(get_db)):
    """Get messages for a history email"""
    email = db.query(EmailHistoryModel).filter(EmailHistoryModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found in history")
    
    # Get messages from Mail.tm using the stored token
    messages = await get_mailtm_messages(email.token)
    
    return {"messages": messages, "count": len(messages)}


@api_router.get("/emails/history/{email_id}/messages/{message_id}")
async def get_history_message_detail(email_id: int, message_id: str, db: Session = Depends(get_db)):
    """Get message detail for a history email"""
    email = db.query(EmailHistoryModel).filter(EmailHistoryModel.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found in history")
    
    message = await get_mailtm_message_detail(email.token, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message


@api_router.delete("/emails/history/delete")
async def delete_history_emails(request: DeleteHistoryRequest, db: Session = Depends(get_db)):
    """Delete history emails. If ids is None or empty, delete all"""
    try:
        if request.ids and len(request.ids) > 0:
            # Delete specific emails by IDs
            result = db.query(EmailHistoryModel).filter(EmailHistoryModel.id.in_(request.ids)).delete(synchronize_session=False)
            db.commit()
            deleted_count = result
        else:
            # Delete all history emails
            result = db.query(EmailHistoryModel).delete(synchronize_session=False)
            db.commit()
            deleted_count = result
        
        return {
            "status": "deleted",
            "count": deleted_count
        }
    except Exception as e:
        logging.error(f"Error deleting history emails: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Startup event to start background tasks
@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    from background_tasks import start_background_tasks
    start_background_tasks()
    logging.info("Application started with background tasks (MySQL)")

=======
# Mail service configurations
MAIL_SERVICES = {
    "mail.tm": "https://api.mail.tm",
    "mail.gw": "https://api.mail.gw"
}

# Define Models
class DomainResponse(BaseModel):
    id: str
    domain: str
    service: str

class CreateEmailRequest(BaseModel):
    service: str
    domain: str

class CreateEmailResponse(BaseModel):
    id: str
    email: str
    password: str
    service: str
    token: Optional[str] = None

class Message(BaseModel):
    id: str
    from_email: str = Field(alias="from")
    subject: str
    intro: Optional[str] = None
    text: Optional[str] = None
    html: Optional[List[str]] = None
    created_at: str = Field(alias="createdAt")
    
    model_config = ConfigDict(populate_by_name=True)

class GetMessagesRequest(BaseModel):
    email: str
    token: str
    service: str

# Helper functions
def generate_random_string(length=10):
    """Generate random string for email username"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(letters) for i in range(length))

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Temporary Email Service"}

@api_router.get("/domains")
async def get_domains():
    """Get available domains from both mail.tm and mail.gw"""
    all_domains = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for service_name, base_url in MAIL_SERVICES.items():
            try:
                response = await client.get(f"{base_url}/domains")
                if response.status_code == 200:
                    data = response.json()
                    domains = data.get("hydra:member", []) if "hydra:member" in data else data
                    for domain_obj in domains:
                        all_domains.append({
                            "id": domain_obj.get("id", domain_obj.get("domain")),
                            "domain": domain_obj.get("domain"),
                            "service": service_name
                        })
            except Exception as e:
                logger.error(f"Error fetching domains from {service_name}: {e}")
    
    return {"domains": all_domains}

@api_router.post("/create-email")
async def create_email(request: CreateEmailRequest):
    """Create a new temporary email account"""
    base_url = MAIL_SERVICES.get(request.service)
    if not base_url:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    # Generate random username
    username = generate_random_string(10)
    email = f"{username}@{request.domain}"
    password = generate_random_string(16)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Create account
            account_data = {
                "address": email,
                "password": password
            }
            create_response = await client.post(
                f"{base_url}/accounts",
                json=account_data
            )
            
            if create_response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=create_response.status_code,
                    detail=f"Failed to create account: {create_response.text}"
                )
            
            account = create_response.json()
            account_id = account.get("id")
            
            # Login to get token
            login_data = {
                "address": email,
                "password": password
            }
            token_response = await client.post(
                f"{base_url}/token",
                json=login_data
            )
            
            if token_response.status_code == 200:
                token_data = token_response.json()
                token = token_data.get("token")
            else:
                token = None
            
            # Save to database
            email_doc = {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "email": email,
                "password": password,
                "service": request.service,
                "token": token,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await db.emails.insert_one(email_doc)
            
            return {
                "id": email_doc["id"],
                "email": email,
                "password": password,
                "service": request.service,
                "token": token
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating email: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/messages")
async def get_messages(request: GetMessagesRequest):
    """Get messages for a specific email"""
    base_url = MAIL_SERVICES.get(request.service)
    if not base_url:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            headers = {
                "Authorization": f"Bearer {request.token}"
            }
            response = await client.get(
                f"{base_url}/messages",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get("hydra:member", []) if "hydra:member" in data else data
                return {"messages": messages}
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch messages"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/messages/{message_id}")
async def get_message_detail(message_id: str, service: str, token: str):
    """Get detailed message content"""
    base_url = MAIL_SERVICES.get(service)
    if not base_url:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = await client.get(
                f"{base_url}/messages/{message_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch message"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching message detail: {e}")
            raise HTTPException(status_code=500, detail=str(e))
>>>>>>> 9802088c29fbefbb5fe355e8fdb4e970da82d1fe

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
<<<<<<< HEAD
=======

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
>>>>>>> 9802088c29fbefbb5fe355e8fdb4e970da82d1fe
