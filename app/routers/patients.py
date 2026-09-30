


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db

router =APIRouter(prefix="/patients", tags=["patients"])


@router.get("" , response_model=list[schemas.PatientOut])
def list_patients(db:Session = Depends(get_db)):
    return db.scalars(select(models.Patient)).all()

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id:int, db:Session = Depends(get_db)):
   patient = db.get(models.Patient,patient_id)
   if patient is None:
       raise HTTPException(status_code=404, detail="Patient not found")
   return patient

@router.patch("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    patient_id:int,
    payload:schemas.PatientUpdate, 
    db:Session = Depends(get_db)
):
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient,field,value,)
        db.commit()
        db.refresh(patient)
        return patient
    

@router.post("" ,response_model=schemas.PatientOut, status_code=201 )
def create_patient(payload: schemas.PatientCreate, db:Session=Depends(get_db)):
    patient = models.Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id:int, db:Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not fount")
    db.delete(patient)
    db.commit()
    