import datetime
from typing import List, Tuple
from pydantic import BaseModel, EmailStr, Field

class Tarea(BaseModel):
    responsable: EmailStr
    descripcion: str
    habilidades: List[str]
    segmentos: int = Field(..., gt=0)
    colaboradores: List[EmailStr]