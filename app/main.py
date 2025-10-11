from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.dtos.login_dto import LoginDTO
from app.dtos.response_login_dto import ResponseLoginDTO
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


from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service
from app.config.security import create_access_token
from app.auth.dependencies import get_current_seller
from app.models.seller import SellerModel


@app.post("/register", status_code=201)
def register_seller(register_dto: RegisterDTO, db: Session = Depends(get_db)):
    try:
        seller = register_seller_service(register_dto, db)
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    login_dto = LoginDTO(email=form_data.username, password=form_data.password)
    seller = auth_service.authenticate_seller(db, login_dto)
    if not seller:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": seller.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/sellers/me", response_model=ResponseLoginDTO)
def read_sellers_me(current_seller: SellerModel = Depends(get_current_seller)):
    return {"email": current_seller.email, "token": current_seller.token}
