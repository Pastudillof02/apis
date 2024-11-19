from typing import List
from pydantic import BaseModel, EmailStr

class Colaborador(BaseModel):
    email: EmailStr
    nombre: str
    habilidades: List[str]

