
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, index=True)

    description = Column(Text, nullable=True)

    status = Column(String(20), nullable=False, default="active")

    environment = Column(String(20), nullable=False, default="development")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
