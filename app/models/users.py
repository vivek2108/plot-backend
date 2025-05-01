from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from app.config.database import Base
from datetime import datetime


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Designations(Base):
    __tablename__ = 'designations'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    designation_id = Column(Integer)
    role_id = Column(Integer)
    create_dt = Column(DateTime, default=datetime.now())
    update_dt = Column(DateTime, default=datetime.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
