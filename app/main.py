from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
from app.correo_reader import leer_y_enviar_correos
import os

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

SECRET_TOKEN = os.getenv("TOKEN", "TU_TOKEN_SECRETO")
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API de Reservas de Sala",
    description="Permite registrar reservas de salas desde un correo electrónico.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/reservas", response_model=schemas.ReservaOut)
def crear_reserva(
    reserva: schemas.ReservaCreate,
    authorization: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    print(f"TOKEN recibido: {authorization}")
    print(f"TOKEN esperado: Bearer {SECRET_TOKEN}")

    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="No autorizado")
    return crud.crear_reserva(db, reserva)


@app.get("/leer-correos")
def ejecutar_lector():
    resultados = leer_y_enviar_correos()
    return {"resultados": resultados}


