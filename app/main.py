from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from fastapi.middleware.cors import CORSMiddleware

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
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if authorization != "Bearer TU_TOKEN_SECRETO":
        raise HTTPException(status_code=401, detail="No autorizado")
    return crud.crear_reserva(db, reserva)
