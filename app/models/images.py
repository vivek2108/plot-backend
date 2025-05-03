from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime
from app.config.database import Base
from datetime import datetime

class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer)
    image_type = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    highlight_coordinates = Column(JSONB, nullable=True)
    create_dt = Column(DateTime, default=datetime.now())
    update_dt = Column(DateTime, default=datetime.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
