from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GuardianCreate(BaseModel):
    full_name: str
    phone: str
    relationship: str | None = None
    is_active: bool = True


class GuardianUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    relationship: str | None = None
    is_active: bool | None = None


class GuardianResponse(BaseModel):
    id: UUID
    organization_id: UUID
    full_name: str
    phone: str
    relationship: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
