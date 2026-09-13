from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    username = Column(String, index=True)
    source_ip = Column(String, index=True)
    success = Column(Boolean, default=True)
    event_type = Column(String, default="login")  # e.g. login, logout, failed_login