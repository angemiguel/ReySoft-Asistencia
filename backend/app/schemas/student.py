from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StudentCreate(BaseModel):
    course_id: UUID
    full_name: str
    student_code: str | None = None
    is_active: bool = True
    guardian_ids: list[UUID] = []
    primary_guardian_id: UUID | None = None


class StudentUpdate(BaseModel):
    course_id: UUID | None = None
    full_name: str | None = None
    student_code: str | None = None
    is_active: bool | None = None


class StudentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    course_id: UUID
    full_name: str
    student_code: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentGuardianCreate(BaseModel):
    guardian_id: UUID
    is_primary: bool = False


class StudentGuardianResponse(BaseModel):
    id: UUID
    student_id: UUID
    guardian_id: UUID
    is_primary: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentImportResponse(BaseModel):
    created: int = 0
    updated: int = 0
    errors: list[str] = []
