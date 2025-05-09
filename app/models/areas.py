from sqlalchemy import Column, Integer, String

from app.config.database import Base


class Areas(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
