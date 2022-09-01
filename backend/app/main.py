from fastapi import FastAPI

from app.auth.routers import router as auth_router
from app.tasks.models import Task
from app.tasks.routers import router as tasks_router
from app.users.models import User
from app.users.routers import router as users_router

from app.db.config import engine


# Bind the sqlachemy modelds to the database
Task.metadata.create_all(bind=engine) # type: ignore
User.metadata.create_all(bind=engine) # type: ignore


# Initialize the app
app = FastAPI()

# Register the routes
app.include_router(tasks_router, prefix="/tasks", tags=["Task"])
app.include_router(users_router, prefix="/users", tags=["Accounts", "Users"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def home():
    return {"status": "API RUNNING"}
