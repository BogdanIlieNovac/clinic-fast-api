
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db


router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("", response_model=list[schemas.AppointmentOut])
def list_appointments(patient_id:int | None = None, db:Session = Depends(get_db)):
    query = select(models.Appointment)
    if patient_id is not None:
        query = query.where(models.Appointment.patient_id == patient_id)
        return db.scalars(query).all()

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id:int, db: Session = Depends(get_db)):
    appointment = db.get(models.Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appoinmtnent not found")
    return appointment

@router.post("", response_model=schemas.AppointmentOut, status_code=201)
def create_appointment(payload:schemas.AppointmentCreate, db:Session = Depends(get_db)):
    patient = db.get(models.Patient, payload.patient_id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    appointment = models.Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

# @router.patch("/{appointment_id}", response_model=schemas.AppointmentOut)
# def update_appointment(appointment_id:int, payload:schemas.AppointmentUpdate, db:Session = Depends(get_db)):
#     appointment = db.get(models.Appointment, appointment_id)
#     if appointment is None:
#         raise HTTPException(status_code=404, detail="Appointment not found")
#     print("PATCH payload:", appointment)
#     for field,value in payload.model_dump(exclude_unset=True).items():
#         setattr(appointment,field,value)
#         db.commit()
#         db.refresh(appointment)
#         return appointment

@router.patch("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(appointment_id: int, payload: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.get(models.Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    data = payload.model_dump(exclude_unset=True)
  
    for field, value in data.items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id:int, db:Session= Depends(get_db)):
    appointment = db.get(models.Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()