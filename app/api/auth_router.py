from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import create_access_token
from app.config.database import get_db
from app.crud.users import authenticate_user
from app.schemas.users import UserLogin

router = APIRouter()


@router.post("/login", response_model=Dict[str, str])
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Authenticate user using JSON credentials and return a JWT access token.

    Args:
        payload (UserLogin): User credentials (username and password).
        db (Session): Database session.

    Raises:
        HTTPException: If authentication fails.

    Returns:
        Dict[str, str]: JWT access token and token type.
    """
    user = authenticate_user(db, payload)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    data = {"sub": user.username, "role": user.role.name, "user_id": user.id}
    access_token = create_access_token(data=data, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Dict[str, str])
def token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    OAuth2-compatible login endpoint using form-encoded body for Swagger UI.

    Args:
        form_data (OAuth2PasswordRequestForm): Form with username and password.
        db (Session): Database session.

    Raises:
        HTTPException: If authentication fails.

    Returns:
        Dict[str, str]: JWT access token and token type.
    """
    user = authenticate_user(db, form_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    data = {"sub": user.username, "role": user.role.name, "user_id": user.id}
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}
