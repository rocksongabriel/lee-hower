# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base # noqa
from app.users.models import User # noqa
from app.tasks.models import Task # noqa
