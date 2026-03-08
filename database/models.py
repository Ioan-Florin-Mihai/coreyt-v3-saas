from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    user_id = Column(String, index=True)
    key_prefix = Column(String, index=True)
    key_hash = Column(String, unique=True, index=True)

    is_active = Column(Boolean, default=True)
    is_revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    api_key = Column(String, index=True)
    endpoint = Column(String)
    tokens = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)