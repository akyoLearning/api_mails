from sqlalchemy import Column, Integer, String, Date, Time
from .database import Base

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    sala = Column(String, index=True)
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    responsable = Column(String)
