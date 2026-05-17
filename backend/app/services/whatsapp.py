from urllib.parse import quote

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AttendanceRecord, AttendanceStatus, Guardian, Student, StudentGuardian, WhatsAppMessageTemplate


def _get_template_text(db: Session, organization_id: int, status: AttendanceStatus) -> str | None:
    template = db.scalar(
        select(WhatsAppMessageTemplate).where(
            WhatsAppMessageTemplate.organization_id == organization_id,
            WhatsAppMessageTemplate.status == status,
            WhatsAppMessageTemplate.is_active.is_(True),
        )
    )
    return template.template_text if template else None


def _get_primary_guardian(db: Session, student_id: int) -> Guardian | None:
    relation = db.scalar(
        select(StudentGuardian).where(
            StudentGuardian.student_id == student_id,
            StudentGuardian.is_primary.is_(True),
        )
    )
    if not relation:
        return None
    return db.get(Guardian, relation.guardian_id)


def _format_datetime_for_template(record: AttendanceRecord) -> tuple[str, str]:
    date_str = record.attendance_date.isoformat()
    time_str = ""
    if record.arrival_time:
        time_str = record.arrival_time.strftime("%H:%M")
    elif record.departure_time:
        time_str = record.departure_time.strftime("%H:%M")
    return date_str, time_str


def build_whatsapp_link(db: Session, record: AttendanceRecord) -> dict:
    guardian = _get_primary_guardian(db, record.student_id)
    if not guardian or not guardian.phone:
        return {"url": ""}

    student = db.get(Student, record.student_id)
    if not student:
        return {"url": ""}

    template_text = _get_template_text(db, record.organization_id, record.status)
    if not template_text:
        return {"url": ""}

    date_str, time_str = _format_datetime_for_template(record)
    course_name = student.course.name if student.course else ""

    message = (
        template_text.replace("{guardian_name}", guardian.full_name)
        .replace("{student_name}", student.full_name)
        .replace("{course_name}", course_name)
        .replace("{school_name}", student.organization.name if student.organization else "")
        .replace("{date}", date_str)
        .replace("{time}", time_str)
    )

    phone_clean = guardian.phone.replace(" ", "").replace("-", "").replace("+", "")
    url = f"https://wa.me/{phone_clean}?text={quote(message)}"
    return {"url": url}
