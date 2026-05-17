from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import (
    AttendanceRecord,
    AttendanceStatus,
    Course,
    Guardian,
    Notification,
    NotificationType,
    Organization,
    OrganizationStatus,
    Student,
    StudentGuardian,
    SubscriptionActivation,
    SubscriptionStatus,
    User,
    WhatsAppMessageTemplate,
)


def sync_expired_organization(db: Session, organization: Organization | None) -> bool:
    if not organization or organization.status != OrganizationStatus.active:
        return False
    current_activation = db.scalar(
        select(SubscriptionActivation).where(
            SubscriptionActivation.organization_id == organization.id,
            SubscriptionActivation.status == SubscriptionStatus.active,
        )
    )
    if not current_activation:
        return False
    from datetime import date
    if current_activation.expiration_date and current_activation.expiration_date < date.today():
        organization.status = OrganizationStatus.suspended
        current_activation.status = SubscriptionStatus.expired
        db.add(
            Notification(
                organization_id=organization.id,
                title="Suscripción expirada",
                message=f"La suscripción de {organization.name} ha expirado.",
                type=NotificationType.warning,
            )
        )
        return True
    return False


def sync_expired_organizations(db: Session) -> None:
    from datetime import date
    today = date.today()
    active_orgs = db.scalars(
        select(Organization).where(Organization.status == OrganizationStatus.active)
    ).all()
    for org in active_orgs:
        sync_expired_organization(db, org)
