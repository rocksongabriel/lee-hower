from fastapi import FastAPI
from . import models
from .database import engine

# import routers
from app.tasks.router import router as task_router
from app.users.routers import router as users_router

# import sqlalchemy models
from app.users.models import User

# TODO move the task model to it's own file and import it here


# Bind the sqlachemy modelds to the database
models.Base.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)


# Initialize the app
app = FastAPI()

# Register the routes
app.include_router(task_router, prefix="/tasks", tags=["Task"])
app.include_router(users_router, prefix="/users", tags=["Accounts", "Users"])


@app.get("/")
def home():
    return {"status": "API RUNNING"}
