from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class LoginLog(Base):
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    login_time = Column(DateTime, server_default=func.now())
    logout_time = Column(DateTime, nullable=True)
    ip_address = Column(String(50), nullable=True)
    device_info = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="success")  # success | failed

    user = relationship("User", back_populates="login_logs")
