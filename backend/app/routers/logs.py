from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.login_log import LoginLog
from ..schemas.login_log import LoginLogResponse, LogoutRequest
from ..config import settings

router = APIRouter(prefix="/logs", tags=["logs"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/", response_model=List[LoginLogResponse])
def get_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(LoginLog)
        .filter(LoginLog.user_id == current_user.id)
        .order_by(LoginLog.login_time.desc())
        .all()
    )


@router.post("/logout")
def logout(
    req: LogoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = (
        db.query(LoginLog)
        .filter(LoginLog.id == req.log_id, LoginLog.user_id == current_user.id)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    log.logout_time = datetime.utcnow()
    db.commit()
    return {"message": "Logged out successfully"}
