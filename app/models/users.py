from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from crud.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    designation = Column(String)
    is_admin = Column(Boolean, default=False)
    create_dt = Column(DateTime, nullable=True)
    update_dt = Column(DateTime, nullable=True)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
