from datetime import date, time
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import AttendanceStatus


class AttendanceReportRecord(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    attendance_date: date
    status: str
    arrival_time: time | None = None
    departure_time: time | None = None
    display_time: time | None = None
    notes: str | None = None


class AttendanceStudentReport(BaseModel):
    student_id: UUID
    student_name: str
    student_code: str | None = None
    course_id: UUID
    course_name: str
    course_section: str | None = None
    course_academic_year: str | None = None
    arrived_count: int = 0
    absent_count: int = 0
    late_count: int = 0
    early_pickup_count: int = 0
    excused_count: int = 0
    excused_absence_equivalent: int = 0
    equivalent_absences: int = 0
    total_records: int = 0
    risk_level: str = "ok"
    risk_color: str = "green"
    records: list[AttendanceReportRecord] = []


class AttendanceCourseReport(BaseModel):
    course_id: UUID
    course_name: str
    course_section: str | None = None
    course_academic_year: str | None = None
    student_count: int = 0
    arrived_count: int = 0
    absent_count: int = 0
    late_count: int = 0
    early_pickup_count: int = 0
    excused_count: int = 0
    excused_absence_equivalent: int = 0
    equivalent_absences: int = 0
    total_records: int = 0
    ok_students: int = 0
    warning_students: int = 0
    danger_students: int = 0
    risk_level: str = "ok"
    risk_color: str = "green"
    records: list[AttendanceReportRecord] = []
