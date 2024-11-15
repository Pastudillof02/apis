import datetime
from typing import List, Tuple
from pydantic import BaseModel, EmailStr

from enum import Enum

class Evento(BaseModel):
    anfitrion: EmailStr
    descripcion: str
    inicio: datetime.date
    duracion: int
    invitados: List[Tuple[str,str]]