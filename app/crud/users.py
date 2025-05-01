from sqlalchemy.orm import Session
from models.users import Users as UsersModel
from schemas.users import Users
from schemas.users import UsersBase
import hashlib

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(db: Session, user: UsersBase):
    db_user = UsersModel(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        designation=user.designation,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(UsersModel).filter(UsersModel.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: UsersBase):
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user:
        if user_update.email:
            user.email = user_update.email
        if user_update.full_name:
            user.full_name = user_update.full_name
        if user_update.password:
            user.hashed_password = get_password_hash(user_update.password)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
