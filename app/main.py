from fastapi import FastAPI
from app.db import Base, engine
from app.routers import appointments, patients

Base.metadata.create_all(bind=engine)
app = FastAPI(title="clinic APi")

app.include_router(patients.router)
app.include_router(appointments.router)

@app.get("/health")
def health():
    return {"status": "ok"}