from uuid import UUID

from sqlalchemy.orm import Session

from app.models import AttendanceStatus, WhatsAppMessageTemplate


DEFAULT_TEMPLATES: dict[AttendanceStatus, str] = {
    AttendanceStatus.arrived: (
        "Hola {guardian_name}, te informamos que {student_name} ha llegado al "
        "colegio {school_name} el día {date} a las {time}."
    ),
    AttendanceStatus.absent: (
        "Hola {guardian_name}, te informamos que {student_name} no ha asistido "
        "al colegio {school_name} el día {date}. Por favor, comunícate con el centro educativo."
    ),
    AttendanceStatus.late: (
        "Hola {guardian_name}, te informamos que {student_name} ha llegado tarde "
        "al colegio {school_name} el día {date} a las {time}."
    ),
    AttendanceStatus.early_pickup: (
        "Hola {guardian_name}, te informamos que {student_name} ha sido retirado "
        "temprano del colegio {school_name} el día {date} a las {time}."
    ),
    AttendanceStatus.excused: (
        "Hola {guardian_name}, te informamos que la ausencia de {student_name} "
        "del colegio {school_name} el día {date} ha sido justificada."
    ),
}


def create_default_whatsapp_templates(db: Session, organization_id: UUID) -> None:
    from sqlalchemy import select
    for status, template_text in DEFAULT_TEMPLATES.items():
        existing = db.scalar(
            select(WhatsAppMessageTemplate).where(
                WhatsAppMessageTemplate.organization_id == organization_id,
                WhatsAppMessageTemplate.status == status,
            )
        )
        if not existing:
            db.add(
                WhatsAppMessageTemplate(
                    organization_id=organization_id,
                    status=status,
                    template_text=template_text,
                    is_active=True,
                )
            )
