from pydantic import BaseModel, Field


class CreateProductDTO(BaseModel):
    name: str = Field(..., max_length=50, description="Nombre del producto (único)")
    description: str = Field(
        ..., max_length=500, description="Descripción detallada del producto"
    )
    price: int = Field(..., gt=0, description="Precio del producto (mayor que 0)")
    quantity: int = Field(
        ..., ge=0, description="Cantidad disponible en inventario (0 o más)"
    )

    class Config:
        orm_mode = True
