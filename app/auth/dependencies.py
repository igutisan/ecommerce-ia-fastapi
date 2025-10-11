import re
from fastapi import Depends, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import ResultProxy
from sqlalchemy.orm import Session
from app.config import security
from app.config.db_connection import get_db
from app.dtos.response_login_dto import ResponseLoginDTO
from app.models.seller import SellerModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_seller(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> ResponseLoginDTO:
    email = security.verify_token(token, credentials_exception)
    seller = db.query(SellerModel).filter(SellerModel.email == email).first()
    response = ResponseLoginDTO(email=email, token=token)
    if seller is None:
        raise credentials_exception
    return response
