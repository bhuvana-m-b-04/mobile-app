from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoginLogResponse(BaseModel):
    id: int
    user_id: int
    login_time: datetime
    logout_time: Optional[datetime] = None
    ip_address: Optional[str] = None
    device_info: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}


class LogoutRequest(BaseModel):
    log_id: int
