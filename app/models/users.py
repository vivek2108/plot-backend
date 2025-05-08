from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    users = relationship("Users", back_populates="role")


class Designations(Base):
    __tablename__ = 'designations'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    users = relationship("Users", back_populates="designation")


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    designation_id = Column(Integer, ForeignKey("designations.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    create_dt = Column(DateTime, default=func.now(), nullable=False)
    update_dt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    role = relationship("Roles", back_populates="users")
    designation = relationship("Designations", back_populates="users")
