from fastapi import FastAPI
from pydantic import UUIDVersionError
import uvicorn

from app.auth.routers import router as auth_router
from app.tasks.models import Task
from app.tasks.routers import router as tasks_router
from app.users.models import User
from app.users.routers import router as users_router

from .database import engine


# Bind the sqlachemy modelds to the database
Task.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)


# Initialize the app
app = FastAPI()

# Register the routes
app.include_router(tasks_router, prefix="/tasks", tags=["Task"])
app.include_router(users_router, prefix="/users", tags=["Accounts", "Users"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def home():
    return {"status": "API RUNNING"}


if __name__ == "__main__":
    uvicorn.run(home)
