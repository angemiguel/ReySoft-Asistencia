from datetime import date, time
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import AttendanceStatus


class AttendanceCreate(BaseModel):
    student_id: UUID
    attendance_date: date
    status: AttendanceStatus
    arrival_time: time | None = None
    departure_time: time | None = None
    notes: str | None = None


class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    status: AttendanceStatus | None = None
    arrival_time: time | None = None
    departure_time: time | None = None
    notes: str | None = None


class AttendanceResponse(BaseModel):
    id: UUID
    organization_id: UUID
    student_id: UUID
    recorded_by_user_id: UUID | None = None
    attendance_date: date
    status: AttendanceStatus
    arrival_time: time | None = None
    departure_time: time | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}
