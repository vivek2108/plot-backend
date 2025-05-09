from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.config.database import get_db

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with an expiration.

    Args:
        data (Dict[str, Any]): The data to encode in the token.
        expires_delta (Optional[timedelta], optional): Custom expiration time. Defaults to 30 minutes.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.

    Args:
        token (str): The token to verify.

    Raises:
        HTTPException: If the token is invalid or expired.

    Returns:
        Dict[str, Any]: Decoded token payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> CurrentUser:
    """
    Extract the current authenticated user from the JWT token.

    Args:
        token (str, optional): JWT token provided via OAuth2 scheme.
        db (Session): Database session for future validation if needed.

    Raises:
        HTTPException: If the token is invalid or required fields are missing.

    Returns:
        CurrentUser: Authenticated user context.
    """
    payload = verify_token(token)
    username = payload.get("sub")
    role = payload.get("role")
    user_id = payload.get("user_id")
    if username is None or role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return CurrentUser(username=username, role=role, user_id=user_id)


def require_role(allowed_roles: List[str]) -> Callable[[CurrentUser], CurrentUser]:
    """
    Role-based access control dependency factory.

    Args:
        allowed_roles (List[str]): Roles allowed to access the endpoint.

    Raises:
        HTTPException: If the current user's role is not in the allowed list.

    Returns:
        Callable[[CurrentUser], CurrentUser]: A FastAPI dependency function.
    """
    def wrapper(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {current_user.role}",
            )
        return current_user

    return wrapper


# Optional decorator for future use
# from functools import wraps

# def require_auth(func: Callable) -> Callable:
#     @wraps(func)
#     def wrapper(*args, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user), **kwargs):
#         if not current_user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not authenticated"
#             )
#         return func(*args, db=db, current_user=current_user, **kwargs)
#     return wrapper
