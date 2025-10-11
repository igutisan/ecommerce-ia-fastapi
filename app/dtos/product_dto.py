from pydantic import BaseModel, Field


class CreateProductDTO(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    price: float = Field(..., gt=0)


class ProductResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image_url: str | None

    class Config:
        orm_mode = True
