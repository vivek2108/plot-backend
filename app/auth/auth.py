from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.config.database import get_db

# from functools import wraps


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_token(token)
    username = payload.get("sub")
    role = payload.get("role")
    user_id = payload.get("user_id")
    if username is None or role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return CurrentUser(username=username, role=role, user_id=user_id)


def require_role(allowed_roles: list[str]):
    def wrapper(current_user: CurrentUser = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {current_user.role}",
            )
        return current_user

    return wrapper


# def require_auth(func):
#     @wraps(func)
#     def wrapper(*args,
#                 db: Session = Depends(get_db),
#                 current_user: CurrentUser = Depends(get_current_user),
#                 **kwargs):
#         if not current_user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not authenticated"
#             )
#         return func(*args, db=db, current_user=current_user, **kwargs)
#     return wrapper
