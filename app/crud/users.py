from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.users import Users as UsersModel, Roles as RolesModel, Designations as DesignationsModel
from app.schemas.users import Users
from app.schemas.users import UsersBase, UserLogin
import hashlib


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def model_to_dict(obj):
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


def create_user(db: Session, user: UsersBase, current_user: str):
    role = db.query(RolesModel).filter_by(name=user.role).first()
    designation = db.query(DesignationsModel).filter_by(title=user.designation).first()
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
        created_by=current_user,
        updated_by=current_user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user = model_to_dict(db_user)
    db_user["role"] = role.name
    db_user["designation"] = designation.title
    return db_user


def get_user(db: Session, user_id: int):
    user = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role), joinedload(UsersModel.designation))
        .filter(UsersModel.id == user_id)
        .first()
    )
    user_dict = model_to_dict(user)
    print(user_dict)
    user_dict["role"] = user.role.name if user.role else None
    user_dict["designation"] = user.designation.title if user.designation else None
    return user_dict


def get_all_user(db: Session):
    users = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role), joinedload(UsersModel.designation))
        .all()
    )
    user_data = []
    # Convert related objects to strings
    for user in users:
        user_dict = model_to_dict(user)
        user_dict["role"] = user.role.name if user.role else None
        user_dict["designation"] = user.designation.title if user.designation else None
        user_data.append(user_dict)

    return user_data


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


def get_user_by_username(db, username: str):
    return db.query(UsersModel).filter(UsersModel.username == username).first()


def authenticate_user(db: Session, user: UserLogin):
    username = user.username
    hashed_password=get_password_hash(user.password)
    db_user = get_user_by_username(db, username)

    if not db_user or db_user.hashed_password != hashed_password:
        return None
    return db_user
