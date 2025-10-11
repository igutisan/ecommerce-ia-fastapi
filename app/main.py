from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    app_name = os.getenv("APP_NAME", "FastAPI App")
    env = os.getenv("APP_ENV", "production")
    return {"app_name": app_name, "environment": env}
