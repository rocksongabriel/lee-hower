from fastapi import FastAPI
from . import models
from .database import engine

from app.tasks.router import router as task_router


models.Base.metadata.create_all(bind=engine)


# Initialize the app
app = FastAPI()

# Register the routes
app.include_router(task_router, prefix="/tasks", tags=["Task"])


@app.get("/")
def home():
    return {"status": "API RUNNING"}
