from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.enums import OrganizationStatus


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str | None = None
    logo_url: str | None = None
    footer_text: str | None = None
    primary_color: str = "#2563EB"
    secondary_color: str = "#1E293B"
    accent_color: str = "#F59E0B"
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrganizationSettingsUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    footer_text: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None
