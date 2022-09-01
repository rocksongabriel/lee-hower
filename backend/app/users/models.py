from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.types import Boolean, String, TIMESTAMP

from app.db.base_class import Base


if TYPE_CHECKING:
    from app.tasks.models import Task


class User(Base):  # type: ignore
    """SQLAlchemy model for Users"""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String(length=50), nullable=True)
    last_name = Column(String(length=50), nullable=True)
    is_active = Column(Boolean, server_default="TRUE")
    is_admin = Column(Boolean, server_default="FALSE")
    created = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    password = Column(String, nullable=False)
