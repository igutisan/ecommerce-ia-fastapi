import uuid
from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db_connection import Base, engine


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(
        String(100), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=True)
    seller_id = Column(String(100), ForeignKey("sellers.id"))

    seller = relationship("SellerModel", back_populates="products")


Base.metadata.create_all(bind=engine)
