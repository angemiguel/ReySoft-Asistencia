from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.organization import OrganizationResponse


class UserResponse(BaseModel):
    id: UUID
    organization_id: UUID | None = None
    full_name: str
    email: str
    role: str
    is_active: bool
    organization: OrganizationResponse | None = None

    model_config = {"from_attributes": True}
