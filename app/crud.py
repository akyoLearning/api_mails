from sqlalchemy.orm import Session
from .models import Reserva
from .schemas import ReservaCreate

def crear_reserva(db: Session, reserva: ReservaCreate):
    nueva = Reserva(**reserva.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
