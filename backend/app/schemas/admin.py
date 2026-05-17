from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.enums import OrganizationStatus, SubscriptionStatus
from app.schemas.organization import OrganizationResponse
from app.schemas.user import UserResponse


class AdminCreateOrganizationRequest(BaseModel):
    organization_name: str
    organization_email: EmailStr
    organization_phone: str = ""
    admin_full_name: str
    admin_email: EmailStr
    password: str
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None
    footer_text: str | None = None
    status: OrganizationStatus = OrganizationStatus.pending


class AdminCreateOrganizationResponse(BaseModel):
    message: str
    organization: OrganizationResponse
    admin_user: UserResponse


class AdminUpdateOrganizationRequest(BaseModel):
    organization_name: str | None = None
    organization_email: EmailStr | None = None
    organization_phone: str | None = None
    footer_text: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None


class ActivationRequest(BaseModel):
    expiration_date: date | None = None
    notes: str | None = None


class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID | None = None
    organization_id: UUID | None = None
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SubscriptionActivationResponse(BaseModel):
    id: UUID
    organization_id: UUID
    activated_by_user_id: UUID | None = None
    activation_date: date
    expiration_date: date | None = None
    status: SubscriptionStatus
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SuperAdminDashboardResponse(BaseModel):
    total_organizations: int
    active_organizations: int
    pending_organizations: int
    suspended_organizations: int
    new_registration_requests: int


class SchoolDashboardResponse(BaseModel):
    active_students: int
    active_guardians: int
    today_attendance: int
    today_absences: int
    today_late_arrivals: int
    today_excused: int
