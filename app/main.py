from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.services.seller_service import register_seller as register_seller_service
from app.dtos.register_dto import RegisterDTO
from app.config.db_connection import get_db
import os

# Cargar variables del archivo .env
load_dotenv()

app = FastAPI(
    title="Ecommerce IA API",
    description="API para el ecommerce de la materia de IA",
    version="0.1.0",
)


@app.post("/register", status_code=201)
def register_seller(register_dto: RegisterDTO, db: Session = Depends(get_db)):
    try:
        seller = register_seller_service(register_dto, db)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
