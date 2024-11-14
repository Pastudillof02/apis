from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl

class LogBook(BaseModel):
    email: EmailStr 
    geocache_id: str
    stamp: datetime

class LogBookInput(BaseModel):
    email: EmailStr 
    geocache_id: str
