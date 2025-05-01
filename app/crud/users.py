from sqlalchemy.orm import Session
from app.models.users import Users as UsersModel, Roles, Designations
from app.schemas.users import Users
from app.schemas.users import UsersBase, UserLogin
import hashlib


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(db: Session, user: UsersBase):
    role = db.query(Roles).filter_by(name=user.role).first()
    designation = db.query(Designations).filter_by(title=user.designation).first()
    if not role:
        raise Exception("Enter a valid role")
    if not designation:
        raise Exception("Enter a valid designation")

    db_user = UsersModel(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        designation_id=designation.id,
        role_id=role.id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.designation = designation.title
    db_user.role = role.name
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


def validate_user(db: Session, user: UserLogin):
    username = user.username
    hashed_password=get_password_hash(user.password)
    db_user = db.query(UsersModel).filter(UsersModel.username == username, UsersModel.hashed_password == hashed_password).first()
    return db_user
