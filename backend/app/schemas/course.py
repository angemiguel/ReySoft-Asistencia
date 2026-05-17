from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    section: str | None = None
    academic_year: str | None = None
    is_active: bool = True


class CourseUpdate(BaseModel):
    name: str | None = None
    section: str | None = None
    academic_year: str | None = None
    is_active: bool | None = None


class CourseResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    section: str | None = None
    academic_year: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
