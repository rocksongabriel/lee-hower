# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base
from app.users.models import User
from app.tasks.models import Task
