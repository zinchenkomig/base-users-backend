from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, Text, ARRAY, DateTime, func
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text, nullable=False, default='')
    tg_id = Column(Text, nullable=True)
    email = Column(Text, unique=True, nullable=True)
    password = Column(Text, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    roles = Column(ARRAY(Text), nullable=True, default=[])
    photo_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
