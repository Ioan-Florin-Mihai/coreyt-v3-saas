import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    is_active = Column(Boolean, nullable=False, default=True)

    # JSON în loc de JSONB (compatibil SQLite)
    meta = Column(JSON, default=dict, nullable=False)

    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), unique=True, nullable=False)

    name = Column(String(255), nullable=False)

    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    is_active = Column(Boolean, nullable=False, default=True)

    meta = Column(JSON, default=dict, nullable=False)

    organization = relationship("Organization", back_populates="users")

    api_keys = relationship(
        "ApiKey", back_populates="user", cascade="all, delete-orphan"
    )


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    key_hash = Column(String(64), nullable=False, unique=True)

    key_prefix = Column(String(8), nullable=False)

    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    last_used_at = Column(DateTime)

    expires_at = Column(DateTime)

    is_active = Column(Boolean, nullable=False, default=True)

    is_revoked = Column(Boolean, nullable=False, default=False)

    meta = Column(JSON, default=dict, nullable=False)

    user = relationship("User", back_populates="api_keys")


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    endpoint = Column(String(255), nullable=False)

    method = Column(String(10), nullable=False)

    http_status = Column(Integer)

    request_tokens = Column(Integer)

    response_tokens = Column(Integer)

    total_tokens = Column(Integer)

    latency_ms = Column(Integer)

    cost_cents = Column(Integer)

    error_message = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    meta = Column(JSON, default=dict, nullable=False)
