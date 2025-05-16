from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.crud.users import create_user, get_all_user, get_user, update_user
from app.schemas.users import UserCredential, Users

router = APIRouter()


@router.get(
    "/",
    response_model=List[Users],
    summary="Fetch all users",
    description="Fetch a list of all users. This endpoint is only accessible "
    "by users with the 'admin' role.",
)
def fetch_all(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin"])),
) -> List[Users]:
    """
    Get a list of all users.
    Only accessible by users with the 'admin' role.

    Args:
        db (Session): SQLAlchemy database session.
        current_user (CurrentUser): Authenticated user with admin role.

    Returns:
        List[Users]: List of all users.
    """
    return get_all_user(db)


@router.get(
    "/{id}",
    response_model=Users,
    summary="Get a specific user by ID",
    description="Fetch the details of a specific user by their ID. "
    "Users can only access their own data.",
)
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> Users:
    """
    Get a specific user by ID.
    Users can only access their own data.

    Args:
        id (int): User ID to fetch.
        db (Session): SQLAlchemy session.
        current_user (CurrentUser): Authenticated user.

    Raises:
        HTTPException: If accessing another user's data or user not found.

    Returns:
        Users: User record.
    """
    if current_user.user_id != id:
        raise HTTPException(
            status_code=403, detail="Access denied to other user's data"
        )

    user = get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Users,
    summary="Register a new user",
    description="Register a new user. This endpoint is only accessible "
    "to users with the 'admin' role.",
)
def create(
    payload: UserCredential,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin"])),
) -> Users:
    """
    Register a new user.
    Only accessible to admin users.

    Args:
        payload (UserCredential): New user data.
        db (Session): SQLAlchemy session.
        current_user (CurrentUser): Admin user performing the operation.

    Returns:
        Users: Created user record.
    """
    return create_user(db, payload, current_user)


@router.put(
    "/{id}",
    response_model=Users,
    summary="Update user information",
    description="Update user information. Users can update their own data, "
    "or admins can update any user.",
)
def update(
    id: int,
    payload: UserCredential,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> Users:
    """
    Update user information.
    Users can update their own data, or admins can update any user.

    Args:
        id (int): ID of the user to update.
        payload (UserCredential): Updated user data.
        db (Session): SQLAlchemy session.
        current_user (CurrentUser): Authenticated user.

    Raises:
        HTTPException: If user tries to update another user's data.

    Returns:
        Users: Updated user record.
    """
    if current_user.is_admin() or current_user.user_id == id:
        return update_user(db, id, payload, current_user)

    raise HTTPException(status_code=403, detail="Access denied to other user's data")
