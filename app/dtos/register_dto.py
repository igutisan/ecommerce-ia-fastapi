from pydantic import BaseModel


class RegisterDTO(BaseModel):
    email: str
    password: str
