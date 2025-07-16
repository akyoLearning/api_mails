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

    model_config = {
        "from_attributes": True
    }

