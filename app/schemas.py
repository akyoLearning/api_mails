from pydantic import BaseModel
from datetime import date, time

class ReservaCreate(BaseModel):
    sala: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    responsable: str

class ReservaOut(ReservaCreate):
    id: int

    class Config:
        orm_mode = True
