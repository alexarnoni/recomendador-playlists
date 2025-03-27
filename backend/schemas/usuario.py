from pydantic import BaseModel, EmailStr, Field

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6)

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
