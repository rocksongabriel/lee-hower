from fastapi import FastAPI


# Initialize the app
app = FastAPI()


@app.get("/")
def home():
    return {"status": "API RUNNING"}
