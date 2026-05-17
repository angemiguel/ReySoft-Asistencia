from datetime import date, time
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import AttendanceStatus
from app.schemas.guardian import GuardianResponse


class ParentLoginRequest(BaseModel):
    phone: str


class ParentTokenResponse(BaseModel):
    access_token: str
    token_type: str
    guardian: GuardianResponse


class ParentGuardianResponse(BaseModel):
    id: UUID
    full_name: str
    phone: str
    relationship: str | None = None
    organization_id: UUID

    model_config = {"from_attributes": True}


class ParentStudentResponse(BaseModel):
    id: UUID
    full_name: str
    student_code: str | None = None
    course_id: UUID
    course_name: str
    course_section: str | None = None
    course_academic_year: str | None = None
    organization_name: str


class ParentAttendanceResponse(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    attendance_date: date
    status: AttendanceStatus
    arrival_time: time | None = None
    departure_time: time | None = None
    display_time: time | None = None
    notes: str | None = None
