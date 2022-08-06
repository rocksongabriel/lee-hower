from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy.types import Boolean, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from app.database import Base


class User(Base):
    """SQLAlchemy model for Users"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String(length=50), nullable=True)
    last_name = Column(String(length=50), nullable=True)
    is_active = Column(Boolean, server_default="TRUE")
    created = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    password = Column(String, nullable=False)