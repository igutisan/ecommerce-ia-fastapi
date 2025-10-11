from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.db_connection import get_db
from app.config.security import get_password_hash
from app.dtos.register_dto import RegisterDTO
from app.models.seller import SellerModel
import uuid


def register_seller(registerDTO: RegisterDTO, db: Session = Depends(get_db)):
    db_user = (
        db.query(SellerModel).filter(SellerModel.email == registerDTO.email).first()
    )
    if db_user:
        raise ValueError("Email already exists")

    hashed_password = get_password_hash(registerDTO.password)

    new_user = SellerModel(email=registerDTO.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
