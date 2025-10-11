import uuid
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.sql.expression import null
from app.config.db_connection import Base, engine, get_db


class SellerModel(Base):
    __tablename__ = "sellers"

    id = Column(
        String(100), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)


Base.metadata.create_all(bind=engine)
