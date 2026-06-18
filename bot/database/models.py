from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class UserModel(BaseModel):
    user_id: int = Field(..., alias="_id")
    username: Optional[str] = None
    first_name: Optional[str] = None
    role: str = "user"  # user, admin
    created_at: datetime = Field(default_factory=utc_now)
    last_active: datetime = Field(default_factory=utc_now)

class TaskModel(BaseModel):
    task_id: str = Field(..., alias="_id")
    user_id: int
    scraper_name: str
    status: str = "pending"  # pending, processing, completed, failed
    progress: float = 0.0
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class LogModel(BaseModel):
    timestamp: datetime = Field(default_factory=utc_now)
    level: str
    module: str
    message: str
    user_id: Optional[int] = None

class SettingsModel(BaseModel):
    key: str = Field(..., alias="_id")
    value: Any
    description: Optional[str] = None
    updated_at: datetime = Field(default_factory=utc_now)
