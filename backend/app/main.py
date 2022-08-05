from fastapi import FastAPI
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)


# Initialize the app
app = FastAPI()


@app.get("/")
def home():
    return {"status": "API RUNNING"}
