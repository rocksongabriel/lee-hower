from sqlalchemy import Column, Boolean, String, Integer, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=255), nullable=False, index=True)
    description = Column(String(length=500), nullable=True, index=True)
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    urgent = Column(Boolean, nullable=False, server_default="FALSE")
    important = Column(Boolean, nullable=False, server_default="FALSE")
    completed = Column(Boolean, nullable=False, server_default="FALSE")
    time_to_spend = Column(Integer, nullable=False)
    time_spent = Column(Integer, nullable=True)
