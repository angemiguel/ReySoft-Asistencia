from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.permissions import ensure_school_admin, ensure_school_user
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models import User, WhatsAppMessageTemplate

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


def _get_template_or_404(db: Session, template_id: UUID, organization_id: UUID) -> WhatsAppMessageTemplate:
    template = db.scalar(
        select(WhatsAppMessageTemplate).where(
            WhatsAppMessageTemplate.id == template_id,
            WhatsAppMessageTemplate.organization_id == organization_id,
        )
    )
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantilla no encontrada.")
    return template


@router.get("/templates", response_model=list[dict])
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_user(current_user)
    templates = db.scalars(
        select(WhatsAppMessageTemplate).where(
            WhatsAppMessageTemplate.organization_id == current_user.organization_id
        )
    ).all()
    return [
        {
            "id": str(t.id),
            "organization_id": str(t.organization_id),
            "status": t.status.value,
            "template_text": t.template_text,
            "is_active": t.is_active,
        }
        for t in templates
    ]


@router.put("/templates/{template_id}", response_model=dict)
def update_template(
    template_id: UUID,
    template_text: str,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_admin(current_user)
    template = _get_template_or_404(db, template_id, current_user.organization_id)
    template.template_text = template_text
    if is_active is not None:
        template.is_active = is_active
    db.commit()
    db.refresh(template)
    return {
        "id": str(template.id),
        "organization_id": str(template.organization_id),
        "status": template.status.value,
        "template_text": template.template_text,
        "is_active": template.is_active,
    }
