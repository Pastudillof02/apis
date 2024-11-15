from typing import List
from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    email: EmailStr
    nombre: str
    contactos: List[str]

    class Config:
        from_attributes = True

class Contacto(BaseModel):
    email: EmailStr
    nombre: str
