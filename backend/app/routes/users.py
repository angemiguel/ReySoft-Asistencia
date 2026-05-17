from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.permissions import ensure_school_admin, ensure_school_user
from app.core.security import hash_password
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models import User, UserRole
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(db: Session, user_id: UUID, organization_id: UUID) -> User:
    user = db.scalar(
        select(User).where(User.id == user_id, User.organization_id == organization_id)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    full_name: str,
    email: str,
    password: str,
    role: UserRole = UserRole.staff,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_admin(current_user)
    existing = db.scalar(select(User.id).where(User.email == email.lower()).limit(1))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo ya está registrado.")
    user = User(
        organization_id=current_user.organization_id,
        full_name=full_name,
        email=email.lower(),
        password_hash=hash_password(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[UserResponse])
def list_users(
    search: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_user(current_user)
    query = select(User).where(User.organization_id == current_user.organization_id)
    if search:
        term = f"%{search}%"
        query = query.where(or_(User.full_name.ilike(term), User.email.ilike(term)))
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    return db.scalars(query.order_by(User.full_name)).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_user(current_user)
    return _get_user_or_404(db, user_id, current_user.organization_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    full_name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_admin(current_user)
    user = _get_user_or_404(db, user_id, current_user.organization_id)
    if email is not None:
        email_lower = email.lower()
        existing = db.scalar(
            select(User.id).where(User.email == email_lower, User.id != user.id).limit(1)
        )
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo ya está registrado.")
        user.email = email_lower
    if full_name is not None:
        user.full_name = full_name
    if password is not None:
        user.password_hash = hash_password(password)
    if role is not None:
        user.role = role
    if is_active is not None:
        user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_school_admin(current_user)
    user = _get_user_or_404(db, user_id, current_user.organization_id)
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user
