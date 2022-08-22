from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class TaskBase(BaseModel):
    """Base schema for representing a task object"""

    title: str
    description: str
    urgent: bool = False
    important: bool = False
    completed: bool = False
    time_to_spend: int
    time_spent: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for creating a Task object"""

    pass


class TaskRead(TaskBase):
    """Schema for the response model of the task objects"""

    id: UUID4
    created: datetime
    owner_id: UUID4

    class Config:
        orm_mode = True
