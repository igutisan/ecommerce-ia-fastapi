from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.dtos.login_dto import LoginDTO
from app.dtos.response_login_dto import ResponseLoginDTO
from app.services.seller_service import register_seller as register_seller_service
from app.dtos.register_dto import RegisterDTO
from app.config.db_connection import get_db
import os
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service
from app.config.security import create_access_token
from app.auth.dependencies import get_current_seller
from app.models.seller import SellerModel
from app.dtos.create_product_dto import CreateProductDTO
from app.services import products_service

# Cargar variables del archivo .env
load_dotenv()

app = FastAPI(
    title="Ecommerce IA API",
    description="API para el ecommerce de la materia de IA",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


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


from typing import List
from app.dtos.product_dto import ProductResponseDTO


@app.post("/products", status_code=201)
async def create_new_product(
    product_dto: CreateProductDTO,
    db: Session = Depends(get_db),
    current_seller: SellerModel = Depends(get_current_seller),
):
    try:
        product = await products_service.create_product(
            product_dto, current_seller.id, db
        )
        return product
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/products/me", response_model=List[ProductResponseDTO])
def get_my_products(
    db: Session = Depends(get_db),
    current_seller: SellerModel = Depends(get_current_seller),
):
    return products_service.get_products_by_seller(db, seller_id=current_seller.id)
