import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine


class SellerModel(Base):
    __tablename__ = "sellers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    products = relationship("ProductModel", back_populates="seller")


Base.metadata.create_all(bind=engine)
