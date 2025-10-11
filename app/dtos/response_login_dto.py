from pydantic import BaseModel


class ResponseLoginDTO(BaseModel):
    email: str
    token: str
