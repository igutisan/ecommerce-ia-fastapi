from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.sql.expression import null
from app.config.db_connection import Base, engine, get_db


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, UUID=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=False)


Base.metadata.create_all(bind=engine)
