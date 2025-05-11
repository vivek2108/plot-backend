from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload

from app.auth.currentuser import CurrentUser
from app.models.users import Designations as DesignationsModel
from app.models.users import Roles as RolesModel
from app.models.users import Users as UsersModel
from app.schemas.users import UserLogin, UsersBase

# Initialize password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the given plain-text password matches the hashed password.

    Args:
        plain_password (str): The plain-text password to check.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def model_to_dict(obj) -> dict:
    """
    Converts a SQLAlchemy model instance to a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: A dictionary representation of the model.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


def create_user(db: Session, user: UsersBase, current_user: CurrentUser) -> dict:
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session.
        user (UsersBase): The user data to create.
        current_user (CurrentUser): The current user performing the operation.

    Returns:
        dict: The created user with additional role and designation info.
    Raises:
        HTTPException: If the role or designation is not found.
    """
    # Fetch the role and designation from the database
    role = db.query(RolesModel).filter_by(name=user.role).first()
    designation = db.query(DesignationsModel).filter_by(title=user.designation).first()

    # Ensure role and designation are valid
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    # Prepare user data for insertion
    user_data = user.dict(exclude={"resource_type", "designation", "role", "password"})
    user_data["created_by"] = current_user.username
    user_data["updated_by"] = current_user.username
    user_data["hashed_password"] = get_password_hash(user.password)
    user_data["designation_id"] = designation.id
    user_data["role_id"] = role.id

    # Create and save the user
    db_user = UsersModel(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Convert user object to dictionary and add role/designation info
    db_user_dict = model_to_dict(db_user)
    db_user_dict["role"] = role.name
    db_user_dict["designation"] = designation.title
    return db_user_dict


def get_user(db: Session, user_id: int) -> dict:
    """
    Retrieves a user by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user data with role and designation info.
    Raises:
        HTTPException: If the user is not found.
    """
    user = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role), joinedload(UsersModel.designation))
        .filter_by(id=user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = model_to_dict(user)
    user_dict["role"] = user.role.name
    user_dict["designation"] = user.designation.title
    return user_dict


def get_all_user(db: Session) -> list:
    """
    Retrieves all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of user data dictionaries with role and designation info.
    """
    users = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role), joinedload(UsersModel.designation))
        .all()
    )

    user_data = []
    for user in users:
        user_dict = model_to_dict(user)
        user_dict["role"] = user.role.name
        user_dict["designation"] = user.designation.title
        user_data.append(user_dict)

    return user_data


def update_user(
    db: Session, user_id: int, user_update: UsersBase, current_user: CurrentUser
) -> dict:
    """
    Updates an existing user's information.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (UsersBase): The data to update the user with.
        current_user (CurrentUser): The current user performing the update.

    Returns:
        dict: The updated user data with role and designation info.
    Raises:
        HTTPException: If the user is not found or update fails.
    """
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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


def get_user_by_username(db: Session, username: str) -> UsersModel:
    """
    Retrieves a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        UsersModel: The user model instance.
    """
    user = (
        db.query(UsersModel)
        .options(joinedload(UsersModel.role))
        .filter(UsersModel.username == username)
        .first()
    )
    return user


def authenticate_user(db: Session, user: UserLogin) -> dict:
    """
    Authenticates a user based on their username and password.

    Args:
        db (Session): The database session.
        user (UserLogin): The user login data containing username and password.

    Returns:
        dict: The authenticated user's data if valid.
        None: If authentication fails.
    """
    username = user.username
    db_user = get_user_by_username(db, username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return None

    return db_user # model_to_dict(db_user)
