from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.users.models import User


class Task(Base):  # type: ignore

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=255), nullable=False, index=True)
    description = Column(String(length=500), nullable=True, index=True)
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    urgency = Column(Boolean, nullable=False, server_default="FALSE")
    importance = Column(Boolean, nullable=False, server_default="FALSE")
    completed = Column(Boolean, nullable=False, server_default="FALSE")
    time_to_spend = Column(Integer, nullable=False)
    time_spent = Column(Integer, nullable=True)

    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
