from multiprocessing import Lock
from sqlalchemy.orm import Session
from app.models.seller import SellerModel
from app.config.security import verify_password
from app.dtos.login_dto import LoginDTO


def authenticate_seller(db: Session, loginDto: LoginDTO) -> SellerModel | None:
    seller = db.query(SellerModel).filter(SellerModel.email == loginDto.email).first()
    if not seller:
        return None
    if not verify_password(loginDto.password, seller.password):
        return None
    return seller
