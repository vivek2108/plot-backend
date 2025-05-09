import hashlib

from sqlalchemy.orm import Session, joinedload

from app.auth.currentuser import CurrentUser
from app.models.users import Designations as DesignationsModel
from app.models.users import Roles as RolesModel
from app.models.users import Users as UsersModel
from app.schemas.users import UserLogin, UsersBase


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def model_to_dict(obj):
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


def create_user(db: Session, user: UsersBase, current_user: CurrentUser):
    role = db.query(RolesModel).filter_by(name=user.role).first()
    designation = db.query(DesignationsModel).filter_by(title=user.designation).first()
    if not role:
        raise Exception("Enter a valid role")
    if not designation:
        raise Exception("Enter a valid designation")

    user_data = user.dict(exclude={"resource_type", "designation", "role", "password"})
    user_data["created_by"] = current_user.username
    user_data["updated_by"] = current_user.username
    user_data["hashed_password"] = get_password_hash(user.password)
    user_data["designation_id"] = designation.id
    user_data["role_id"] = role.id
    db_user = UsersModel(**user_data)

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
    user_dict["role"] = user.role.name
    user_dict["designation"] = user.designation.title
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
        user_dict["role"] = user.role.name
        user_dict["designation"] = user.designation.title
        user_data.append(user_dict)

    return user_data


def update_user(
    db: Session, user_id: int, user_update: UsersBase, current_user: CurrentUser
):
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()

    if not user:
        return None

    update_data = {
        key: value
        for key, value in user_update.dict(exclude_unset=True).items()
        if value not in (None, "")
    }

    for field, value in update_data.items():
        if field == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, field, value)

    user.updated_by = current_user.username
    db.commit()
    db.refresh(user)

    user_dict = model_to_dict(user)
    user_dict["role"] = user.role.name
    user_dict["designation"] = user.designation.title
    return user_dict


def get_user_by_username(db, username: str):
    user = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role))
        .filter(UsersModel.username == username)
        .first()
    )
    return user


def authenticate_user(db: Session, user: UserLogin):
    username = user.username
    hashed_password = get_password_hash(user.password)
    db_user = get_user_by_username(db, username)

    if not db_user or db_user.hashed_password != hashed_password:
        return None
    return db_user
