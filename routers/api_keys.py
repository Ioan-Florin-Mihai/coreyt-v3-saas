import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.key_manager import ApiKeyManager
from database.models import ApiKey
from database.session import get_db

router = APIRouter(prefix="/api/users/keys", tags=["api-keys"])


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key_prefix: str
    created_at: datetime
    is_active: bool


class ApiKeyCreateResponse(ApiKeyResponse):
    key: str


@router.post("", response_model=ApiKeyCreateResponse)
def create_api_key(body: ApiKeyCreate, db: Session = Depends(get_db)):

    raw_key = ApiKeyManager.generate_key()

    key_hash = ApiKeyManager.hash_key(raw_key)

    prefix = ApiKeyManager.extract_prefix(raw_key)

    db_key = ApiKey(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),  # temporary user id
        key_hash=key_hash,
        key_prefix=prefix,
        name=body.name,
        created_at=datetime.utcnow(),
        is_active=True,
        is_revoked=False,
    )

    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    return ApiKeyCreateResponse(
        id=str(db_key.id),
        key=raw_key,
        name=db_key.name,
        key_prefix=db_key.key_prefix,
        created_at=db_key.created_at,
        is_active=db_key.is_active,
    )


@router.get("", response_model=list[ApiKeyResponse])
def list_api_keys(db: Session = Depends(get_db)):

    keys = db.query(ApiKey).all()

    return [
        ApiKeyResponse(
            id=str(k.id),
            name=k.name,
            key_prefix=k.key_prefix,
            created_at=k.created_at,
            is_active=k.is_active,
        )
        for k in keys
    ]
