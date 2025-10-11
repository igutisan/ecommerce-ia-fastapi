from pydantic import BaseModel, Field, EmailStr


class RegisterDTO(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico válido del usuario")
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Contraseña entre 8 y 64 caracteres con al menos una mayúscula, una minúscula, un número y un carácter especial",
    )
